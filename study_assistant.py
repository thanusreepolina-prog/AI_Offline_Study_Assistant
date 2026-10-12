import tkinter as tk
from tkinter import messagebox

def get_answer():
    question = question_entry.get().lower().strip()

    if not question:
        messagebox.showwarning("Warning", "Please enter a question.")
    elif "python" in question:
        answer_label.config(
            text="Python is a programming language."
        )
    elif "artificial intelligence" in question or "ai" in question:
        answer_label.config(
            text="Artificial Intelligence helps computers perform tasks."
        )
    elif "exam" in question or "student" in question:
        answer_label.config(
            text="Students can use study notes to prepare for exams."
        )
    else:
        answer_label.config(
            text="Sorry, I could not find an answer."
        )

window = tk.Tk()
window.title("AI Offline Study Assistant")
window.geometry("500x350")

heading = tk.Label(
    window,
    text="AI Offline Study Assistant",
    font=("Arial", 16, "bold")
)
heading.pack(pady=20)

question_entry = tk.Entry(window, width=45)
question_entry.pack(pady=10)

ask_button = tk.Button(
    window,
    text="Ask Question",
    command=get_answer
)
ask_button.pack(pady=10)

answer_label = tk.Label(
    window,
    text="Your answer will appear here.",
    wraplength=420
)
answer_label.pack(pady=20)

window.mainloop()