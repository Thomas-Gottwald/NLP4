import gensim


def getPaperSimilarity(corpusset, queryDocument):
    documents = corpusset
    compare = queryDocument

    stoplist = set('for a of the and to in'.split())
    texts = [
        [word for word in document.lower().split() if word not in stoplist]
        for document in documents
    ]

    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    feature_cnt = len(dictionary.token2id)
    print(feature_cnt)

    lsi = gensim.models.LsiModel(corpus, id2word=dictionary)

    vec_bow = dictionary.doc2bow(compare.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    print(vec_lsi)

    index = gensim.similarities.SparseMatrixSimilarity(lsi[corpus], num_features=feature_cnt)

    sim = index[vec_lsi]

    for i in range(len(sim)):
        print('keyword is similar to text%d: %.2f' % (i + 1, sim[i]))

