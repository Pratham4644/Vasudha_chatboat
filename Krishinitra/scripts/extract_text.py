""

import fitz  # PyMuPDF
import os
import re
from collections import Counter
from pathlib import Path

# CONFIGURATION

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "raw_pdfs"
OUTPUT_DIR = BASE_DIR / "data" / "extracted_text"

# CLEANING FUNCTIONS

def remove_page_numbers(text: str) -> str:
    """
    Remove standalone page numbers like:
    '1'
    'Page 1'
    'Page 1 of 10'
    """
    text = re.sub(r'(?m)^\s*[Pp]age\s+\d+(\s+of\s+\d+)?\s*$', '', text)
    text = re.sub(r'(?m)^\s*\d{1,4}\s*$', '', text)
    return text


def remove_repeated_headers_footers(lines: list, threshold: int = 3) -> list:
    """
    Remove lines that repeat more than threshold times.
    These are likely headers or footers.
    """
    stripped = [l.strip() for l in lines if l.strip()]
    freq = Counter(stripped)

    cleaned_lines = []
    for line in lines:
        s = line.strip()
        if s and freq[s] > threshold:
            continue
        cleaned_lines.append(line)

    return cleaned_lines


def normalize_spacing(text: str) -> str:
    """
    - Collapse multiple spaces
    - Limit excessive blank lines
    """
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def clean_text(raw_text: str) -> str:
    """
    Safe cleaning pipeline.
    No keyword deletion.
    """
    text = remove_page_numbers(raw_text)

    lines = text.splitlines()
    lines = remove_repeated_headers_footers(lines)

    text = "\n".join(lines)
    text = normalize_spacing(text)

    return text


# EXTRACTION FUNCTION

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text page by page using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    all_pages_text = []

    for page_number, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")

        if not raw_text.strip():
            print(f"   Warning: Page {page_number} is empty or image-based")
            continue

        cleaned = clean_text(raw_text)

        if cleaned:
            all_pages_text.append(cleaned)

    doc.close()

    return "\n\n".join(all_pages_text)


# MAIN PIPELINE

def run_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    pdf_files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print(f"No PDF files found in '{INPUT_DIR}'")
        return

    print(f"Found {len(pdf_files)} PDF(s)\n")

    success_count = 0
    fail_count = 0
    total_words = 0

    for pdf_file in pdf_files:
        pdf_path = INPUT_DIR / pdf_file
        txt_filename = os.path.splitext(pdf_file)[0] + ".txt"
        txt_path = OUTPUT_DIR / txt_filename

        print(f"Processing: {pdf_file}")

        try:
            extracted_text = extract_text_from_pdf(pdf_path)

            if not extracted_text.strip():
                print("   No readable text extracted. Possibly scanned PDF.\n")
                fail_count += 1
                continue

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)

            word_count = len(extracted_text.split())
            total_words += word_count

            print(f"   Saved -> {txt_filename} ({word_count} words)\n")
            success_count += 1

        except Exception as e:
            print(f"   Failed: {e}\n")
            fail_count += 1

    print("--------------------")
    print(f"Success files : {success_count}")
    print(f"Failed files  : {fail_count}")

    if success_count > 0:
        avg_words = total_words // success_count
        print(f"Average words per file: {avg_words}")

    print(f"Output folder: {OUTPUT_DIR}{os.sep}")


if __name__ == "__main__":
    run_pipeline()
