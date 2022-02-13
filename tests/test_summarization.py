import arxiv
import pytest
from src.modules.PDFMiner import get_pdf_text
from src.modules.Summarization import generate_summary


def test_summarization():
    search = arxiv.Search(query="nlp keyword extraction", max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    for result in search.results():
        pdf = result.summary
    summary = generate_summary(pdf, top_n=3)
    assert isinstance(summary, list)


