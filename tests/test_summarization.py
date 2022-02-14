import arxiv
from src.modules.Summarization import generate_summary
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


def test_summarization():
    pdf = ''
    search = arxiv.Search(query="nlp keyword extraction", max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    for result in search.results():
        pdf = result.summary
    summary = generate_summary(pdf, top_n=3)
    assert isinstance(summary, list)
