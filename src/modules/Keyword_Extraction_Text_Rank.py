import os
import  yake
import PDFMiner
import language_processing
from rake_nltk import Rake

path_save_pdf = "C:/Users/jan-p/Documents/Uni Wuppertal/Semester 1/NLP/Projekt NLP4/Test_Paper/"

pdf = PDFMiner.PDFMiner.getPDFText(path_save_pdf + 'Paper_5.pdf')




keyword_extractor = Rake()
keyword_extractor.extract_keywords_from_text(pdf)
phrases = keyword_extractor.get_ranked_phrases_with_scores()

for keyword in phrases:
    print(keyword)