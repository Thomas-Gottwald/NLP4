import json
import os
import re
import src.modules.AbstractExtraction as ae
import src.modules.SearchStudies


def test_get_abstract_of_reference_extraction():
    reference_list = [{
      "id": "Rytgaard_et+al_2021_a",
      "entry": "RYTGAARD, H. C. & VAN DER LAAN, M. J. (2021). One-step tmle for targeting cause-specific absolute risks and survival curves. arXiv preprint arXiv:2107.01537.  [Titel anhand dieser ArXiv-ID in Citavi-Projekt übernehmen] ",
      "arxiv_url": "https://arxiv.org/pdf/2107.01537"
    },
    {
      "crossref": "https://dx.doi.org/10.1126/science.aba9757",
      "id": "Schenck_2021_a",
      "entry": "SCHENCK, E. J., HOFFMAN, K. L., CUSICK, M., KABARITI, J., SHOLLE, E. T. & CAMPION JR, T. R. (2021). Critical care database for advanced research (cedar): An automated method to support intensive care units with electronic health record data. Journal of Biomedical Informatics 118, 103789.",
      "scholar_url": "https://scholar.google.co.uk/scholar?q=Critical%20care%20database%20for%20advanced%20research%20%28cedar%29%3A%20An%20automated%20method%20to%20support%20intensive%20care%20units%20with%20electronic%20health%20record%20data%202021",
      "oa_query": "https://ref.scholarcy.com/oa_version?query=Critical%20care%20database%20for%20advanced%20research%20%28cedar%29%3A%20An%20automated%20method%20to%20support%20intensive%20care%20units%20with%20electronic%20health%20record%20data%202021"
    }]
    anstracts = ae.get_abstracts_of_reference_links(reference_list)
    print(anstracts)
    print(src.modules.SearchStudies.cleanup_reference_abstracts(anstracts))
    assert isinstance(anstracts, dict)


def test_get_abstract_of_pdf():
    pdf = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\starter_set\\15.pdf"
    abstract = ae.get_abstract_by_pdf(pdf)
    print(abstract)
    assert isinstance(abstract,str)

def test_get_abstract_of_pdf_with_references():
    pdf = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\modules\\rsos.201199.pdf"
    abstract = ae.get_abstract_by_pdf(pdf, with_references=True)
    print(abstract)
    assert isinstance(abstract,dict)

    pdf = "C:\\Users\\fabia\PycharmProjects\\NLP4\\src\\starter_set\\2202.03513.pdf"
    abstract = ae.get_abstract_by_pdf(pdf, with_references=True)
    print(abstract)
    assert isinstance(abstract, dict)



