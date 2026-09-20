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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        background-color: #f5f7fb;
    }

    /* ShopEase title */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .app-subtitle {
        font-size: 1.15rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 1.2rem;
    }

    /* Chat container */
    .chat-shell {
        border: 1px solid #dfe6ee;
        border-radius: 16px;
        background-color: #ffffff;
        padding: 1.2rem;
        min-height: 350px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }

    .chat-header {
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .chat-subtitle {
        color: #64748b;
        margin-bottom: 1rem;
    }

    /* Chat messages */
    .message {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        max-width: 75%;
    }

    .user-message {
        margin-left: auto;
        background-color: #e0f2fe;
        color: #0f172a;
    }

    .bot-message {
        margin-right: auto;
        background-color: #f1f5f9;
        color: #0f172a;
    }

    /* Sidebar */
    .sidebar-section {
        margin-bottom: 1.2rem;
    }

    .sidebar-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }

    /* Status items */
    .status-item {
        margin-bottom: 0.35rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm the ShopEase AI Support Agent. "
                "I can help with orders, returns, refunds, "
                "shipping, and support requests."
            )
        }
    ]


if "debug_info" not in st.session_state:

    st.session_state.debug_info = {
        "intent": "Waiting for user",
        "decision": "Waiting",
        "tool": "Not used",
        "rag": "Not used",
        "sources": "None",
        "latency": "-"
    }


# ============================================================
# MOCK RESPONSE FUNCTION
# ============================================================

