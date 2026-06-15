"""
chunk_data.py
- Section filtering (removes annexures, tables, export data, ministry junk)
- Numeric-heavy table detection
- Drops tiny chunks
- Keeps only farmer-useful agronomy content
"""

import os
import re
import json
from collections import Counter
from pathlib import Path

# CONFIGURATION

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "extracted_text"
OUTPUT_DIR = BASE_DIR / "data" / "chunks"
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

TARGET_CHUNK_MIN_WORDS = 150
TARGET_CHUNK_MAX_WORDS = 1200
OVERLAP_WORDS = 150

MIN_FINAL_CHUNK_WORDS = 120
MAX_NUMERIC_RATIO = 0.40

# REJECTED SECTION KEYWORDS

REJECT_SECTION_KEYWORDS = [
    "annexure", "appendix", "website", "ministry",
    "export", "import", "country", "production statistics",
    "state-wise", "marketing year", "frp", "procurement",
    "organization", "conference", "seminar",
    "trading", "area statistics", "yield statistics",
    "important institution", "board", "authority",
]

# CROP DETECTION

CROP_KEYWORDS = {
    "wheat": ["wheat", "gehun"],
    "cotton": ["cotton", "kapas", "bt cotton"],
    "rice": ["rice", "paddy", "dhan"],
    "sugarcane": ["sugarcane", "ganna", "sugar cane"],
}

def detect_crop(filename: str, text: str) -> str:
    combined = (filename + " " + text[:2000]).lower()
    for crop, keywords in CROP_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            return crop
    return "unknown"

# HEADING DETECTION

KNOWN_HEADINGS = [
    "Sowing", "Seed Rate", "Seed Treatment",
    "Fertilizer", "Irrigation",
    "Weed Management", "Pest Management",
    "Disease Management", "Harvesting",
    "Varieties", "Soil Preparation",
]

def build_heading_pattern():
    known = '|'.join(re.escape(h) for h in KNOWN_HEADINGS)
    return re.compile(
        rf'(?m)^[ \t]*(?:'
        rf'(?:{known})'
        rf'|[A-Z][A-Za-z\s\(\)\/\-]{{3,50}}'
        rf')[ \t]*$',
        re.IGNORECASE
    )

HEADING_PATTERN = build_heading_pattern()

def split_by_headings(text: str):
    sections = []
    matches = list(HEADING_PATTERN.finditer(text))

    if not matches:
        return [{"section": "General", "text": text.strip()}]

    if matches[0].start() > 0:
        intro = text[:matches[0].start()].strip()
        if intro:
            sections.append({"section": "Introduction", "text": intro})

    for i, match in enumerate(matches):
        heading = match.group().strip()
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content:
            sections.append({"section": heading, "text": content})

    return sections

# QUALITY FILTERING

def word_count(text):
    return len(text.split())

def numeric_ratio(text):
    tokens = text.split()
    if not tokens:
        return 1
    numeric_tokens = sum(1 for t in tokens if any(c.isdigit() for c in t))
    return numeric_tokens / len(tokens)

def is_useful_section(section, text):
    section_lower = section.lower()

    if any(keyword in section_lower for keyword in REJECT_SECTION_KEYWORDS):
        return False

    if numeric_ratio(text) > MAX_NUMERIC_RATIO:
        return False

    if word_count(text) < MIN_FINAL_CHUNK_WORDS:
        return False

    return True

# SPLIT LARGE SECTIONS

def split_large_section(section, max_words, overlap_words):
    words = section["text"].split()
    chunks = []
    start = 0
    part = 1

    while start < len(words):
        end = min(start + max_words, len(words))
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)

        chunks.append({
            "section": f"{section['section']} (Part {part})",
            "text": chunk_text
        })

        if end == len(words):
            break

        start += max_words - overlap_words
        part += 1

    return chunks

# MAIN CHUNKING

def chunk_document(text, filename):
    crop = detect_crop(filename, text)
    sections = split_by_headings(text)

    final_sections = []

    for sec in sections:
        if word_count(sec["text"]) > TARGET_CHUNK_MAX_WORDS:
            final_sections.extend(
                split_large_section(sec, TARGET_CHUNK_MAX_WORDS, OVERLAP_WORDS)
            )
        else:
            final_sections.append(sec)

    chunks = []
    for i, sec in enumerate(final_sections):
        if not is_useful_section(sec["section"], sec["text"]):
            continue

        chunk = {
            "chunk_id": f"{os.path.splitext(filename)[0]}_chunk_{i+1}",
            "crop": crop,
            "source_file": filename,
            "section": sec["section"],
            "word_count": word_count(sec["text"]),
            "text": sec["text"]
        }
        chunks.append(chunk)

    return chunks

# PIPELINE

def run_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    txt_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

    if not txt_files:
        print("No text files found")
        return

    all_chunks = []

    for txt_file in txt_files:
        print(f"Chunking: {txt_file}")

        with open(INPUT_DIR / txt_file, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_document(text, txt_file)
        all_chunks.extend(chunks)

        print(f"  Crop: {chunks[0]['crop'] if chunks else 'none'}")
        print(f"  Chunks kept: {len(chunks)}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print("Total final chunks:", len(all_chunks))

    crop_counts = Counter(c["crop"] for c in all_chunks)
    print("Chunks by crop:")
    for crop, count in crop_counts.items():
        print(crop, "->", count)

if __name__ == "__main__":
    run_pipeline()
