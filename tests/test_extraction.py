
from pathlib import Path
import json
import fitz  # PyMuPDF

DATA_DIR = Path("data")
PDF_DIR = DATA_DIR / "pdfs"
BENCHMARK = DATA_DIR / "financebench_open_source.jsonl"

# Load the benchmark questions.
with BENCHMARK.open("r", encoding="utf-8") as f:
    questions = [json.loads(line) for line in f if line.strip()]

print(f"Loaded {len(questions)} benchmark questions.\n")


# Inspect the actual document identifiers in FinanceBench
for company in ["AMD", "PEPSICO"]:
    matches = [
        q for q in questions
        if company in str(q.get("doc_name", "")).upper()
    ]

    print(f"\n{company} questions found: {len(matches)}")

    for q in matches[:10]:
        print("Document:", repr(q.get("doc_name")))
        print("Question:", q.get("question"))
        print()


for name in ["AMD_2022_10K", "PEPSICO_2022_10K"]:
    pdf_path = PDF_DIR / f"{name}.pdf"

    with fitz.open(pdf_path) as pdf:
        print(f"\nDOCUMENT: {name}")
        print(f"Pages: {len(pdf)}")

        # Check that Python can extract text.
        first_page = pdf[0].get_text("text")
        print(f"First page extracted: {len(first_page)} characters")

        # Questions associated with this document.
        matching = [
            q for q in questions
            if q.get("doc_name") == name
        ]

        print(f"Benchmark questions: {len(matching)}")

        # Use the first question with usable evidence.
        selected = next(
            (
                q for q in matching
                if any(
                    e.get("evidence_text")
                    and isinstance(e.get("evidence_page_num"), int)
                    for e in q.get("evidence", [])
                )
            ),
            None,
        )

        if selected is None:
            print("No suitable benchmark question found.")
            continue

        print("\nQuestion:", selected["question"])
        print("Reference answer:", selected["answer"])

        for evidence in selected["evidence"]:
            page_num = evidence.get("evidence_page_num")
            expected = evidence.get("evidence_text", "")

            if not isinstance(page_num, int) or not expected:
                continue

            if not 0 <= page_num < len(pdf):
                print("Invalid evidence page:", page_num)
                continue

            extracted = pdf[page_num].get_text("text")

            # Normalize whitespace for PDF line wrapping.
            normalize = lambda s: " ".join(s.split()).lower()

            exact_match = normalize(expected) in normalize(extracted)

            print(f"\nEvidence PDF page index: {page_num}")
            print("Exact normalized evidence match:", exact_match)
            print("Annotated evidence:", expected[:400])
            print("Extracted page sample:", extracted[:400])
