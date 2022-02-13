from src.modules.ReferenceExtraction import get_referenced_papers
from src.modules.ReferenceExtraction import get_reference_abstracts
import os
dirname = os.path.dirname(__file__)

def test_returns_reference_links():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    references = get_referenced_papers(pdf)
    assert "oa_querry" in references[0].keys() or "crossref" in references[0].keys() or "scholar_url" in references[0].keys()


def test_returns_reference_links_of_link():
    pdf = "https://arxiv.org/pdf/2101.00005.pdf"
    references = get_referenced_papers(pdf)
    assert references is None or "oa_querry" in references[0].keys() or "crossref" in references[0].keys() or "scholar_url" in references[0].keys()


def test_get_reference_abstract():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    abstracts = get_reference_abstracts(pdf)
    assert isinstance(abstracts, dict)

