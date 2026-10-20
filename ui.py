import uuid
from typing import Any

import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ShopEase AI Support",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .shopease-header {
            text-align: center;
            padding: 1rem 0 1.5rem 0;
        }

        .shopease-title {
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .shopease-subtitle {
            color: #777;
            font-size: 1rem;
        }

        .status-card {
            padding: 0.7rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            background-color: #f7f7f7;
        }

        .source-item {
            padding: 0.5rem 0;
            border-bottom: 1px solid #eeeeee;
        }

        .footer {
            text-align: center;
            color: #888;
            font-size: 0.8rem;
            padding: 2rem 0 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BACKEND API
# ============================================================

def send_message_to_backend(
    message: str,
    customer_id: str,
    conversation_id: str
) -> dict[str, Any]:
    """
    Send the user's message to the FastAPI backend.

    Returns:
        dict:
            {
                "response": "...",
                "sources": [...]
            }
    """

    response = requests.post(
        CHAT_ENDPOINT,
        json={
            "message": message,
            "customer_id": customer_id,
            "conversation_id": conversation_id
        },
        timeout=60
    )

    response.raise_for_status()

    result = response.json()
    if not isinstance(result, dict) or not isinstance(
        result.get("response"), str
    ):
        raise ValueError("The backend returned an unexpected response.")

    sources = result.get("sources", [])
    if not isinstance(sources, list) or any(
        not isinstance(source, dict)
        or not isinstance(source.get("source"), str)
        or not isinstance(source.get("chunk_id"), int)
        for source in sources
    ):
        raise ValueError("The backend returned invalid source information.")

    return {
        "response": result["response"],
        "sources": sources
    }


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm the ShopEase AI Support Agent. "
                "I can help with orders, refunds, cancellations, "
                "and ShopEase policies."
            ),
            "sources": []
        }
    ]

if "latest_sources" not in st.session_state:
    st.session_state.latest_sources = []

if "last_user_message" not in st.session_state:
    st.session_state.last_user_message = ""

if "backend_status" not in st.session_state:
    st.session_state.backend_status = "Unknown"

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = uuid.uuid4().hex


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛍️ ShopEase")
    st.caption("AI Customer Support Agent")

    st.divider()

    # --------------------------------------------------------
    # Customer Information
    # --------------------------------------------------------

    st.subheader("Customer")

    customer_id = st.text_input(
        "Customer ID",
        value="CUST1001"
    )

    st.caption(
        "Requests are scoped to this customer ID. "
        "This demo does not authenticate customer identities."
    )

    st.divider()

    # --------------------------------------------------------
    # Quick Actions
    # --------------------------------------------------------

    st.subheader("Quick Actions")

    st.info(
        "Ask about orders, refunds, policies, or cancellation requests."
    )

    if st.button(
        "📄 Ask about Return Policy",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is the return policy?"
        )

    if st.button(
        "💰 Ask about Refund Policy",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is the refund policy?"
        )

    if st.button(
        "🚚 Ask about Shipping",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is the shipping policy?"
        )

    if st.button(
        "🛡️ Ask about Warranty",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is the warranty policy?"
        )

if "active_customer_id" not in st.session_state:
    st.session_state.active_customer_id = customer_id
elif st.session_state.active_customer_id != customer_id:
    st.session_state.active_customer_id = customer_id
    st.session_state.conversation_id = uuid.uuid4().hex
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm the ShopEase AI Support Agent. "
                "I can help with orders, refunds, cancellations, "
                "and ShopEase policies."
            ),
            "sources": []
        }
    ]
    st.session_state.latest_sources = []
    st.session_state.last_user_message = ""
    st.session_state.backend_status = "Unknown"


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="shopease-header">
        <div class="shopease-title">
            🛍️ ShopEase AI Support
        </div>
        <div class="shopease-subtitle">
            AI-powered customer support using FastAPI, RAG, FAISS and Gemini
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CUSTOMER / SYSTEM INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Customer",
        customer_id
    )

with col2:
    st.metric(
        "Knowledge Base",
        "83 chunks"
    )

with col3:
    st.metric(
        "Vector Store",
        "FAISS"
    )


st.divider()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        st.markdown(message["content"])

        sources = message.get("sources", [])

        if sources:

            with st.expander("📚 Knowledge Base Sources"):

                for source in sources:

                    st.markdown(
                        f"**📄 {source['source']}**"
                    )

                    st.caption(
                        f"Chunk ID: {source['chunk_id']}"
                    )


# ============================================================
# QUICK QUESTION HANDLING
# ============================================================

quick_question = st.session_state.pop(
    "quick_question",
    None
)


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask your ShopEase support question..."
)

if quick_question:
    user_input = quick_question


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input and user_input.strip():
    user_input = user_input.strip()

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "sources": []
        }
    )

    st.session_state.last_user_message = user_input

    # --------------------------------------------------------
    # Call FastAPI
    # --------------------------------------------------------

    with st.spinner("ShopEase AI is thinking..."):

        try:

            result = send_message_to_backend(
                user_input,
                customer_id.strip(),
                st.session_state.conversation_id
            )

            answer = result["response"]
            sources = result["sources"]

            st.session_state.latest_sources = sources
            st.session_state.backend_status = "Connected"

            # ------------------------------------------------
            # Save assistant response
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )

        except requests.exceptions.ConnectionError:

            error_message = (
                "⚠️ I couldn't connect to the FastAPI backend. "
                "Please make sure the FastAPI server is running."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "Disconnected"

        except requests.exceptions.Timeout:

            error_message = (
                "⏳ The request took too long. "
                "The AI service may be temporarily busy. "
                "Please try again."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "Timeout"

        except requests.exceptions.HTTPError as error:

            error_message = (
                "⚠️ The backend rejected this request "
                f"(HTTP {error.response.status_code}). "
                "Please check the customer ID and try again."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "HTTP Error"

        except ValueError:

            error_message = (
                "⚠️ The support service returned an unexpected response. "
                "Please try again."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "Error"

        except requests.exceptions.RequestException:
            error_message = (
                "⚠️ The support service could not complete the request. "
                "Please try again."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "Error"

    # --------------------------------------------------------
    # Refresh UI
    # --------------------------------------------------------

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ShopEase AI Customer Support Agent ·
        FastAPI + RAG + FAISS + Gemini
    </div>
    """,
    unsafe_allow_html=True
)