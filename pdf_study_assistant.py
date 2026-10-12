import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import filedialog
from pypdf import PdfReader
import json
import urllib.request
import urllib.error
project_folder = Path(__file__).parent
pdf_path = None

notes=""
def ask_ollama(question, pdf_notes):
    prompt = f"""
You are an offline study assistant.
Answer the student's question using only the PDF notes below.
If the answer is not in the notes, say:
"I could not find the answer in the selected PDF."

PDF NOTES:
{pdf_notes[:12000]}

QUESTION:
{question}
"""

    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result.get("response", "No answer returned.")

    except urllib.error.URLError as error:
        return f"Could not connect to Ollama: {error}"
    except Exception as error:
        return f"AI error: {error}"
def browse_pdf():
    global notes, pdf_path

    selected_file = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if selected_file:
        try:
            reader = PdfReader(selected_file)
            notes = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            pdf_path = Path(selected_file)
            pdf_label.config(text=f"Selected PDF: {pdf_path.name}")
            answer_label.config(
                text="PDF loaded successfully! Ask a question."
            )
        except Exception as error:
            messagebox.showerror(
                "PDF Error",
                f"Could not read PDF: {error}"
            )
def clear_question():
    question_entry.delete(0, tk.END)
    answer_label.config(
        text="Ask a question about your PDF notes."
    )
def get_answer():
    question = question_entry.get().strip()

    if not pdf_path:
        messagebox.showwarning(
            "Warning", "Please select a PDF first."
        )
        return

    if not notes.strip():
        answer_label.config(text="Could not read the PDF notes.")
        return

    if not question:
        messagebox.showwarning(
            "Warning", "Please enter a question."
        )
        return

    answer_label.config(text="AI is thinking... Please wait.")
    window.update_idletasks()

    answer = ask_ollama(question, notes)
    answer_label.config(text=f"Answer: {answer}")
window = tk.Tk()
window.title("PDF Study Assistant")
window.geometry("520x550")

tk.Label(
    window,
    text="PDF Study Assistant",
    font=("Arial", 16, "bold")
).pack(pady=20)

question_entry = tk.Entry(window, width=50)
question_entry.pack(pady=10)
tk.Button(
    window,
    text="Browse PDF",
    command=browse_pdf
).pack(pady=10)
tk.Button(
    window,
    text="Ask Question",
    command=get_answer
).pack(pady=10)

answer_label = tk.Label(
    window,
    text="Ask a question about your PDF notes.",
    wraplength=460
)
answer_label.pack(pady=20)
pdf_label = tk.Label(
    window,
    text="No PDF selected",
    wraplength=460
)
pdf_label.pack(pady=5)
def show_pdf_notes():
    notes_window = tk.Toplevel(window)
    notes_window.title("PDF Study Notes")
    notes_window.geometry("600x450")

    text_area = tk.Text(notes_window, wrap="word")
    text_area.pack(fill="both", expand=True, padx=10, pady=10)

    text_area.insert("1.0", notes if notes else "No PDF notes available.")
    text_area.config(state="disabled")
tk.Button(
    window,
    text="Show PDF Notes",
    command=show_pdf_notes
).pack(pady=10)
tk.Button(
    window,
    text="Clear Question",
    command=clear_question
).pack(pady=10)
window.mainloop()