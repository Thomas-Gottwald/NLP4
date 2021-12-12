import arxiv
import pdfplumber


class PaperLoader:
  def arxivQuery(self):
    search = arxiv.Search(
      query="covid-19",
      max_results=10,
      sort_by=arxiv.SortCriterion.SubmittedDate
    )




