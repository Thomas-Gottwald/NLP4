import fire
from PaperSearch import snowballing as sb
import KeywordKeyphraseExtractor
import Similarities
import Summarization
from PDFMiner import get_pdf_text
from ReferenceExtraction import get_referenced_papers
import json
import PaperSelection
import os
from pathlib import Path
dirname = Path(__file__).parent


def summarization(text='', top_n=5):
    """
    Creates a summary out of a text. Therefore, the algorithm takes a text and parse it into the single sentences.
    Those sentences get compared with each other --> Cosine similarity. Out of this it is possible to choose the most
    relevant sentences relating all others to create the summary.
    :param top_n: Chose the n best sentences to create the summary.
    :param text: Text for summarization.
    :return: Returns the summary of the given text.
    """
    return Summarization.generate_summary(text, top_n)


def extract_pdf_references(pdf="", save_to_file=""):
    """
    Extracts the references of the given Paper. If save_to_file is set the references will be saved in the specified file.
    :param pdf: Path or URL to the pdf of which the references should be extracted
    :param save_to_file Optional path to file in which the extracted references will be saved in json format
    """
    references = get_referenced_papers(pdf)
    print(references)
    if save_to_file != "":
        with open(save_to_file, "w") as f:
            f.write(json.dumps(references, indent=4, sort_keys=True))


def snowballing(seed_set_path=os.path.join(dirname, 'snowballing_seed_set'), iterations=1, min_similarity=0.85, result_file=os.path.join(dirname, 'snowballing_result.json')):
    """
    Conducts and automated forward snowballing with set of papers PDFs given in the seed_set_path as seed set
    :param seed_set_path: Path to your existing seed set. Alternatively place your papers to start with in the default folder: src/seed_set
    :param iterations: specify how many iterations the snowballing should make
    :param min_similarity:
    :param result_file:
    """
    sb(seed_set_path, iterations, min_similarity=min_similarity, result_file=result_file)


def paper_selection(text=[], keywords=[]):
    """
    This function calculates the similarity between keywords or phrases relating a text. So it is possible to compare
    several texts and keywords in once to see which text is the best relating special keywords. Also a plot is
    generated, where it is possible to see the scores of all paper and keywords

    :param text: This is a list of texts which you want to compare with the keywords
    :param keywords: The keywords in this list are used to compare the single texts.
    :return:
    """
    df = PaperSelection.paper_importance(text, keywords)
    fig = PaperSelection.plot_paper_selection(df)
    return df, fig


def snowballing_paper_selection(snowballing_result_path=os.path.join(dirname, 'snowballing_result.json'), keywords=[]):
    """
    Takes the result generated from the snowballing and adds keyword similarities (paper importance) of each result from the snowballing,
    as well as plotting the results in an interactive plot.
    :param snowballing_result_path: Path to to your existing seed set. Alternatively place your place your papers to start with in the default folder: src/seed_set.
    :param keywords: The keywords in this list are used to compare the snowballing results.
    """
    PaperSelection.snowballing_paper_importance(snowballing_result_path, keywords)


def extract_keywords_pdf(pdf=""):
    """
    Prints the extracted keywords of the given PDF
    :param paper1: Path or URL to the PDF
    """
    KeywordKeyphraseExtractor.rake_phrase_extraction(get_pdf_text(pdf).rsplit('References', 1)[0])


def extract_keyphrases_pdf(pdf=""):
    """
    Prints extracted KeyPhrases to the given PDF
    :param paper1: path or url to the PDF
    """
    KeywordKeyphraseExtractor.rake_phrase_extraction(get_pdf_text(pdf).rsplit('References', 1)[0])


def pdf_similarity(paper1="", paper2="", only_abstract=False):
    """
    Returns the cosine similarity of SPECTER embeddings between  paper1 and paper2
    :param paper1: Path to first paper to be compared
    :param paper2: Path to second paper to be compared
    :param only_abstract If set to true the function will try to extract the abstracts of the pdfs and will only compare those
    """
    similarity = Similarities.pdf_similarity(paper1, paper2, only_abstract=only_abstract)
    print(f"Papers have similarity score of: {similarity}")


if __name__ == "__main__":
    fire.Fire()
