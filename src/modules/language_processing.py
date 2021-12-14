import nltk
from nltk.stem import PorterStemmer
def preprocessing(text = str("")):
    #Lemmatizer = nltk.stem.WordNetLemmatizer()

    stemmer = PorterStemmer()
    text = nltk.word_tokenize(text)

    text_neu = str('')
    for word in text:
        #print(word)
        text_neu = text_neu + str(stemmer.stem(word)) + ' '

    #print(text_neu)
    #text_neu = nltk.word_tokenize(text_neu)
    #print(text_neu)
    #text_neu = nltk.pos_tag(text_neu)
    #print(text_neu)
    #text_neu = nltk.chunk.ne_chunk(text_neu)
    #print(text_neu)
    return text_neu

#text = 'Your houses are burning, be carefully and then we all go into our homes'
#text_neu = preprocessing(text=text)
