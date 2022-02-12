from sentence_transformers import SentenceTransformer, util
import pandas as pd
from plotly.subplots import make_subplots as ms


def paper_importance(text=[], keywords=[]):

    model = SentenceTransformer('allenai-specter')

    keyword_corpus = model.encode(keywords, convert_to_tensor=True)
    match_set = {}
    text_corpus = model.encode(text, convert_to_tensor=True)
    match_set = util.semantic_search(text_corpus, keyword_corpus,  top_k=len(keywords))

    rank_title = []
    for i in range(0, len(text)):
        rank_title.append('Text_' + str(i))

    df = pd.DataFrame(index=rank_title, columns=keywords)

    for i, match in enumerate(match_set):

        for entry in match:
            df.iloc[i, entry['corpus_id']] = entry['score']
    print(df)
    return df


def plot_paper_selection(df=pd.DataFrame()):

    fig = ms(rows=1, cols=1, x_title='Keywords', y_title='Similarity')
    for i, name in enumerate(df.index):
        fig.add_scatter(x=df.columns, y=df.iloc[i, :], mode="markers", marker=dict(size=10),
                        row=1, col=1, name=name)
    fig.show()


