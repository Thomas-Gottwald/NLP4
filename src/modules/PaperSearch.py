import json
import os
import re
import AbstractExtraction
import ReferenceExtraction
import Similarities


def snowballing(seed_set_path, iterations, min_similarity=0.85, result_file="snowballing_result.json"):
    seed_set = [os.path.join(seed_set_path, x) for x in os.listdir(seed_set_path) if x.endswith('.pdf')]
    print(seed_set)
    print("This may take a while, go get a coffee... or two :)")
    seed_set_abstracts = []
    reference_abstracts = dict()
    for file in seed_set:
        title_abstract = AbstractExtraction.get_abstract_by_pdf(file)
        if title_abstract['abstract'] != "None":
            title_abstract["abstract"] = re.sub('</jats.*?>|<jats.*?>', "", title_abstract["abstract"])  # remove jats-tags that appear in some abstracts retrieved by crossref api
            seed_set_abstracts.append(title_abstract)
    for file in seed_set:
        temp_ref_abstracts = ReferenceExtraction.get_reference_abstracts(file)
        reference_abstracts.update(temp_ref_abstracts)

    reference_abstracts = ReferenceExtraction.cleanup_reference_abstracts(reference_abstracts)
    corpus_set = seed_set_abstracts
    query_set = reference_abstracts
    result_set = {}

    new_set = get_similar_references(corpus_set, query_set, min_similarity)
    result_set.update(new_set.copy())
    print("First Iteration done")

    # The while loops continues the snowballing with the initialy retrieved references
    # for the given number of iterations
    i = 0
    while i < iterations:
        reference_abstracts = dict()
        for paperKey in new_set:
            corpus_set.append(new_set[paperKey])  # Append all new papers of itearation to corpus_set
            if new_set[paperKey]['references'] == 'None' and "crossref" not in paperKey:
                # If the paper is not from crossref we need to extract the references
                # and the abstracts of the paper with the get_reference_abstracts function
                reference_abstracts.update(ReferenceExtraction.get_reference_abstracts(paperKey))
            elif new_set[paperKey]['references'] != 'None':
                # If the paper allready has references extracted, since we extracted it's abstract from crossref
                # (see AbstractExtraction.get_abstract_from_doi)
                # we can simply extract all abstracts from the references by the doi of the reference
                for reference in new_set[paperKey]['references']:
                    reference_abstracts[reference] = AbstractExtraction.get_abstract_from_doi(reference)

        reference_abstracts = ReferenceExtraction.cleanup_reference_abstracts(reference_abstracts)
        query_set = reference_abstracts
        new_set.clear()
        if len(query_set) != 0:
            new_set = get_similar_references(corpus_set, query_set, 0.8)
            result_set.update(new_set.copy())
        print(f"-----------------------------{i + 2}. Iteration done-------------------------------")
        i += 1
    with open("result_file.json", "w") as f:
        json.dump(result_set, f, indent=4)
    print(json.dumps(result_set))
    return json.dumps(result_set)


def get_similar_references(corpus_set, query_set, min_similarity):
    print("Start caluclating abstract similarities")
    similarities = Similarities.specter_query_reference_similarity(corpus_set, query_set)
    new_set = {}
    for paper in similarities:
        for score in similarities[paper][0]:
            if score["score"] > min_similarity and paper not in new_set:
                new_set[paper] = query_set[paper]
                new_set[paper]["similarity"] = f"{score['score']}, similar to corpus_set Papers"
    return new_set
