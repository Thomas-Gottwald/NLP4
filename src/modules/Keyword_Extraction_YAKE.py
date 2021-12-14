import os
import  yake
import pdfplumber
import language_processing
import PDFMiner
import arxiv
from rake_nltk import Rake

'''''
with pdfplumber.open(path_save_pdf) as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])
pdf.
'''

path_save_pdf = "C:/Users/jan-p/Documents/Uni Wuppertal/Semester 1/NLP/Projekt NLP4/Test_Paper/Paper_5.pdf"

language = "en"
max_ngram_size = 1
deduplication_thresold = 0.5
deduplication_algo = 'seqm'
windowSize = 3
numOfKeywords = 10


search = arxiv.Search(
    query="nlp keyword extraction",
    max_results=5,
    sort_by=arxiv.SortCriterion.Relevance
    )

pdf_abstract = list()
for result in search.results():
    pdf_abstract.append(result.summary)

#pdf = PDFMiner.PDFMiner.getPDFText(path_save_pdf + 'Paper_5.pdf')

#processed_text = language_processing.preprocessing(text = pdf_abstract[4])
processed_text = pdf_abstract[4]

print(processed_text)
print('-----------Yake Keywords---------------------------------------------')
keyword_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = keyword_extractor.extract_keywords(processed_text)
for keyword in keywords:
    print(keyword)
print('-----------Rake Keywords---------------------------------------------')
keyword_extractor = Rake()
keyword_extractor.extract_keywords_from_text(processed_text)
phrases = keyword_extractor.get_ranked_phrases_with_scores()[:numOfKeywords]
#keyword_extractor.
for keyword in phrases:
    print(keyword)