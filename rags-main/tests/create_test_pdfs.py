
from pathlib import Path
from reportlab.pdfgen import canvas

output_dir = Path("tests/sample_docs")
output_dir.mkdir(parents=True, exist_ok=True)

documents = {
    "company.pdf": [
        "WynTech is a fictional software company.",
        "WynTech was founded in 2022.",
        "Its headquarters is in Chennai.",
        "Its main product is called CloudReach."
    ],
    "product.pdf": [
        "CloudReach is a business automation platform.",
        "It supports email and WhatsApp campaigns.",
        "CloudReach uses Python for backend services.",
        "Its database is PostgreSQL."
    ]
}

for filename, lines in documents.items():
    path = output_dir / filename
    pdf = canvas.Canvas(str(path))
    pdf.setFont("Helvetica", 12)

    y = 760
    for line in lines:
        pdf.drawString(50, y, line)
        y -= 25

    pdf.save()
    print(f"Created: {path}")
