import logging

import requests
import arxiv


def getReferencedPapers(pdf, justAbstract=True):
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
    if jsonResponse["metadata"].get("doi") is not None:
        crossrefReferences = requests.get('http://api.crossref.org/works/' + jsonResponse["metadata"]["doi"])
    logging.info(f"Found {len(referenceLinks)} refrences in given paper")

    if justAbstract:
        return getAbstracts(referenceLinks)
    else:
        return getPdfs(referenceLinks)


def getAbstracts(referenceLinks):
    abstracts = {}
    for reflink in referenceLinks:
        if reflink.get("crossref") is not None:
            link = reflink.get("crossref")
            doi = link.replace("https://dx.doi.org/", "")
            abstracts[link.replace("https://dx.doi.org/","http://api.crossref.org/works/")] = getAbstractFromDoi(doi)
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
    except: return {'abstract': "None", 'references': "None"}



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
    except: return {'abstract': "None", 'references': "None"}


def getPdfs(referenceLinks):
    refLinks = []
    for reflink in referenceLinks:
        link = reflink.get("oa_query")
        if link is not None:
            refLinks.append(link)


import ssl

# for idx, url in enumerate(refLinks):
#     res = requests.get(url)
#     if (res.headers.get('content-type') == "application/pdf"):
#         try:
#             print(res.url)
#             context = ssl._create_unverified_context()
#             ponse = urllib.request.urlopen(res.url, context=context)
#             file = open(f"{idx}" + ".pdf", 'wb')
#             file.write(ponse.read())
#             file.close()
#             print(file.name)
#         except requests.HTTPError as exception:
#             print(exception)
#             continue


from refextract import extract_references_from_file

# references = extract_references_from_file('2111.10594v1.Misrepresenting_Scientific_Consensus_on_COVID_19_The_Amplification_of_Dissenting_Scientists_on_Twitter.pdf')


# for ref in references:
#   for val in ref:
#      if "arxiv" in val:
#         print(ref)

import requests

# url = 'https://arxiv.org/pdf/cond-mat/9910332.pdf'
# import urllib.request
#
# pdf_path = "https://ref.scholarcy.com/oa_version?query=Barabasi%20Albert%20Emergence%20of%20scaling%20in%20random%20networks%2C%201999"
#
#
# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)
#     file = open(filename + ".pdf", 'wb')
#     file.write(response.read())
#     file.close()
#
#
# download_file(pdf_path, "Test")


# url = "https://arxiv.org/pdf/2111.10594.pdf"
#
# response = requests.get('https://ref.scholarcy.com/api/references/extract', params={"url": url})
# jsonResponse = response.json()
# referenceLinks = jsonResponse["reference_links"]
#getAbstractFromDoi("10.2196/23279")