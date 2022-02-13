import pytest
from src.modules.PDFMiner import get_pdf_text


def test_pdf_to_text():
    pdf_string = get_pdf_text("C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf")
    assert isinstance(pdf_string, str)
    assert isinstance("", int)


