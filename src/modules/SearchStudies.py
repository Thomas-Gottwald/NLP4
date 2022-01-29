import Similarities
import ReferenceExtraction
import os
import re
import json

# def getAbstracts():
#     for file in ["3.pdf","7.pdf","9.pdf","11.pdf","15.pdf"]:


def snowballing(starterSetPath, iterations):
    starterSet = [starterSetPath + "\\" + x for x in os.listdir(starterSetPath) if x.endswith('.pdf')]
    print(starterSet)
    starterSetAbstracts = []
    referenceAbstracts = dict()
    for file in starterSet:
        starterSetAbstracts.append(
            re.sub("</jats.*?>|<jats.*?>", "", ReferenceExtraction.getAbstractByPdf(file)['abstract']))
    for file in starterSet:
        referenceAbstracts.update(ReferenceExtraction.getReferencedPapers(file))

    referenceAbstracts = clean_reference_abstracts(referenceAbstracts)
    corpus_set = starterSetAbstracts
    query_set = referenceAbstracts
    result_set = {}

    new_set = getSimilarReferences(corpus_set, query_set, 0.8)
    result_set.update(new_set.copy())
    print("First Iteration done")
    i = 0

    while i < iterations:
        referenceAbstracts = dict()
        for paperKey in new_set:
            corpus_set.append(new_set[paperKey]['abstract'])
            if new_set[paperKey]['references'] == 'None' and "crossref" not in paperKey:
                referenceAbstracts.update(ReferenceExtraction.getReferencedPapers(paperKey))
            elif new_set[paperKey]['references'] != 'None':
                for reference in new_set[paperKey]['references']:
                    referenceAbstracts[reference] = ReferenceExtraction.getAbstractFromDoi(reference)

        referenceAbstracts = clean_reference_abstracts(referenceAbstracts)
        query_set = referenceAbstracts
        new_set.clear()
        new_set = getSimilarReferences(corpus_set, query_set, 0.8)
        result_set.update(new_set.copy())
        print("-----------------------------NextIteration done-------------------------------")
        print(new_set)
        print(len(new_set))
        i += 1
    return json.dumps(result_set)


def clean_reference_abstracts(referenceAbstracts):
    for paper in referenceAbstracts:
        if referenceAbstracts[paper]["references"] != "None":
            referenceList = []
            for reference in referenceAbstracts[paper]["references"]:
                referenceList.append(reference.get("DOI"))
            referenceList = [x for x in referenceList if x is not None]
            referenceAbstracts[paper]["references"] = referenceList

    filtered = {k:v for k, v in referenceAbstracts.items() if v["abstract"] != 'None'}
    referenceAbstracts = filtered
    for key in referenceAbstracts:
        referenceAbstracts[key]["abstract"] = re.sub("</jats.*?>|<jats.*?>", "", referenceAbstracts[key]["abstract"])
    return referenceAbstracts


def getSimilarReferences(corpus_set, query_set, min_similarity):
    similarities = Similarities.sBERT_querys(corpus_set, query_set)
    new_set = {}
    for paper in similarities:
        for score in similarities[paper][0]:
            if score["score"] > min_similarity and paper not in new_set:
                new_set[paper] = query_set[paper]
                new_set[paper]["similarity"] = f"{score['score']}, similar to corpus_set Papers"
    return new_set


# result = snowballing("C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set",1)
# print(result)
# print(len(result))
# with open("test.json", "w") as f:
#     f.write(json.dumps(json.loads(result), indent=4, sort_keys=True))
