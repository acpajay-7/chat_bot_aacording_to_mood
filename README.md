
# 💜 Moodly AI — Mood-Based Chatbot

A modern AI chatbot built with **Streamlit**, **Hugging Face Transformers**, and **SmolLM2-1.7B-Instruct**. Moodly AI lets users chat with different AI personalities through a beautiful dark-themed web interface.

Choose a mood, start a conversation, and enjoy a personalized chatting experience!

## ✨ Features

- 🎭 **Multiple AI Personalities**
  - 😂 Funny Mode — jokes and playful responses.
  - 🔥 Angry Mode — dramatic and sarcastic responses.
  - 🌧️ Sad Mode — emotional and reflective responses.
  - 💜 Friendly Mode — warm and helpful conversations.

- 🎨 **Modern Streamlit UI**
  - Dark theme with gradient styling.
  - Interactive chat bubbles.
  - Sidebar for mood selection and settings.
  - Conversation history and clear-chat button.
  - Suggested prompts to start conversations.

- 🤗 **Hugging Face Integration**
  - Uses SmolLM2-1.7B-Instruct.
  - Runs inference locally on your computer.
  - No Mistral API key required.
  - Supports adjustable creativity and response length.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| Hugging Face Transformers | Loads and runs the language model |
| SmolLM2-1.7B-Instruct | Text generation |
| PyTorch | Model inference |
| uv | Python package and environment management |

## 📁 Project Structure

```text
chat_bot_mistral/
│
├── .venv/              # Virtual environment
├── ui.py                # Streamlit user interface and chatbot
├── chatbot.py           # Optional terminal chatbot
├── requirements.txt     # Python dependencies
└── README.md             # Project documentation
```

> Note: The application can run using `ui.py` alone. Keep `chatbot.py` if you also want the terminal version.

## ⚙️ Installation

### 1. Clone the repository

If your project is hosted on GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Alternatively, open your existing project directory in VS Code.

### 2. Create a virtual environment

```bash
uv venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Make sure your `requirements.txt` contains the packages required by the project.

```powershell
uv pip install -r requirements.txt
```

If you only need the main UI dependencies:

```powershell
uv pip install streamlit transformers torch
```

## 🚀 Run the Application

Start the Streamlit application:

```powershell
uv run streamlit run ui.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your browser to start chatting.

## 🤖 Model Information

**Model:** [SmolLM2-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct)

SmolLM2-1.7B-Instruct is a compact instruction-tuned language model designed for local use and lightweight applications.

The model files are downloaded from Hugging Face the first time the application runs. An internet connection is required for the initial download.

After downloading, the model can generally run offline, provided its files and dependencies are available locally.

## 🎛️ How to Use

1. Launch Moodly AI.
2. Select a personality from the sidebar.
3. Adjust response length and creativity.
4. Type a message in the chat input.
5. Read the AI response and continue the conversation.
6. Use **Clear conversation** to start fresh.
7. Switch personalities whenever you want.

## 💻 System Requirements

- Python version compatible with the installed PyTorch and Transformers packages.
- Internet connection for the initial model download.
- Sufficient RAM and disk space for the model and its dependencies.
- A supported GPU is optional; CPU inference is available but may be slower.

Performance depends on your hardware and the installed software versions.

## 🔒 Privacy

- No Mistral API key is required.
- Model inference runs locally by default.
- Chat history is maintained in the Streamlit session while the application is running.
- The model is downloaded from Hugging Face.

Local inference does not automatically mean that every part of your application is offline: the initial download and any external resources may require internet access.

## ⚠️ Limitations

- Small language models may produce inaccurate or repetitive responses.
- Personality instructions may not always be followed perfectly.
- CPU-based text generation can be slow.
- The model does not guarantee factual accuracy.

## 🔮 Future Improvements

- 💾 Persistent chat history.
- 🌗 Light and dark theme switching.
- 📥 Export conversations to TXT or PDF.
- 🎙️ Speech-to-text and text-to-speech.
- 📚 Retrieval-Augmented Generation (RAG).
- 🚀 Deployment to a suitable hosting platform.
- 🧠 Support for additional Hugging Face models.

## 👨‍💻 Author

**Ajay**

GitHub: https://github.com/acpajay-7

## 📄 License

Review the model's license and the licenses of the project's dependencies before redistributing or using the application commercially.

Model details: https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct

---

**Built with 💜 using Python, Streamlit, and Hugging Face.**
