from pathlib import Path
from pypdf import PdfReader
project_folder = Path(__file__).parent
pdf_path = project_folder / "pdf_output" / "study_notes.pdf"
reader = PdfReader(str(pdf_path))
for page in reader.pages:
    text = page.extract_text()
    if text:
        print(text)
        print("\n--- Important Study Keywords ---")

keywords = [
    "Python",
    "Artificial Intelligence",
    "computers",
    "students",
    "exams"
]

for word in keywords:
    if word.lower() in text.lower():
        print(word)
        print("\n--- Study Notes Summary ---")

sentences = [s.strip() for s in text.split(".") if s.strip()]

for sentence in sentences[:3]:
    print(sentence + ".")
    print("\n--- Ask Your Study Notes ---")
print("\n--- Ask Your Study Notes ---")

while True:
    question = input(
        "Ask a question (or type 'exit' to stop): "
    ).lower()

    if question == "exit":
        print("Study Assistant closed. Goodbye!")
        break

    elif "python" in question:
        print("Answer: Python is a programming language.")

    elif "artificial intelligence" in question or "ai" in question:
        print("Answer: Artificial Intelligence helps computers perform tasks.")

    elif "exam" in question or "student" in question:
        print("Answer: Students can use study notes to prepare for exams.")

    else:
        print("Sorry, I could not find an answer in my basic question list.")