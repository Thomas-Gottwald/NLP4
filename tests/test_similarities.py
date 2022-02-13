import pytest
from src.modules.Similarities import specter_1to1_cosine
from src.modules.Similarities import specter_query_similarity
from src.modules.PDFMiner import getPDFText


def test_1to1_similarity():
    paper1 = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf"
    sim = specter_1to1_cosine(getPDFText(paper1).rsplit('References', 1)[0], getPDFText(paper1).rsplit('References', 1)[0])
    assert isinstance(sim.numpy()[0][0],float)

def test_querry_similarity():
    corpus =  ["C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf","C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\3.pdf","C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\7.pdf"]
    query = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf"


