import pytest
from src.modules.Similarities import sBert_1to1_cosine
from src.modules.Similarities import sBERT_querys
from src.modules.PDFMiner import PDFMiner


def test_1to1_similarity():
    paper1 = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf"
    sim = sBert_1to1_cosine(PDFMiner.getPDFText(paper1).rsplit('References', 1)[0], PDFMiner.getPDFText(paper1).rsplit('References', 1)[0])
    assert sim.numpy()[0] == 1

def test_querry_similarity():
    corpus =  ["C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf","C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\3.pdf","C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\7.pdf"]
    query = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf"


