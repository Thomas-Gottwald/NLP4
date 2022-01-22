import gensim
from sentence_transformers import SentenceTransformer, util

def sBERT_querys(corpus_set,query_set):
    model = SentenceTransformer('allenai-specter')
    corpus_embeddings = model.encode(corpus_set,convert_to_tensor=True)
    match_set = {}
    for key in query_set:
        if query_set[key]['abstract'] == "None":
            continue
        query = model.encode(query_set[key]['abstract'], convert_to_tensor=True)
        match_set[key] = util.semantic_search(query,corpus_embeddings)
    return match_set


def sBert_1to1_cosine(first, second):
    model = SentenceTransformer('allenai-specter')
    first = model.encode(first, convert_to_tensor=True)
    second = model.encode(second,convert_to_tensor=True)
    return util.cos_sim(first,second)

