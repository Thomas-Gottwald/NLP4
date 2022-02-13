import fire
import logging
from SearchStudies import snowballing as sb
import KeywordKeyphraseExtractor
import Similarities
from PDFMiner import getPDFText
from ReferenceExtraction import get_referenced_papers
import json
import os


def extract_keywords_pdf(pdf="Tropical Med Int Health - 2020 - Velavan - The COVID%u201019 epidemic.pdf"):
    """
    Prints the extracted keywords of the given PDF
    :param paper1: path or url to the PDF
    """
    KeywordKeyphraseExtractor.rake_phrase_extraction(getPDFText(pdf).rsplit('References', 1)[0])


def snowballing(starterSetPath="C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set", iterations=1):
    """
    Conducts and automated forward snowballing with set of papers given in <starterSetPath> as seed set
    :param starterSetPath: path to to your existing seed set. Alternatively place your starter set in the default folder src/seed_set
    :param iterations: specify how many iterations the snowballing should make
    """
    sb(starterSetPath, iterations)


def pdf_similarity(paper1="rsos.201199.pdf", paper2="C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set\\2111.10594v1.Misrepresenting_Scientific_Consensus_on_COVID_19_The_Amplification_of_Dissenting_Scientists_on_Twitter.pdf", only_abstract=False):
    """
    Returns the cosine similarity of sBert embeddings between of paper1 and paper2
    :param paper1: Path to first paper to be compared
    :param paper2: Path to second paper to be compared
    :param only_abstract If set to true the function will try to extract the abstracts of the pdfs and will only compare those
    """
    similarity = Similarities.pdf_similarity(paper1, paper2, only_abstract=only_abstract)
    print(f"Papers have similarity score of: {similarity}")


def extract_pdf_references(pdf="rsos.201199.pdf", save_to_file=""):
    references = get_referenced_papers(pdf)
    print(references)
    if save_to_file != "":
        with open(save_to_file, "w") as f:
            f.write(json.dumps(references, indent=4, sort_keys=True))


def extract_keyphrases_string(pdf="Tropical Med Int Health - 2020 - Velavan - The COVID%u201019 epidemic.pdf"):
    """
    Prints extracted KeyPhrases to the given PDF
    :param paper1: path or url to the PDF
    """
    KeywordKeyphraseExtractor.rake_phrase_extraction(getPDFText(pdf).rsplit('References', 1)[0])


if __name__ == "__main__":
    fire.Fire()
