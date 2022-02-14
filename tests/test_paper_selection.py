import arxiv
import pandas
import os
from src.modules.PaperSelection import paper_importance, plot_paper_selection, snowballing_paper_importance
dirname = os.path.dirname(__file__)


def test_paper_selection():
    research_keywords = ['NLP', 'Keywords', 'Core', 'Tweets', 'geography']
    search = arxiv.Search(query="nlp keyword extraction", max_results=5, sort_by=arxiv.SortCriterion.Relevance)
    pdf_abstract = list()
    rank_title = list()
    for result in search.results():
        pdf_abstract.append(result.summary)
        rank_title.append(result.title)
    df = paper_importance(pdf_abstract, research_keywords)
    fig = plot_paper_selection(df)
    df = paper_importance(pdf_abstract, research_keywords, rank_title)
    fig = plot_paper_selection(df)
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(fig, object)


def test_select_snowballing_results():
    snowballing_paper_importance(os.path.join(dirname, 'snowballing_result_no_keyword_sims.json'), ['conspiracy', 'missinformation', 'vaccination', 'test', 'whale'])
