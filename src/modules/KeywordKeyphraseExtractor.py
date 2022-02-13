import yake
from rake_nltk import Rake


def yake_extraction(text, number_of_keyphrases=10, language='en', words_in_keyphrase=10, deduplication_threshold=0.5):
    keyword_extractor = yake.KeywordExtractor(lan=language, n=words_in_keyphrase, dedupLim=deduplication_threshold,
                                              top=number_of_keyphrases)
    phrases = keyword_extractor.extract_keywords(text)
    print('-----------Yake Key-phrases---------------------------------------------')
    for phrase in phrases:
        print(phrase)
    return phrases


def rake_phrase_extraction(text, number_of_keywords=10):
    num_keywords = number_of_keywords
    keyword_extractor = Rake()
    keyword_extractor.extract_keywords_from_text(text)

    phrases = keyword_extractor.get_ranked_phrases()[:num_keywords]
    print('-----------Rake Key-phrases---------------------------------------------')
    for phrase in phrases:
        print(phrase)
    return phrases



