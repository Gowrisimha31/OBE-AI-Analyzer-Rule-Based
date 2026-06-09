import pdfplumber
import re


def extract_questions(pdf_path):

    questions = []

    with pdfplumber.open(pdf_path) as pdf:

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += "\n" + page_text

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) < 10:
            continue

        if re.match(r"^\d+[\.\)]", line):
            questions.append(line)

        elif re.match(r"^Q[\.\s]?\d+", line, re.IGNORECASE):
            questions.append(line)

    return questions