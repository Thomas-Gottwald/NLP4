import pytest
from src.modules.PDFMiner import get_pdf_text
import os
dirname = os.path.dirname(__file__)


def test_pdf_to_text():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    pdf_string = get_pdf_text(pdf)
    assert isinstance(pdf_string, str)
