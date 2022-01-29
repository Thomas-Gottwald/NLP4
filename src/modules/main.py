import fire
import logging
from SearchStudies import snowballing as sb


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


if __name__ == "__main__":
    fire.Fire()
