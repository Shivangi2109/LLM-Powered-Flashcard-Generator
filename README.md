# 🧠 LLM-Powered Flashcard Generator

This is a lightweight, LLM-powered flashcard generation web app built with **Flask** and integrated with **Together.ai's LLM (DeepSeek-R1-LLaMA)**. It extracts educational content from `.pdf` or `.txt` files and generates 10–15 **question-answer flashcards** with difficulty levels (Easy/Medium/Hard) using natural language understanding.

---

## 🚀 Features

- 🔍 Accepts raw text or educational files (PDF/TXT)
- 🧠 Generates 10–15 flashcards per input
- 🧾 Adds difficulty levels to each flashcard (Easy/Medium/Hard)
- 💬 Powered by Together.ai's open LLMs
- 🌗 Light/Dark mode toggle for better accessibility
- 🌐 Clean Flask web interface (no Streamlit)
- 🧼 Auto-deletes temporary files for clean deployment

---

## 📁 Project Structure

```bash
FLASHCARD_GENERATOR/
│
├── .venv/ # Virtual environment
├── .env # Your Together API key 
├── run.py # Flask app entry point
├── requirements.txt
│
├── app/
│ ├── init.py # Initializes Flask app
│ ├── routes.py # All route logic and flashcard generation
│ ├── templates/
│ │ └── index.html # Main frontend HTML
│ └── temp_uploads/ # Stores temporary uploaded files (auto-deleted)
 ```

---
# Output



---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/flashcard-generator.git
cd flashcard-generator
```

### 2. Create a virtual environment
```bash
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```
### 3. Install the Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the API Key
```bash
#Create a .env file in the project root and add your API key:
TOGETHER_API_KEY=your_together_api_key_here
```

### 5.Run the Flask App
```bash
python run.py
# Open your browser and visit : http://localhost:5000
```







