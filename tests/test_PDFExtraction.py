from src.modules.PDFMiner import getPDFText
import os
dirname = os.path.dirname(__file__)

def test_pdf_to_text():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    pdfString = getPDFText(pdf)
    assert isinstance(pdfString, str)
