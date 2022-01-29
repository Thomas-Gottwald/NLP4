import arxiv



class PaperLoader:
  #returns a set of Papers hosted in arxivDb and returns a set of papers
  def arxivQuery(self):
    search = arxiv.Search(
      query="nlp",
      max_results=10,
      sort_by=arxiv.SortCriterion.SubmittedDate
    )




