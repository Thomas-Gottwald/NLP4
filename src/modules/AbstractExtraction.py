import requests
import arxiv
import logging


def get_abstract_from_arxiv_id(arxiv_id):
    arxiv_search = arxiv.Search(id_list=[arxiv_id])
    abstract = next(arxiv_search.results()).summary
    return abstract


def get_abstract_from_doi(doi, with_references = False):
    print(doi)
    try:
        requestAbs = requests.get('http://api.crossref.org/works/' + doi).json()
        abstract = requestAbs["message"].get("abstract", "None")
        if with_references:
            if requestAbs["message"].get("reference") is not None:
                references = requestAbs["message"].get("reference")
            else:
                references = "None"
            return {'abstract': abstract, 'references': references}
        else:
            return abstract
    except:
        if with_references:
            return {'abstract': "None", 'references': "None"}
        else:
            return 'None'


def get_abstract_by_pdf(pdf, with_references = False):
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
            return get_abstract_from_doi(doi, with_references=with_references)
        elif meta.get("arxiv") is not None:
            arxivId = meta.get("arxiv")
            if with_references:
                return {'abstract': get_abstract_from_arxiv_id(arxivId), 'references': "None"}
            return get_abstract_from_arxiv_id(arxivId)
        elif with_references:
            return {'abstract': "None", 'references': "None"}
        else:
            return "None"
    except:
        if with_references:
            return {'abstract': "None", 'references': "None"}
        else:
            return 'None'


def get_abstracts_of_reference_links(reference_links):
    abstracts = {}
    for reflink in reference_links:
        if reflink.get("crossref") is not None:
            link = reflink.get("crossref")
            doi = link.replace("https://dx.doi.org/", "")
            abstracts[link.replace("https://dx.doi.org/", "http://api.crossref.org/works/")] = get_abstract_from_doi(doi,with_references=True)
        elif reflink.get("arxiv_url") is not None:
            link = reflink.get("arxiv_url")
            arxiv_id = link.replace("https://arxiv.org/pdf/", "")
            abs_ref = {'abstract': get_abstract_from_arxiv_id(arxiv_id), 'references': "None"}
            abstracts[link] = abs_ref
        else:
            link = reflink.get("oa_query")
            if link is None:
                continue
            else:
                try:
                    response = requests.get(link)
                    if response.headers.get('content-type') == "application/pdf":
                        abstracts[response.url] = get_abstract_by_pdf(response.url,with_references=True)
                except requests.exceptions.RequestException:
                    continue
    logging.info(f"Extracted {len(abstracts)} abstract of {len(reference_links)} papers")
    return abstracts


