import pytest
from src.modules.Similarities import sBert_1to1_cosine
from src.modules.PDFMiner import PDFMiner


def test_pdf_to_text():
    pdfString = PDFMiner.getPDFText("C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf")
    assert isinstance(pdfString, str)


