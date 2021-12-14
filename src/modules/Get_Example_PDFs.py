import arxiv

path_save_pdf = "C:/Users/jan-p/Documents/Uni Wuppertal/Semester 1/NLP/Projekt NLP4/Test_Paper"

search = arxiv.Search(
    query="nlp keyword extraction",
    max_results=5,
    sort_by=arxiv.SortCriterion.Relevance
)
i = 0
for result in search.results():
    i += 1
    print(i,".", result.title)
    result.download_pdf(dirpath= path_save_pdf, filename = 'Paper_'+str(i)+'.pdf') #"%s.pdf"%result.title)

