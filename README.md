# AI Text Assistant 🤖

An AI-powered text assistant built using **Python, Streamlit, and Google Gemini API**. It helps users summarize, rewrite, and explain text with customizable response tones and output lengths.

## 🚀 Features

- **Text Summarization:** Generate concise summaries from lengthy text.
- **Text Rewriting:** Rewrite content in clear and natural English.
- **Text Explanation:** Understand complex text through simple explanations.
- **Tone Selection:** Choose Professional, Casual, or Friendly tone.
- **Output Length:** Select Short, Medium, or Detailed responses.
- **Copy Response:** Easily copy generated AI responses.
- **Generation History:** View previous generated responses during the session.
- **Input Validation:** Validate empty and short text inputs.
- **Error Handling:** Handle API and application errors.
- **Loading Indicator:** Display a loading message during AI generation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Google Gemini API | AI text generation |
| Google Gen AI SDK | Gemini API integration |
| python-dotenv | Environment variable management |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
ai-text-assistant/
│
├── main.py
├── requirements.txt
├── interview.txt
├── README.md
├── .gitignore
└── .env (not uploaded)
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/pallavithulkar/ai-text-assistant.git
```

### 2. Navigate to the project folder

```bash
cd ai-text-assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

**Important:** Never upload your `.env` file or expose your API key publicly.

### 7. Run the application

```bash
streamlit run main.py
```

The application will open in your browser.

## 🧠 How It Works

1. The user selects an AI task.
2. The user chooses a response tone and output length.
3. The user enters text.
4. The application builds a dynamic prompt.
5. The prompt is sent to the Gemini API.
6. Gemini generates a response.
7. The application displays the result and stores it in session history.

## 🔮 Future Improvements

- Persistent chat history using a database.
- User authentication.
- React-based frontend.
- FastAPI backend integration.
- Deployment and production improvements.

## 👩‍💻 Author

**Pallavi Thulkar**

GitHub: [@pallavithulkar](https://github.com/pallavithulkar)

---

⭐ If you find this project useful, consider giving it a star!