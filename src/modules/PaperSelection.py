from sentence_transformers import SentenceTransformer, util
import pandas as pd
from plotly.subplots import make_subplots as ms
import json


def paper_importance(text=[], keywords=[], rank_title=[]):

    model = SentenceTransformer('allenai-specter')
    keyword_corpus = model.encode(keywords, convert_to_tensor=True)
    match_set = {}
    text_corpus = model.encode(text, convert_to_tensor=True)
    match_set = util.semantic_search(text_corpus, keyword_corpus, top_k=len(keywords))

    if len(rank_title) == len(text):
        df = pd.DataFrame(index=rank_title, columns=keywords)

        for i, match in enumerate(match_set):

            for entry in match:
                df.iloc[i, entry['corpus_id']] = entry['score']
        print(df)
        return df

    else:
        print('Not enough Titles for the Papers names are replaced by Numbers')
        rank_title_num = list()
        for i in range(0, len(text)):
            rank_title_num.append('Text_' + str(i))

        df = pd.DataFrame(index=rank_title_num, columns=keywords)

        for i, match in enumerate(match_set):

            for entry in match:
                df.iloc[i, entry['corpus_id']] = entry['score']
        print(df)
        return df


def plot_paper_selection(df=pd.DataFrame()):
    fig = ms(rows=1, cols=1, x_title='Keywords', y_title='Similarity')
    for i, name in enumerate(df.index):
        fig.add_scatter(x=df.columns, y=df.iloc[i, :], mode="lines + markers", marker=dict(size=10),
                        row=1, col=1, name=name)
    fig.show()
    return fig


def reference_importance_by_keyword(snowballing_result_path, keywords=[]):
    with open(snowballing_result_path) as json_file:
        snowballing_result = json.load(json_file)
    model = SentenceTransformer('allenai-specter')

    keyword_corpus = model.encode(keywords, convert_to_tensor=True)
    for paper in snowballing_result:
        abstract_embedding = model.encode(snowballing_result[paper]['abstract'])
        match_set = util.semantic_search(abstract_embedding, keyword_corpus, top_k=len(keywords))
        scores = {}
        for score in match_set[0]:
            scores[keywords[score['corpus_id']]] = score['score']
        snowballing_result[paper]["keyword_similarites"] = scores
    with open("test.json", "w") as f:
        json.dump(snowballing_result, f, indent=4)
    plot_reference_importance(snowballing_result_path)


def plot_reference_importance(snowballing_result_path):
    with open(snowballing_result_path) as json_file:
        snowballing_result = json.load(json_file)
    key_words = list(snowballing_result[list(snowballing_result.keys())[0]]["keyword_similarites"].keys())
    columns = key_words.copy()
    columns.append("paper")
    papers = []
    for paper in snowballing_result:
        papers.append(paper)
    df = pd.DataFrame(index=papers, columns=key_words)
    for paper in snowballing_result:
        for key_word in key_words:
            df.at[paper, key_word] = snowballing_result[paper]["keyword_similarites"][key_word]
    plot_paper_selection(df)
