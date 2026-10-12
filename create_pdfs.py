from pathlib import Path
from reportlab.pdfgen import canvas

# Project folder
project_folder = Path(__file__).resolve().parent

# Input text file and output folder
text_file = project_folder / "study_notes.txt"
pdf_folder = project_folder / "pdf_output"
pdf_file = pdf_folder / "study_notes.pdf"

# Check input file
if not text_file.is_file():
    print("ERROR: study_notes.txt was not found.")
else:
    try:
        # Create the PDF folder if needed
        pdf_folder.mkdir(parents=True, exist_ok=True)

        pdf = canvas.Canvas(str(pdf_file))
        y = 800

        with text_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Start a new page if needed
                if y < 60:
                    pdf.showPage()
                    y = 800

                pdf.drawString(60, y, line[:100])
                y -= 25

        pdf.save()

        print("PDF created successfully!")
        print(f"Saved at: {pdf_file}")

    except Exception as error:
        print(f"ERROR: {error}")