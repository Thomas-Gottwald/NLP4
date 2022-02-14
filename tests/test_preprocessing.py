import arxiv
from src.modules.text_preprocessing import tokenize, remove_stopwords, lemmatizing, port_stemmer, position_tag
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


def test_preprocessing():
    pdf = ""
    search = arxiv.Search(query="nlp keyword extraction", max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    for result in search.results():
        pdf = result.summary

    tokens = tokenize(pdf)
    filtered_text = remove_stopwords(pdf, ["the", "and"])
    lemma = lemmatizing(pdf)
    stem = port_stemmer(pdf)
    tags = position_tag(pdf)

    assert isinstance(tokens, list)
    assert isinstance(filtered_text, str)
    assert isinstance(lemma, str)
    assert isinstance(stem, str)
    assert isinstance(tags, list)
