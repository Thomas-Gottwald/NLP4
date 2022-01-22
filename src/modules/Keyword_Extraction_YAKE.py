import os
import  yake
import pdfplumber
import language_processing as lp
import PDFMiner
import arxiv
from rake_nltk import Rake
from nltk.corpus import stopwords


language = "en"
max_ngram_size = 10
deduplication_thresold = 0.5
deduplication_algo = 'seqm'
windowSize = 3
numOfKeywords = 10

# Load of the several research Papers, sorted by relevance. The 5 best PDF are loaded
search = arxiv.Search( query="nlp keyword extraction",
    max_results=5, sort_by=arxiv.SortCriterion.Relevance)

# Extracting the Abstract of the Papers
pdf_abstract = list()
for result in search.results():
    pdf_abstract.append(result.summary)

# -- Reads the hole document, one special task is that it can read also over two columns
#pdf = PDFMiner.PDFMiner.getPDFText(path_save_pdf + 'Paper_5.pdf')

# -- Preprocessing of the Text
#processed_text = language_processing.preprocessing(text = pdf_abstract[4])
processed_text = lp.remove_stopwords(pdf_abstract[4], stopwords.words('english'))
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