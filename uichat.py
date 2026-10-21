
import streamlit as st
import torch
from transformers import pipeline

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Moodly AI | Your Mood Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(
            ellipse at top left,
            #202044 0%, #10111b 45%, #090b12 100%
        );
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
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Smaller model for testing on resource-limited cloud servers.
MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"


@st.cache_resource(show_spinner=False)
def load_chatbot():
    """
    Load the model once and reuse it across Streamlit reruns.
    """
    device = 0 if torch.cuda.is_available() else -1

    chatbot = pipeline(
        task="text-generation",
        model=MODEL_NAME,
        device=device,
    )

    return chatbot


def generate_reply(model, conversation, max_tokens, temperature):
    """
    Generate a response from the chat messages and extract
    the assistant's reply.
    """
    result = model(
        conversation,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=temperature,
        return_full_text=False,
    )

    generated = result[0]["generated_text"]

    # Chat-template pipelines can return message dictionaries.
    if isinstance(generated, list):
        assistant_messages = [
            message
            for message in generated
            if isinstance(message, dict)
            and message.get("role") == "assistant"
        ]

        if assistant_messages:
            reply = assistant_messages[-1].get("content", "")
        elif generated and isinstance(generated[-1], dict):
            reply = generated[-1].get("content", "")
        else:
            reply = ""

    else:
        reply = str(generated)

    return reply.strip()


# ============================================================
# MOOD CONFIGURATION
# ============================================================

MOODS = {
    "😊 Funny": {
        "key": "funny",
        "emoji": "😂",
        "description": "Jokes, playful replies and good vibes.",
        "color": "#fbbf24",
        "prompt": (
            "You are Moodly, a funny and playful chatbot. "
            "Use light humor, witty responses, and occasional jokes. "
            "Answer the user's actual question helpfully. "
            "Keep responses natural and reasonably concise."
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
            "Remain helpful and answer the actual question."
        ),
    },
    "🥹 Sad": {
        "key": "sad",
        "emoji": "🌧️",
        "description": "Soft, emotional and thoughtful responses.",
        "color": "#93c5fd",
        "prompt": (
            "You are Moodly, a gentle and reflective chatbot. "
            "Use a soft, thoughtful and slightly melancholic tone. "
            "Remain supportive, clear and helpful."
        ),
    },
    "✨ Friendly": {
        "key": "friendly",
        "emoji": "💜",
        "description": "Warm, calm and helpful conversations.",
        "color": "#c4b5fd",
        "prompt": (
            "You are Moodly, a friendly and supportive chatbot. "
            "Be warm, clear, conversational and helpful. "
            "Answer questions directly in a natural tone."
        ),
    },
}

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_mood" not in st.session_state:
    st.session_state.active_mood = "😊 Funny"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 💜 Moodly AI")
    st.caption("Your conversation, your mood.")
    st.divider()

    st.markdown("### 🎭 Choose your mood")

    mood_options = list(MOODS.keys())

    selected_mood = st.radio(
        "Chat personality",
        options=mood_options,
        index=mood_options.index(
            st.session_state.active_mood
        ),
        label_visibility="collapsed",
    )

    # Clear the conversation when the personality changes.
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
        value=100,
        step=25,
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.1,
        max_value=1.2,
        value=0.7,
        step=0.1,
    )

    st.caption(
        "Higher creativity can produce more varied responses."
    )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        f"""
        <div class="small-note">
            MODEL<br>
            SmolLM2-135M-Instruct<br><br>
            RUNNING MODE<br>
            Cloud CPU/GPU inference<br><br>
            API KEY<br>
            Not required
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ Your personal AI companion</div>
        <h1>Every mood has a voice.</h1>
        <p>
            One chatbot. Different personalities. Endless conversations.
            Choose your mood and let the conversation begin.
        </p>
        <div class="status">● Cloud model · No API key required</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CHAT HEADER
# ============================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(
        f"### {mood['emoji']} Chatting in {selected_mood} mode"
    )

with col2:
    st.markdown(
        f"""
        <div style="
            text-align:right;
            color:#aaa9c5;
            padding-top:12px;
            font-size:13px;
        ">
            💬 {len(st.session_state.messages)} messages
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# WELCOME SCREEN AND SUGGESTED PROMPTS
# ============================================================

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
            if st.button(
                suggestion,
                use_container_width=True,
                key=f"suggestion_{i}",
            ):
                st.session_state.pending_prompt = suggestion
                st.rerun()

# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input("Type your message here...")

# Handle a suggested prompt button click.
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

# ============================================================
# GENERATE RESPONSE
# ============================================================

if prompt and prompt.strip():
    prompt = prompt.strip()

    # Store and display the user's message.
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner(
            f"{mood['emoji']} Moodly is thinking..."
        ):
            # Load the model when the first response is requested.
            model = load_chatbot()

            # Include the mood instructions and recent chat history.
            conversation = [
                {
                    "role": "system",
                    "content": mood["prompt"],
                }
            ]

            conversation.extend(
                st.session_state.messages[-12:]
            )

            # Generate and extract the response.
            reply = generate_reply(
                model=model,
                conversation=conversation,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            if not reply:
                reply = (
                    "I couldn't generate a reply this time. "
                    "Please try a different message."
                )

        # Save the assistant's response.
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as error:
        st.error(
            "Moodly couldn't generate a response. "
            "Please try again or check the deployment logs."
        )

        with st.expander("Technical details"):
            st.code(str(error))

        # Remove the unanswered user message so it can be retried.
        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"] == "user"
        ):
            st.session_state.messages.pop()

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777a99;
        font-size:12px;
    ">
        Made with 💜 using Streamlit & Hugging Face Transformers
        <br>
        Responses are generated by a language model and may occasionally
        be inaccurate.
    </div>
    """,
    unsafe_allow_html=True,
)
