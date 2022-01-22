import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def remove_stopwords(text = str(""), stopwords = []):
    filtered_text = ''
    tokens = nltk.word_tokenize(text)
    for w in tokens:
        if w.lower() in stopwords:
            continue
        else:
            filtered_text = filtered_text + w + ' '

    return filtered_text


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
