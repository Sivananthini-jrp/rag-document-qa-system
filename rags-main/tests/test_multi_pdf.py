
from pathlib import Path

from core.utils import load_data


def test_load_multiple_pdfs():
    paths = [
        "tests/sample_docs/company.pdf",
        "tests/sample_docs/product.pdf",
    ]

    assert all(Path(p).exists() for p in paths)

    documents = load_data(file_names=paths)

    assert len(documents) >= 2

    combined_text = " ".join(
        doc.text for doc in documents
    )

    assert "WynTech" in combined_text
    assert "CloudReach" in combined_text
    assert "PostgreSQL" in combined_text


def test_pdf_metadata():
    paths = [
        "tests/sample_docs/company.pdf",
        "tests/sample_docs/product.pdf",
    ]

    documents = load_data(file_names=paths)

    filenames = {
        Path(doc.metadata.get("file_name", "")).name
        for doc in documents
    }

    assert "company.pdf" in filenames
    assert "product.pdf" in filenames
