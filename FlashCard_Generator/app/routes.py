
import os, shutil
from dotenv import load_dotenv; load_dotenv()

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from together import Together
from PyPDF2 import PdfReader   # simple PDF text extractor

main = Blueprint("main", __name__)

# ---------- Together client ---------- #
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))  # ensure .env has the key
CHAT_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"  # must be a valid slug

# ---------- helpers ---------- #
def pdf_to_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def generate_flashcards(text: str):
    """Ask Together.ai to create 10–15 flashcards and parse them into a list of dicts."""
    prompt = (
    "Generate 10–15 flashcards from the following content. "
    "Each flashcard should have:\n"
    "- A question (Q)\n"
    "- A concise and correct answer (A)\n"
    "- A difficulty level: Easy, Medium, or Hard\n\n"
    f"{text[:2000]}\n\n"
    "Format:\nQ1: ...\nA1: ...\nDifficulty1: ...\nQ2: ...\nA2: ...\nDifficulty2: ..."
)
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful flashcard generator."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,  # increased for longer response
        )
        import re

        raw_output = resp.choices[0].message.content.strip()

        # Parse flashcards in Q/A/Difficulty format
        pattern = r"Q\d+:\s*(.*?)\nA\d+:\s*(.*?)\nDifficulty\d+:\s*(.*?)(?=\nQ\d+:|$)"
        matches = re.findall(pattern, raw_output, re.DOTALL)

        cards = [{"question": q.strip(), "answer": a.strip(), "difficulty": d.strip()} for q, a, d in matches]
        return cards
   
    except Exception as e:
        return [{"question": "Error", "answer": f"API error: {e}"}]

    # ---- Parse Q/A pairs ---- #
    # flashcards = []
    # q, a = "", ""
    # for line in raw.splitlines():
    #     line = line.strip()
    #     if line.lower().startswith("q"):
    #         q = line.split(":", 1)[1].strip()
    #     elif line.lower().startswith("a"):
    #         a = line.split(":", 1)[1].strip()
    #     elif line.lower().startswith("difficulty"):
    #         difficulty = line.split(":", 1)[1].strip()
    #         if q and a:
    #             flashcards.append({"question": q, "answer": a, "difficulty": difficulty})
    #             q, a = "", ""

    # return flashcards

# ---------- routes ---------- #
@main.route("/")
def index():
    return render_template("index.html", flashcards=[])

@main.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text_input", "").strip()
    file = request.files.get("file_input")

    # ---------- handle file upload ---------- #
    if file and file.filename:
        upload_dir = "temp"
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, secure_filename(file.filename))
        file.save(path)

        if path.lower().endswith(".pdf"):
            text = pdf_to_text(path)
        elif path.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
        shutil.rmtree(upload_dir)                   # clean temp folder

    # ---------- guard‑rail: no text ---------- #
    if not text:
        return render_template("index.html", flashcards=[{
            "question": "⚠️  No content provided.",
            "answer":   "Please paste text or upload a .txt/.pdf file."
        }])

    flashcards = generate_flashcards(text)
    return render_template("index.html", flashcards=flashcards)



# from together import Together
# from flask import Blueprint

# main = Blueprint('main', __name__)
# client = Together(api_key=os.getenv("TOGETHER_API_KEY"))  # Replace with your actual API key
# @main.route('/models')
# def show_models():
#     try:
#         models = client.models.list()

#         # Inspecting full model objects
#         model_names = []
#         for model in models:
#             if hasattr(model, "id"):
#                 model_names.append(model.id)
#             elif isinstance(model, dict) and "name" in model:
#                 model_names.append(model["name"])
#             else:
#                 model_names.append(str(model))  # fallback

#         return "<br>".join(model_names)

#     except Exception as e:
#         return f"Error listing models: {str(e)}"
