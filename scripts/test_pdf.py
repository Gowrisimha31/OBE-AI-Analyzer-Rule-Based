from pdf_extractor import extract_questions

questions = extract_questions(
    "dataset/raw_extracted/qp1.pdf"
)

for q in questions:
    print(q)