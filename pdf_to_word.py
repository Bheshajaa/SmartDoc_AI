import io
import os
import tempfile
import pythoncom
import win32com.client


def pdf_to_word(file):
    pythoncom.CoInitialize()  # ✅ REQUIRED

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = os.path.join(tmp, "input.pdf")
        docx_path = os.path.join(tmp, "output.docx")

        # Write uploaded PDF
        with open(pdf_path, "wb") as f:
            f.write(file.read())

        # Open Word
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(pdf_path)
        doc.SaveAs(docx_path, FileFormat=16)  # 16 = DOCX
        doc.Close()
        word.Quit()

        # Read DOCX back to memory
        with open(docx_path, "rb") as f:
            return io.BytesIO(f.read())
