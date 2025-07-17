import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import google.generativeai as genai

# === CONFIG ===
GEMINI_API_KEY = "AIzaSyAQtqr6t6FynIriiXFrEv6hRpE6fuXlUk8"
PDF_PATH = r'D:\python projects\DSA\Major_project\diploma memo.pdf'
POPPLER_PATH = r"C:\poppler\poppler-24.08.0\Library\bin"

# === SETUP GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# === TEXT EXTRACTION ===
def extract_text_from_pdf(pdf_path):
    print("[*] Converting PDF to images and extracting text...")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    full_text = ''
    for i, page in enumerate(pages):
        gray = page.convert('L')
        text = pytesseract.image_to_string(gray, lang='eng')
        full_text += f"\n\n--- Page {i+1} ---\n{text}"
    return full_text

# === GEMINI CALL ===
def call_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Gemini API error:", e)
        return "Error generating response."

# === SAVE TO FILE ===
def save_summary(text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[+] Summary saved to: {filename}")

# === CHAT LOOP ===
def chatbot_loop(context_text):
    print("\n🧠 Chatbot ready! Ask about the document or type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        prompt = f"""You are an AI assistant. Read the following document and answer the user's question.\n\nDocument:\n{context_text[:25000]}\n\nQuestion: {user_input}\nAnswer:"""
        answer = call_gemini(prompt)
        print("AI:", answer)

# === MAIN ===
if __name__ == "__main__":
    doc_text = extract_text_from_pdf(PDF_PATH)

    print("[*] Generating English summary...")
    summary_en = call_gemini(f"Summarize the following document in English:\n\n{doc_text[:25000]}")
    save_summary(summary_en, "summary_en.txt")

    print("[*] Generating Telugu summary...")
    summary_te = call_gemini(f"Summarize the following document in Telugu:\n\n{doc_text[:25000]}")
    save_summary(summary_te, "summary_te.txt")

    chatbot_loop(doc_text)
