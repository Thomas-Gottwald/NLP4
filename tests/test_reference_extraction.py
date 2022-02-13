from src.modules.ReferenceExtraction import get_referenced_papers
from src.modules.ReferenceExtraction import get_reference_abstracts


def test_returns_reference_links():
    pdf = "C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set\\15.pdf"
    references = get_referenced_papers(pdf)
    print(references)
    assert "oa_querry" in references[0].keys() or "crossref" in references[0].keys() or "scholar_url" in references[0].keys()

def test_returns_reference_links_of_link():
    pdf = "https://arxiv.org/abs/2101.00005"
    references = get_referenced_papers(pdf)
    print(references)
    assert references is None or "oa_querry" in references[0].keys() or "crossref" in references[0].keys() or "scholar_url" in references[0].keys()

def test_get_reference_abstract():
    pdf = "C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set\\15.pdf"
    abstracts = get_reference_abstracts(pdf)
    assert isinstance(abstracts, dict)

