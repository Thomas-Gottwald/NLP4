import fire
import pickle
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class SearchStudies:
    """
    Contains all existing functions for automating literature reviews
    """

    def snowballing(self, starterSetPath = ""):
        """
        Trains model on `train_data_path` data and saves trained model to `model_path`.
        :param starterSetPath: path to to your existing starterset. Alternatively plcae your starter set in the default folde
        """
        logger.info(f"Snowballing startign")
        #SearchStudies.snowballing(starterSetPath)
        logger.info("Snowballing finished")



class SelectStudies:
    """
    Contains all functions that help to select appropriate studies
    """
    def extractKeywords(self):
        """
        Extracts keywords of given paper in PDF format
        """
        logger.info("BLABLABLABALBLABLA")


if __name__ == "__main__":
    fire.Fire()