import logging

import requests
import arxiv
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def getReferencedPapers(pdf):
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)

    if "http" in pdf:
        logging.info(f"Starting scholarcy request with url: {pdf}")
        response = requests.get('https://ref.scholarcy.com/api/references/extract', params={"url": pdf})
    else:
        print("test")
        logging.info(f"Starting scholarcy request with file: {pdf}")
        with open(pdf, 'rb') as f:
            response = requests.post('https://ref.scholarcy.com/api/references/extract', files={'file': f})

    jsonResponse = response.json()
    referenceLinks = jsonResponse["reference_links"]
    logging.info(f"Found {len(referenceLinks)} refrences in given paper")

    return getAbstracts(referenceLinks)


def getAbstracts(referenceLinks):
    abstracts = {}
    for reflink in referenceLinks:
        if reflink.get("crossref") is not None:
            link = reflink.get("crossref")
            doi = link.replace("https://dx.doi.org/", "")
            abstracts[link.replace("https://dx.doi.org/", "http://api.crossref.org/works/")] = getAbstractFromDoi(doi)
        elif reflink.get("arxiv_url") is not None:
            link = reflink.get("arxiv_url")
            arxivId = link.replace("https://arxiv.org/pdf/", "")
            abstracts[link] = getAbstractFromArxiv(arxivId)
        else:
            link = reflink.get("oa_query")
            if link is None:
                continue
            else:
                response = requests.get(link)
                if response.headers.get('content-type') == "application/pdf":
                    abstracts[response.url] = getAbstractByPdf(response.url)
    logging.info(f"Extracted {len(abstracts)} abstract of {len(referenceLinks)} papers")
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


def getAbstractFromArxiv(arxivId):
    arxivSearch = arxiv.Search(id_list=[arxivId])
    abstract = next(arxivSearch.results()).summary
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
