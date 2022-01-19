import gensim
from sentence_transformers import SentenceTransformer, util

def getPaperSimilarity(corpusset, queryDocument):
    documents = corpusset
    compare = queryDocument

    stoplist = set('for a of the and to in \n is '.split())
    texts = [
        [word for word in document.lower().split() if word not in stoplist]
        for document in documents
    ]

    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    feature_cnt = len(dictionary.token2id)
    print(feature_cnt)

    lsi = gensim.models.TfidfModel(corpus, id2word=dictionary)

    vec_bow = dictionary.doc2bow(compare.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    print(vec_lsi)

    index = gensim.similarities.SparseMatrixSimilarity(lsi[corpus], num_features=feature_cnt)

    sim = index[vec_lsi]

    for i in range(len(sim)):
        print('keyword is similar to text%d: %.2f' % (i + 1, sim[i]))

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


