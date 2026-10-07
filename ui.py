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

def send_message_to_backend(message):
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
        json={"message": message},
        timeout=60
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm the ShopEase AI Support Agent. "
                "I can currently answer questions using the ShopEase "
                "knowledge base."
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
        "Customer tools will use this ID when the agent layer is connected."
    )

    st.divider()

    # --------------------------------------------------------
    # Quick Actions
    # --------------------------------------------------------

    st.subheader("Quick Actions")

    st.info(
        "Knowledge-base questions are currently supported. "
        "Business tools will be connected through the agent layer."
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

if user_input:

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

            result = send_message_to_backend(user_input)

            answer = result.get(
                "response",
                "No response received from the backend."
            )

            sources = result.get(
                "sources",
                []
            )

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
                f"⚠️ The backend returned an HTTP error: {error}"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )

            st.session_state.backend_status = "HTTP Error"

        except Exception:

            error_message = (
                "⚠️ Something went wrong while processing "
                "your request."
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