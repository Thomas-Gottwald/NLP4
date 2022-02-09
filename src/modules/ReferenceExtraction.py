import logging

import requests
import arxiv
logging.basicConfig(level=logging.INFO)
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

    return get_abstracts_of_reference_links(referenceLinks)


def get_abstracts_of_reference_links(reference_links):
    abstracts = {}
    for reflink in reference_links:
        if reflink.get("crossref") is not None:
            link = reflink.get("crossref")
            doi = link.replace("https://dx.doi.org/", "")
            abstracts[link.replace("https://dx.doi.org/", "http://api.crossref.org/works/")] = getAbstractFromDoi(doi)
        elif reflink.get("arxiv_url") is not None:
            link = reflink.get("arxiv_url")
            arxiv_id = link.replace("https://arxiv.org/pdf/", "")
            abstracts[link] = getAbstractFromArxiv(arxiv_id)
        else:
            link = reflink.get("oa_query")
            if link is None:
                continue
            else:
                try:
                    response = requests.get(link)
                    if response.headers.get('content-type') == "application/pdf":
                        abstracts[response.url] = getAbstractByPdf(response.url)
                except requests.exceptions.RequestException:
                    continue
    logging.info(f"Extracted {len(abstracts)} abstract of {len(reference_links)} papers")
    return abstracts


def getAbstractByPdf(pdf):
    try:
        if "http" in pdf:
            logging.info(f"Starting scholarcy request with url: {pdf}")
            response = requests.get('https://ref.scholarcy.com/api/references/extract', params={"url": pdf})
        else:
            logging.info(f"Starting scholarcy request with file: {pdf}")
            with open(pdf, 'rb') as f:
                response = requests.post('https://ref.scholarcy.com/api/references/extract', files={'file': f})
        meta = response.json().get("metadata")
        if meta.get("doi") is not None:
            doi = meta.get("doi")
            return getAbstractFromDoi(doi)
        elif meta.get("arxiv") is not None:
            arxivId = meta.get("arxiv")
            return getAbstractFromArxiv(arxivId)
        else:
            return {'abstract': "None", 'references': "None"}
    except:
        return {'abstract': "None", 'references': "None"}


def getAbstractFromArxiv(arxiv_id):
    arxiv_search = arxiv.Search(id_list=[arxiv_id])
    abstract = next(arxiv_search.results()).summary
    return {'abstract': abstract, 'references': "None"}


def getAbstractFromDoi(doi):
    print(doi)
    try:
        requestAbs = requests.get('http://api.crossref.org/works/' + doi).json()
        abstract = requestAbs["message"].get("abstract", "None")
        if requestAbs["message"].get("reference") is not None:
            references = requestAbs["message"].get("reference")
        else:
            references = "None"
        return {'abstract': abstract, 'references': references}
    except:
        return {'abstract': "None", 'references': "None"}


def getPdfsOfScolarcyLink(referenceLinks):
    refLinks = []
    for reflink in referenceLinks:
        link = reflink.get("oa_query")
        if link is not None:
            refLinks.append(link)
