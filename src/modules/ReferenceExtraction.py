import logging
import requests
import arxiv
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
    referenceLinks = jsonResponse["reference_links"]
    logging.info(f"Found {len(referenceLinks)} refrences in given paper")

    return referenceLinks


def get_pdfs_of_scholarcy_link(referenceLinks):
    refLinks = []
    for reflink in referenceLinks:
        link = reflink.get("oa_query")
        if link is not None:
            refLinks.append(link)
