
from app.agent.decision import AgentDecision, Route
from app.agent.router import route_decision
from app.agent.handlers import handle_final_response


def execute_agent(decision: AgentDecision, user_message: str):
    agent_result = route_decision(decision)

    if decision.route in (Route.TOOL, Route.RAG):
        final_response = handle_final_response(
            user_message,
            agent_result
        )

        return {
            "response": final_response,
            "sources": agent_result.get("sources", [])
        }

    if isinstance(agent_result, dict):
        return agent_result

    if agent_result == "ESCALATION":
        return {
            "response": (
                "I'm unable to handle this request directly. "
                "Please contact customer support for further assistance."
            ),
            "sources": []
        }

    if agent_result == "CLARIFICATION":
        return {
            "response": decision.clarification_question
            or "Could you please provide more details?",
            "sources": []
        }

    return {
        "response": str(agent_result),
        "sources": []
    }