def get_mock_response(user_message):
    """
    Temporary mock response.

    Later this function will be replaced by:

    Streamlit
        ↓
    FastAPI
        ↓
    AI Agent
        ↓
    RAG / Tools / Memory
        ↓
    LLM
    """

    message = user_message.lower()

    # -------------------------
    # Order status
    # -------------------------

    if "order" in message and (
        "status" in message
        or "where" in message
        or "track" in message
    ):

        st.session_state.debug_info = {
            "intent": "Order Status",
            "decision": "Tool Call",
            "tool": "get_order_status",
            "rag": "Not Used",
            "sources": "None",
            "latency": "1.42 sec"
        }

        return (
            "Your order **ORD1001** has been shipped. "
            "The expected delivery date is **September 23, 2026**. "
            "Tracking number: **TRK987654**."
        )

    # -------------------------
    # Return policy
    # -------------------------

    if "return" in message:

        st.session_state.debug_info = {
            "intent": "Return Policy",
            "decision": "RAG Retrieval",
            "tool": "Not Used",
            "rag": "Used",
            "sources": "return_policy.pdf",
            "latency": "1.21 sec"
        }

        return (
            "According to the ShopEase return policy, "
            "eligible products can be returned within the "
            "specified return period and must satisfy the "
            "return conditions."
        )

    # -------------------------
    # Refund
    # -------------------------

    if "refund" in message:

        st.session_state.debug_info = {
            "intent": "Refund Status",
            "decision": "Tool Call",
            "tool": "check_refund_status",
            "rag": "Not Used",
            "sources": "None",
            "latency": "1.36 sec"
        }

        return (
            "The refund for order **ORD1005** is currently "
            "**processing**. The refund amount is **₹2,499**."
        )

    # -------------------------
    # Cancellation
    # -------------------------

    if "cancel" in message:

        st.session_state.debug_info = {
            "intent": "Order Cancellation",
            "decision": "Confirmation Required",
            "tool": "cancel_order",
            "rag": "Not Used",
            "sources": "None",
            "latency": "-"
        }

        return (
            "Order **ORD1001** may be eligible for cancellation. "
            "Before I proceed, please confirm that you want to "
            "cancel this order."
        )

    # -------------------------
    # Damaged product
    # -------------------------

    if "damaged" in message or "broken" in message:

        st.session_state.debug_info = {
            "intent": "Damaged Product",
            "decision": "Support Ticket",
            "tool": "create_support_ticket",
            "rag": "Not Used",
            "sources": "None",
            "latency": "1.51 sec"
        }

        return (
            "I'm sorry that your product arrived damaged. "
            "I can help create a support ticket for this issue."
        )

    # -------------------------
    # Default response
    # -------------------------

    st.session_state.debug_info = {
        "intent": "Unknown",
        "decision": "Escalation / Clarification",
        "tool": "Not Used",
        "rag": "Not Used",
        "sources": "None",
        "latency": "-"
    }

    return (
        "I can help with order status, returns, refunds, "
        "shipping, cancellations, and support requests. "
        "Could you provide a little more information?"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛍️ ShopEase")

    st.divider()

    # -------------------------
    # Customer
    # -------------------------

    st.markdown("### 👤 Customer")

    st.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-label">Customer ID</div>
            <strong>CUST1001</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------
    # Quick actions
    # -------------------------

    st.markdown("### ⚡ Quick Actions")

    if st.button("📦 Order Status", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Where is my order ORD1001?"
            }
        )

        response = get_mock_response(
            "Where is my order ORD1001?"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    if st.button("↩️ Return Policy", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "What is your return policy?"
            }
        )

        response = get_mock_response(
            "What is your return policy?"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    if st.button("💰 Refund Status", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "What is the status of my refund?"
            }
        )

        response = get_mock_response(
            "What is the status of my refund?"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    if st.button("❌ Cancel Order", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "I want to cancel my order ORD1001."
            }
        )

        response = get_mock_response(
            "I want to cancel my order ORD1001."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    if st.button("🎫 Create Ticket", use_container_width=True):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": "My product arrived damaged."
            }
        )

        response = get_mock_response(
            "My product arrived damaged."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    st.divider()

    # -------------------------
    # Developer / Debug
    # -------------------------

    with st.expander("🔍 Developer / Debug", expanded=True):

        debug = st.session_state.debug_info

        st.write("**Intent**")
        st.write(debug["intent"])

        st.write("**Decision**")
        st.write(debug["decision"])

        st.write("**Tool**")
        st.write(debug["tool"])

        st.write("**RAG**")
        st.write(debug["rag"])

        st.write("**Sources**")
        st.write(debug["sources"])

        st.write("**Latency**")
        st.write(debug["latency"])

    # -------------------------
    # Guardrails
    # -------------------------

    with st.expander("🛡️ Guardrails", expanded=False):

        st.write("🟢 Customer authorization")
        st.write("🟢 Policy grounding")
        st.write("🟢 Action confirmation")
        st.write("🟢 Prompt injection protection")

    # -------------------------
    # System status
    # -------------------------

    with st.expander("🟢 System Status", expanded=False):

        st.write("🟢 Streamlit UI")
        st.write("🟡 LLM — Not connected")
        st.write("🟡 RAG — Not connected")
        st.write("🟡 Vector Database — Not connected")
        st.write("🟡 Database — Not connected")
        st.write("🟡 Tools — Mock only")
        st.write("🟡 Memory — Prototype only")


# ============================================================
# MAIN PAGE
# ============================================================

st.markdown(
    '<div class="app-title">ShopEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'AI Customer Support & Resolution Agent'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHAT AREA
# ============================================================

st.markdown(
    '<div class="chat-shell">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-header">💬 Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-subtitle">'
    'Customer ↔ AI Support Agent'
    '</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="message user-message">
                👤 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="message bot-message">
                🤖 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask your question..."
)


if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Get mock response
    response = get_mock_response(user_input)

    # Add assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Refresh UI
    st.rerun()


# ============================================================
# SOURCES
# ============================================================

st.markdown("### 📚 Sources")

sources = st.session_state.debug_info["sources"]

if sources == "None":

    st.caption("No knowledge-base sources used for the latest request.")

else:

    st.info(
        f"📄 {sources}\n\n"
        "Relevant content from this document was used for the response."
    )


# ============================================================
# CURRENT PROJECT STATUS
# ============================================================

st.divider()

st.caption(
    "Prototype mode • Backend services are not connected yet."
)