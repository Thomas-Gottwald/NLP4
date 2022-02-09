import fire
import logging
from SearchStudies import snowballing as sb
import KeywordKeyphraseExtractor
import Similarities
from PDFMiner import PDFMiner


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SelectStudies:
    """
    Contains all functions that help to select appropriate studies
    """
    def extractKeywords(self):
        """
        Extracts keywords of given paper in PDF format
        """
        logger.info("BLABLABLABALBLABLA")
        fire.Fire()


class search_studies:
    """
    Contains all existing functions for automating literature reviews
    """

    def snowballing(self, starterSetPath=".\\src\\starter_set"):
        """
        Trains model on `train_data_path` data and saves trained model to `model_path`.
        :param starterSetPath: path to to your existing starterset. Alternatively plcae your starter set in the default folde
        """
        logger.info("Snowballing startign")
        sb(starterSetPath, 1)
        logger.info("Snowballing finished")


class functions:
    """
    Contains all standalone functions
    """
    def snowballing(self, starterSetPath="C:\\Users\\fabia\\PycharmProjects\\NLP4\\src\\starter_set", iterations=1):
        """
        Conducts and automated forward snowballing on with set of papers given in <starterSetPath>
        :param starterSetPath: path to to your existing starterset. Alternatively place your starter set in the default folder
        :param iterations: specify how many iterations the snowballing should make
        """
        logger.info("Snowballing startign")
        sb(starterSetPath, iterations)
        logger.info("Snowballing finished")

    def similiarity1to1(self, paper1 = "rsos.201199.pdf", paper2="2111.10594v1.Misrepresenting_Scientific_Consensus_on_COVID_19_The_Amplification_of_Dissenting_Scientists_on_Twitter.pdf"):
        """
        Returns the cosine similarity of sBert embeddings between of paper1 and paper2
        :param paper1: Path to first paper to be compared
        :param paper2: Path to second paper to be compared
        """
        print(f"Papers have similarity score of: {Similarities.sBert_1to1_cosine(PDFMiner.getPDFText(paper1).rsplit('References',1)[0],PDFMiner.getPDFText(paper2).rsplit('References',1)[0])}")

    def extractKeyWords(self, pdf="Tropical Med Int Health - 2020 - Velavan - The COVID%u201019 epidemic.pdf"):
        """
        Prints the extracted keywords of the given PDF
        :param paper1: path or url to the PDF
        """
        KeywordKeyphraseExtractor.rake_phrase_extraction(PDFMiner.getPDFText(pdf).rsplit('References',1)[0])

    def extractKeyPhrases(self, pdf="Tropical Med Int Health - 2020 - Velavan - The COVID%u201019 epidemic.pdf"):
        """
        Prints extracted KeyPhrases to the given PDF
        :param paper1: path or url to the PDF
        """
        KeywordKeyphraseExtractor.rake_phrase_extraction(PDFMiner.getPDFText(pdf).rsplit('References',1)[0])


if __name__ == "__main__":
    fire.Fire()
