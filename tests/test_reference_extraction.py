from src.modules.ReferenceExtraction import get_referenced_papers


def test_returns_reference_links():
    pdf = "C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set\\15.pdf"
    references = get_referenced_papers(pdf)
    print(references)
    assert "oa_querry" in references[0].keys() or "crossref" in references[0].keys() or "scholar_url" in references[0].keys()