import sys
import json
import html
import re
import streamlit as st

from agent.core import run_agent


# =========================================================
# UTF-8 ENCODING FIX
# =========================================================

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Desktop Assistant",
    page_icon="⚡",
    layout="wide"
)


# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a;
        color: white;
        border-right: 1px solid #1e293b;
    }

    .main-chat-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
    }

    .chat-bubble {
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        max-width: 85%;
        line-height: 1.6;
        font-size: 14px;
        word-wrap: break-word;
        overflow-wrap: break-word;
        animation: fadeIn 0.3s ease-in;
    }

    .user-bubble {
        background-color: #ffffff;
        color: #1e293b;
        align-self: flex-end;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    .assistant-bubble {
        background-color: #f8fafc;
        color: #334155;
        align-self: flex-start;
        border-left: 4px solid #3b82f6;
    }

    @keyframes fadeIn {

        from {
            opacity: 0;
            transform: translateY(5px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SAFE TEXT CLEANER
# =========================================================

def safe_text(text):

    if not isinstance(text, str):
        text = str(text)

    text = text.replace("→", "->")

    text = re.sub(
        r'\x1b\[[0-9;]*[a-zA-Z]',
        '',
        text
    )

    text = re.sub(
        r'<[^>]+>',
        '',
        text
    )

    text = re.sub(
        r'```json|```',
        '',
        text
    )

    text = text.encode(
        "utf-8",
        "ignore"
    ).decode("utf-8")

    return text.strip()


# =========================================================
# RESPONSE PARSER
# =========================================================

def parse_response(raw_response):

    if not isinstance(raw_response, str):
        return str(raw_response)

    stripped = raw_response.strip()

    try:

        parsed = json.loads(stripped)

        if isinstance(parsed, dict):

            for key in (
                "content",
                "answer",
                "message",
                "text",
                "result",
                "output"
            ):

                if key in parsed and isinstance(parsed[key], str):
                    return parsed[key].strip()

            values = [
                v for v in parsed.values()
                if isinstance(v, str)
            ]

            if values:
                return " ".join(values).strip()

    except (json.JSONDecodeError, TypeError):
        pass

    start = stripped.find("{")
    end = stripped.rfind("}")

    if start != -1 and end != -1 and end > start:

        try:

            parsed = json.loads(
                stripped[start:end + 1]
            )

            if isinstance(parsed, dict):

                for key in (
                    "content",
                    "answer",
                    "message",
                    "text",
                    "result",
                    "output"
                ):

                    if key in parsed and isinstance(parsed[key], str):
                        return parsed[key].strip()

        except:
            pass

    return raw_response


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "<h1 style='font-size:22px;'>⚡ Desktop Assistant</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#94a3b8; font-size:13px;'>Active Terminal Session</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 📡 System Info")

    st.caption("OS: Windows / Linux / macOS")
    st.caption("Status: Connected")

    if st.button(
        "Reset Environment",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.rerun()


# =========================================================
# MAIN INTERFACE
# =========================================================

st.markdown("## Workspace")

st.markdown(
    "<p style='color:#64748b;'>Control your local environment via natural language.</p>",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================================
# CHAT AREA
# =========================================================

chat_placeholder = st.container()

with chat_placeholder:

    for chat in st.session_state.chat_history:

        role_class = (
            "user-bubble"
            if chat["role"] == "user"
            else "assistant-bubble"
        )

        safe_content = safe_text(chat["content"])

        safe_content = html.escape(safe_content)

        safe_content = safe_content.replace(
            "\n",
            "<br>"
        )

        st.markdown(f"""
            <div style="display:flex; flex-direction:column;">
                <div class="chat-bubble {role_class}">
                    <b>{"You" if chat["role"] == "user" else "Assistant"}</b>
                    <br><br>
                    {safe_content}
                </div>
            </div>
        """, unsafe_allow_html=True)


# =========================================================
# INPUT AREA
# =========================================================

if prompt := st.chat_input(
    "Enter a system command (e.g., 'Open Chrome')"
):

    st.session_state.chat_history.append({
        "role": "user",
        "content": safe_text(prompt)
    })

    with st.spinner("Processing request..."):

        try:

            raw_response = run_agent(prompt)

            response = parse_response(raw_response)

            response = safe_text(response)

        except Exception as e:

            response = f"Critical Error: {str(e)}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()