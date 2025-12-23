import io
import os
import tempfile
import pythoncom
from docx2pdf import convert


def word_to_pdf(file):
    # ✅ Required for Windows COM
    pythoncom.CoInitialize()

    with tempfile.TemporaryDirectory() as tmp:
        docx_path = os.path.join(tmp, "input.docx")
        pdf_path = os.path.join(tmp, "output.pdf")

        # Write uploaded file to temp
        with open(docx_path, "wb") as f:
            f.write(file.read())

        # Convert using MS Word
        convert(docx_path, pdf_path)

        # Read PDF back to memory
        with open(pdf_path, "rb") as f:
            return io.BytesIO(f.read())
