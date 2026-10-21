
import streamlit as st
from transformers import pipeline
import torch

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Moodly AI | Your Mood Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: radial-gradient(ellipse at top left, #202044 0%, #10111b 45%, #090b12 100%);
    color: #f4f4ff;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg, #29274e, #191b31 65%, #252044);
    border: 1px solid rgba(167,139,250,.25);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 24px;
    box-shadow: 0 15px 50px rgba(0,0,0,.20);
}

.eyebrow {
    color: #b9a5ff;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 800;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 48px);
    font-weight: 800;
    margin: 8px 0;
    color: #ffffff;
}

.hero p {
    color: #c6c7df;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 0;
}

.status {
    display: inline-block;
    background: rgba(74,222,128,.12);
    color: #86efac;
    border: 1px solid rgba(74,222,128,.3);
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 12px;
    margin-top: 16px;
}

section[data-testid="stSidebar"] {
    background: #111320;
    border-right: 1px solid #282a40;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e9e6ff;
}

div[data-testid="stChatMessage"] {
    background: rgba(28,30,49,.8);
    border: 1px solid rgba(160,160,210,.12);
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
}

div[data-testid="stChatInput"] {
    border: 1px solid #6554a5;
    border-radius: 18px;
    background: #171827;
}

div[data-testid="stChatInput"] textarea {
    color: white;
}

