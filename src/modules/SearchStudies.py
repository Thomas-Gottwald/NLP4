import json
import os
import re
import AbstractExtraction
import ReferenceExtraction
import Similarities


def snowballing(starterSetPath, iterations):
    starterSet = [starterSetPath + "\\" + x for x in os.listdir(starterSetPath) if x.endswith('.pdf')]
    starterSet = starterSet[0:2]
    print(starterSet)
    starterSetAbstracts = []
    reference_abstracts = dict()
    for file in starterSet:
        starterSetAbstracts.append(
            re.sub("</jats.*?>|<jats.*?>", "", AbstractExtraction.get_abstract_by_pdf(file)))
    for file in starterSet:
        temp_ref_abstracts = ReferenceExtraction.get_reference_abstracts(file)
        reference_abstracts.update(temp_ref_abstracts)

    print(reference_abstracts)
    reference_abstracts = cleanup_reference_abstracts(reference_abstracts)
    corpus_set = starterSetAbstracts
    query_set = reference_abstracts
    result_set = {}

    new_set = get_similar_references(corpus_set, query_set, 0.8)
    result_set.update(new_set.copy())
    print("First Iteration done")
    i = 0

    while i < iterations:
        reference_abstracts = dict()
        for paperKey in new_set:
            corpus_set.append(new_set[paperKey]['abstract'])
            if new_set[paperKey]['references'] == 'None' and "crossref" not in paperKey:
                reference_abstracts.update(ReferenceExtraction.get_reference_abstracts(paperKey))
            elif new_set[paperKey]['references'] != 'None':
                for reference in new_set[paperKey]['references']:
                    reference_abstracts[reference] = AbstractExtraction.get_abstract_from_doi(reference,with_references=True)

        reference_abstracts = cleanup_reference_abstracts(reference_abstracts)
        query_set = reference_abstracts
        new_set.clear()
        new_set = get_similar_references(corpus_set, query_set, 0.8)
        result_set.update(new_set.copy())
        print("-----------------------------NextIteration done-------------------------------")
        print(new_set)
        print(len(new_set))
        i += 1
    return json.dumps(result_set)


def cleanup_reference_abstracts(referenceAbstracts):
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


def get_similar_references(corpus_set, query_set, min_similarity):
    similarities = Similarities.specter_query_similarity(corpus_set, query_set)
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
#      f.write(json.dumps(json.loads(result), indent=4, sort_keys=True))
