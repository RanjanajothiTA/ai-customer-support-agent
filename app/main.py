from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from app.agent.decision import AgentDecision, Intent, Route, ToolName
from app.agent.executor import execute_agent
from app.agent.decision_engine import decide
from app.memory.conversation_store import ConversationStore


app = FastAPI(
    title="AI Customer Support Agent",
    description=(
        "An AI-powered customer support agent that can handle "
        "customer queries and provide assistance."
    ),
    version="1.0.0"
)

conversation_store = ConversationStore()


class ChatRequest(BaseModel):
    message: str = Field(max_length=2000)
    customer_id: str = Field(pattern=r"^CUST\d+$")
    conversation_id: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9_-]+$"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Please write your request.")

        return value


class Source(BaseModel):
    source: str
    chunk_id: int


class ChatResponse(BaseModel):
    response: str
    sources: list[Source] = Field(default_factory=list)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Load or create the conversation.
    state = conversation_store.get_conversation(
        request.conversation_id
    )

    if state is None:
        state = conversation_store.create_conversation(
            request.conversation_id,
            request.customer_id
        )
    elif state.customer_id != request.customer_id:
        return {
            "response": "This conversation does not belong to this customer.",
            "sources": []
        }

    # Save the user's message.
    conversation_store.add_message(
        request.conversation_id,
        "user",
        request.message
    )

    message = request.message.strip().lower()
    pending_order_id = state.pending_cancellation_order_id

    # --------------------------------------------------
    # Handle an existing cancellation confirmation.
    # --------------------------------------------------
    if pending_order_id:

        if message in {
            "yes",
            "yes please",
            "confirm",
            "confirm cancellation"
        }:
            decision = AgentDecision(
                intent=Intent.CANCEL_ORDER,
                route=Route.CONFIRMATION,
                tool=ToolName.CANCEL_ORDER,
                tool_input={
                    "order_id": pending_order_id,
                    "customer_id": request.customer_id
                },
                needs_confirmation=False,
                confirmation_received=True
            )

            # Execute the cancellation tool.
            response = safe_execute_agent(
                decision,
                request.message
            )

            # Convert the tool result into a user-friendly response.
            if isinstance(response, dict) and "success" in response:
                if response["success"]:
                    data = response.get("data") or {}
                    order_id = data.get(
                        "order_id",
                        pending_order_id
                    )

                    response = {
                        "response": (
                            f"Order {order_id} has been "
                            "cancelled successfully."
                        ),
                        "sources": []
                    }
                else:
                    response = {
                        "response": (
                            response.get("error")
                            or "I couldn't cancel the order. Please try again."
                        ),
                        "sources": []
                    }
            elif isinstance(response, dict):
                response = {
                    "response": response.get(
                        "response",
                        response.get("message", str(response))
                    ),
                    "sources": response.get("sources", [])
                }
            else:
                response = {
                    "response": str(response),
                    "sources": []
                }

            if not (
            isinstance(response, dict)
            and "something went wrong while processing your request"
            in response.get("response", "").lower()
            ):
                conversation_store.clear_pending_cancellation(
                request.conversation_id
            )

        elif message in {
            "no",
            "no thanks",
            "don't cancel",
            "do not cancel"
        }:
            conversation_store.clear_pending_cancellation(
                request.conversation_id
            )

            response = {
                "response": (
                    f"Okay, I won't cancel order {pending_order_id}."
                ),
                "sources": []
            }

        else:
            # Do not execute cancellation for unrelated messages.
            response = {
                "response": (
                    f"Order {pending_order_id} is awaiting cancellation "
                    "confirmation. Please reply 'yes' to confirm or 'no' "
                    "to keep the order."
                ),
                "sources": []
            }

        conversation_store.add_message(
            request.conversation_id,
            "assistant",
            response["response"]
        )

        return response

    # --------------------------------------------------
    # No pending cancellation: process normally.
    # --------------------------------------------------
    normalized_message = request.message.lower()
    policy_intent = None

    if "refund policy" in normalized_message:
        policy_intent = Intent.REFUND_POLICY
    elif "shipping policy" in normalized_message:
        policy_intent = Intent.SHIPPING_POLICY
    elif "warranty" in normalized_message:
        policy_intent = Intent.WARRANTY
    elif "return" in normalized_message:
        policy_intent = Intent.RETURN_POLICY

    if policy_intent is not None:
        decision = AgentDecision(
            intent=policy_intent,
            route=Route.RAG,
            tool_input={"query": request.message}
        )
    else:
        decision = decide(
            request.message,
            request.customer_id,
            current_order_id=state.current_order_id
        )

    tool_input = decision.tool_input or {}

    conversation_store.update_context(
        request.conversation_id,
        current_order_id=tool_input.get("order_id"),
        current_issue=tool_input.get("issue_type"),
        last_intent=decision.intent.value
    )

    response = safe_execute_agent(
        decision,
        request.message
    )

    # --------------------------------------------------
    # Normalize responses and save pending confirmations.
    # --------------------------------------------------
    if isinstance(response, dict):

        if response.get("type") == "confirmation_required":
            conversation_store.update_context(
                request.conversation_id,
                pending_cancellation_order_id=response["order_id"]
            )

            response = {
                "response": response["message"],
                "sources": []
            }

        elif response.get("type") == "cancellation_not_allowed":
            response = {
                "response": response.get(
                    "message",
                    "This order is not eligible for cancellation."
                ),
                "sources": []
            }

        elif "success" in response:
            if response["success"]:
                data = response.get("data") or {}
                order_id = data.get("order_id", "your order")

                response = {
                    "response": f"Successfully processed order {order_id}.",
                    "sources": []
                }
            else:
                response = {
                    "response": (
                        response.get("error")
                        or "I couldn't complete your request. Please try again."
                    ),
                    "sources": []
                }

        else:
            response = {
                "response": response.get(
                    "response",
                    response.get("message", str(response))
                ),
                "sources": response.get("sources", [])
            }

    else:
        response = {
            "response": str(response),
            "sources": []
        }

    # Save the assistant's reply.
    conversation_store.add_message(
        request.conversation_id,
        "assistant",
        response["response"]
    )

    return response


def safe_execute_agent(decision, user_message):
    try:
        return execute_agent(decision, user_message)
    except Exception:
        return {
            "response": (
                "I'm sorry, something went wrong while processing "
                "your request. Please try again."
            ),
            "sources": [],
            "execution_failed": True,
        }