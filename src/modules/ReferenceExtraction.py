import logging
import requests
from AbstractExtraction import get_abstracts_of_reference_links
import re
logger = logging.getLogger(__name__)


def get_referenced_papers(pdf):
    try:
        if "http" in pdf:
            logging.info(f"Starting scholarcy request with url: {pdf}")
            response = requests.get('https://ref.scholarcy.com/api/references/extract', params={"url": pdf})
        else:
            logging.info(f"Starting scholarcy request with file: {pdf}")
            with open(pdf, 'rb') as f:
                response = requests.post('https://ref.scholarcy.com/api/references/extract', files={'file': f})
    except requests.exceptions.ConnectionError:
        return "None"

    jsonResponse = response.json()
    referenceLinks = jsonResponse.get("reference_links", "None")
    if referenceLinks is None:
        referenceLinks = "None"

    return referenceLinks


def get_reference_abstracts(pdf):
    return get_abstracts_of_reference_links(get_referenced_papers(pdf))


def cleanup_reference_abstracts(reference_abstracts):
    for paper in reference_abstracts:
        if reference_abstracts[paper]["references"] != "None":
            referenceList = []
            for reference in reference_abstracts[paper]["references"]:
                referenceList.append(reference.get("DOI"))
            referenceList = [x for x in referenceList if x is not None]
            reference_abstracts[paper]["references"] = referenceList

    filtered = {k:v for k, v in reference_abstracts.items() if v["abstract"] != 'None'}
    reference_abstracts = filtered
    for key in reference_abstracts:
        reference_abstracts[key]["abstract"] = re.sub('</jats.*?>|<jats.*?>', "", reference_abstracts[key]["abstract"])
    return reference_abstracts