.stButton > button {
    border-radius: 12px;
    border: 1px solid #5c4a94;
    background: linear-gradient(135deg, #7557dc, #5942a8);
    color: white;
    font-weight: 600;
    min-height: 42px;
    transition: .2s ease;
}

.stButton > button:hover {
    border-color: #b9a5ff;
    color: white;
    transform: translateY(-1px);
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

.small-note {
    color: #9295b3;
    font-size: 12px;
    line-height: 1.6;
}

div[data-testid="stMarkdownContainer"] p {
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


# ---------------- MODEL ----------------
MODEL_NAME = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

@st.cache_resource(show_spinner=False)
def load_chatbot():
    device = 0 if torch.cuda.is_available() else -1

    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        device=device,
    )


# ---------------- MOOD SETTINGS ----------------
MOODS = {
    "😊 Funny": {
        "key": "funny",
        "emoji": "😂",
        "description": "Jokes, playful replies and good vibes.",
        "color": "#fbbf24",
        "prompt": (
            "You are Moodly, a funny and playful chatbot. "
            "Use light humor, witty responses, and occasional jokes. "
            "Stay helpful and answer the user's actual question."
        ),
    },
    "😠 Angry": {
        "key": "angry",
        "emoji": "🔥",
        "description": "Dramatic, grumpy and sarcastic replies.",
        "color": "#fb7185",
        "prompt": (
            "You are Moodly, a comically angry and grumpy chatbot. "
            "Use exaggerated frustration and playful sarcasm, "
            "but never threaten or genuinely insult the user. "
            "Still answer questions helpfully."
        ),
    },
    "🥹 Sad": {
        "key": "sad",
        "emoji": "🌧️",
        "description": "Soft, emotional and thoughtful responses.",
        "color": "#93c5fd",
        "prompt": (
            "You are Moodly, a gentle, sad and emotional chatbot. "
            "Use a soft, reflective and slightly melancholic tone. "
            "Remain supportive, clear, and helpful."
        ),
    },
    "✨ Friendly": {
        "key": "friendly",
        "emoji": "💜",
        "description": "Warm, calm and helpful conversations.",
        "color": "#c4b5fd",
        "prompt": (
            "You are Moodly, a friendly and supportive chatbot. "
            "Be warm, clear, conversational and helpful."
        ),
    },
}


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_mood" not in st.session_state:
    st.session_state.active_mood = "😊 Funny"


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 💜 Moodly AI")
    st.caption("Your conversation, your mood.")
    st.divider()

    st.markdown("### 🎭 Choose your mood")

    selected_mood = st.radio(
        "Chat personality",
        options=list(MOODS.keys()),
        index=list(MOODS.keys()).index(
            st.session_state.active_mood
        ),
        label_visibility="collapsed",
    )

    if selected_mood != st.session_state.active_mood:
        st.session_state.active_mood = selected_mood
        st.session_state.messages = []
        st.rerun()

    mood = MOODS[selected_mood]

    st.markdown(
        f"""
        <div style="
            background:#1c1d30;
            border:1px solid {mood['color']}66;
            border-radius:16px;
            padding:16px;
            margin-top:8px;
        ">
            <div style="font-size:28px">{mood['emoji']}</div>
            <div style="font-size:17px;font-weight:700;margin:8px 0">
                {selected_mood}
            </div>
            <div style="font-size:13px;color:#b7bad1;line-height:1.6">
                {mood['description']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### ⚙️ Response settings")

    max_tokens = st.slider(
        "Response length",
        min_value=50,
        max_value=300,
        value=150,
        step=25,
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.1,
        max_value=1.2,
        value=0.8,
        step=0.1,
    )

    st.caption("Higher creativity produces more varied responses.")

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="small-note">
            MODEL<br>
            SmolLM2-1.7B-Instruct<br><br>
            RUNNING MODE<br>
            Local inference on your computer<br><br>
            API KEY<br>
            Not required
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- HERO HEADER ----------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ Your personal AI companion</div>
        <h1>Every mood has a voice.</h1>
        <p>
            One chatbot. Different personalities. Endless conversations.
            Choose your mood and let the conversation begin.
        </p>
        <div class="status">● Local model · No API key required</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- CHAT HEADER ----------------
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"### {mood['emoji']} Chatting in {selected_mood} mode")

with col2:
    st.markdown(
        f"<div style='text-align:right;color:#aaa9c5;"
        f"padding-top:12px;font-size:13px'>"
        f"💬 {len(st.session_state.messages)} messages</div>",
        unsafe_allow_html=True,
    )

# ---------------- WELCOME MESSAGE ----------------
if not st.session_state.messages:
    st.markdown(
        """
        <div style="
            text-align:center;
            padding:35px 15px 25px;
            background:rgba(30,31,51,.48);
            border:1px dashed #41405f;
            border-radius:20px;
            margin:12px 0 22px;
        ">
            <div style="font-size:42px">💬</div>
            <h3 style="color:#f4f1ff;margin:10px 0">
                Your next conversation starts here
            </h3>
            <p style="color:#aaa9c5">
                Say hello, ask a question, or try one of the prompts below.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        "Tell me a joke 😂",
        "Motivate me today ✨",
        "How was your day?",
    ]

    suggestion_cols = st.columns(3)

    for i, suggestion in enumerate(suggestions):
        with suggestion_cols[i]:
            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_prompt = suggestion
                st.rerun()


# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Type your message here...")

if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")


# ---------------- GENERATE RESPONSE ----------------
if prompt:
    if prompt.strip() == "":
        st.stop()

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner(f"{mood['emoji']} Moodly is thinking..."):
            model = load_chatbot()

            conversation = [
                {
                    "role": "system",
                    "content": mood["prompt"],
                }
            ]

            # Keep recent conversation history for context.
            conversation.extend(
                st.session_state.messages[-12:]
            )

            result = model(
                conversation,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=temperature,
                return_full_text=True,
            )

            generated = result[0]["generated_text"]

            # Chat-formatted generation returns a list of messages.
            if isinstance(generated, list):
                reply = generated[-1]["content"]
            else:
                reply = str(generated)

            reply = reply.strip()

            if not reply:
                reply = "I couldn't generate a reply. Please try again."

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as error:
        st.error(
            "Something went wrong while generating the response. "
            "Check your internet connection for the initial model "
            "download and check your installed packages."
        )
        with st.expander("Technical details"):
            st.code(str(error))

        # Remove the unanswered user message so it can be retried.
        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"] == "user"
        ):
            st.session_state.messages.pop()


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#777a99;font-size:12px">
        Made with 💜 using Streamlit & Hugging Face Transformers
        <br>Responses are generated locally and may occasionally be inaccurate.
    </div>
    """,
    unsafe_allow_html=True,
)
