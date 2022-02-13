import pytest
from src.modules.PDFMiner import getPDFText


def test_pdf_to_text():
    pdfString = getPDFText("C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf")
    assert isinstance(pdfString, str)
    assert isinstance("",int)


