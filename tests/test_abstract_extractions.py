import src.modules.AbstractExtraction as ae
import os
dirname = os.path.dirname(__file__)


def test_get_abstract_of_reference_extraction():
    reference_list = [{
      "id": "Rytgaard_et+al_2021_a",
      "entry": "RYTGAARD, H. C. & VAN DER LAAN, M. J. (2021). One-step tmle for targeting cause-specific absolute risks and survival curves. arXiv preprint arXiv:2107.01537.  [Titel anhand dieser ArXiv-ID in Citavi-Projekt übernehmen] ",
      "arxiv_url": "https://arxiv.org/pdf/2107.01537"
    }, {
      "crossref": "https://dx.doi.org/10.1126/science.aba9757",
      "id": "Schenck_2021_a",
      "entry": "SCHENCK, E. J., HOFFMAN, K. L., CUSICK, M., KABARITI, J., SHOLLE, E. T. & CAMPION JR, T. R. (2021). Critical care database for advanced research (cedar): An automated method to support intensive care units with electronic health record data. Journal of Biomedical Informatics 118, 103789.",
      "scholar_url": "https://scholar.google.co.uk/scholar?q=Critical%20care%20database%20for%20advanced%20research%20%28cedar%29%3A%20An%20automated%20method%20to%20support%20intensive%20care%20units%20with%20electronic%20health%20record%20data%202021",
      "oa_query": "https://ref.scholarcy.com/oa_version?query=Critical%20care%20database%20for%20advanced%20research%20%28cedar%29%3A%20An%20automated%20method%20to%20support%20intensive%20care%20units%20with%20electronic%20health%20record%20data%202021"
    }]
    abstracts = ae.get_abstracts_of_reference_links(reference_list)
    print(abstracts)
    assert isinstance(abstracts, dict)


def test_get_abstract_of_pdf():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')  # Test non_arxiv Paper
    abstract = ae.get_abstract_by_pdf(pdf)
    assert isinstance(abstract,dict)

    pdf = os.path.join(dirname, 'test_paper/2202.03513.pdf')  # Test paper of arxiv
    abstract = ae.get_abstract_by_pdf(pdf)
    assert isinstance(abstract,dict)

    pdf = os.path.join(dirname, 'test_paper/123.1231.pdf')  # Test error with non existing paper
    abstract = ae.get_abstract_by_pdf(pdf)
    assert isinstance(abstract,dict)


def test_get_abstract_of_pdf_with_references():
    pdf = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    abstract = ae.get_abstract_by_pdf(pdf)
    print(abstract)
    assert isinstance(abstract,dict)

    pdf = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    abstract = ae.get_abstract_by_pdf(pdf)
    print(abstract)
    assert isinstance(abstract, dict)


def test_get_abstract_of_doi():
    doi = "wrong_doi"
    abstract = ae.get_abstract_from_doi(doi)  # Test behavior for wrong DOI
    assert isinstance(abstract,dict)

    doi = "10.1007/BF02946780"  # Test for doi with no references
    abstract = ae.get_abstract_from_doi(doi)
    assert isinstance(abstract, dict)

    doi = "10.1126/science.aba975"
    abstract = ae.get_abstract_from_doi(doi)
    assert isinstance(abstract,dict)
