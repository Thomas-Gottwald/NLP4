import logging
import requests
from AbstractExtraction import get_abstracts_of_reference_links
logger = logging.getLogger(__name__)


def get_referenced_papers(pdf):
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)

    if "http" in pdf:
        logging.info(f"Starting scholarcy request with url: {pdf}")
        response = requests.get('https://ref.scholarcy.com/api/references/extract', params={"url": pdf})
    else:
        logging.info(f"Starting scholarcy request with file: {pdf}")
        with open(pdf, 'rb') as f:
            response = requests.post('https://ref.scholarcy.com/api/references/extract', files={'file': f})

    jsonResponse = response.json()
    referenceLinks = jsonResponse.get("reference_links","None")

    return referenceLinks


def get_reference_abstracts(pdf):
    return get_abstracts_of_reference_links(get_referenced_papers(pdf))
