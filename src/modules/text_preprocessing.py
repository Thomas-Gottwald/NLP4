from nltk.stem import PorterStemmer
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def remove_stopwords(text=str(""), stops=[]):
    stopword = stops
    filtered_text = ''
    tokens = nltk.word_tokenize(text)
    for w in tokens:
        if w.lower() in stopword:
            continue
        else:
            filtered_text = filtered_text + w + ' '

    return filtered_text


def lemmatizing(text=str('')):
    nltk.download('omw-1.4')
    text_neu = ""
    text = nltk.word_tokenize(text)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for word in text:
        text_neu = text_neu + str(lemmatizer.lemmatize(word)) + ' '

    return text_neu


def port_stemmer(text=str('')):
    text_neu = ""
    text = nltk.word_tokenize(text)
    stemmer = PorterStemmer()
    for word in text:
        text_neu = text_neu + str(stemmer.stem(word)) + ' '

    return text_neu


def position_tag(text):
    tokens = nltk.word_tokenize(text)
    text_neu = nltk.pos_tag(tokens)
    return text_neu
