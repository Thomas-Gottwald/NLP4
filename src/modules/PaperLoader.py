import arxiv
import pdfplumber

import nltk

nltk.download('wordnet')


class PaperLoader:
  #returns a set of Papers hosted in arxivDb and returns a set of papers
  def arxivQuery(self):
    search = arxiv.Search(
      query="nlp",
      max_results=10,
      sort_by=arxiv.SortCriterion.SubmittedDate
    )




  #pdf = search.results().__next__().download_pdf()
  with pdfplumber.open("2112.01519v1.Long_range_entanglement_from_measuring_symmetry_protected_topological_phases.pdf") as pdf:
    first_page = pdf.pages[3]
    print(first_page.extract_words())

