from pathlib import Path
import json

from pypdf import PdfReader

def chunk_pdf_by_page(pdf_path: Path):
    reader = PdfReader(pdf_path)

    chunks = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if not text:
            continue

        chunks.append({
            "chunk_id": f"{pdf_path.stem}_p{page_number}",
            "source": pdf_path.name,
            "page": page_number,
            "text": text,
        })

    return chunks


def save_jsonl(chunks, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def parserPdf(pdf_dir, output_dir):
    # Percorre todos os PDFs
    pdf_files = list(pdf_dir.glob("*.pdf"))

    print(f"Encontrados {len(pdf_files)} PDF(s).")

    for pdf_path in pdf_files:
        print(f"Processando: {pdf_path.name}")

        chunks = chunk_pdf_by_page(pdf_path)

        output_path = output_dir / f"{pdf_path.stem}.jsonl"

        save_jsonl(chunks, output_path)

        print(f"  → {len(chunks)} chunks criados.")

