
---
## NLP To the Rescue! (NLP4)

This project is an attempt to create a system which uses natural language processing (NLP) techniques to aid authors in performing systematic literature 
reviews (SLR). This system offers some implementations of NLP techniques like for exeample text similarity and key word extraction.
Herby the current state of the project is focused on aiding the author in the search of relevant studies and the
selection of relevant studies.


## Motivation
Performing a systematic literature review is usually a time-consuming task and can take up to 12 Months [1].
These tasks are for example: 
* Defining the research question
* Search relevant studies
* Select relevant studies
* ... For a full description see: 

One reason an SLR is so time-consuming is that it consists of several tasks which each needs time to fulfill.
Natural language processing has the potential to aid an author in doing these task or even completely automate some of them.

This project should give a starting point for future development of additional NLP techniques to automate or aid the specified tasks
in a SLR.


## Features
As already mentioned the current state of the proposed system, focuses on aiding the author in the search of relevant studies and the
section of relevant studies. 
Therefore we implement the following features:
* Feature list
    * PDF Extraction
    * Abstract Extraction
    * Reference Extraction 
    * Automatic Snowballing (Paper)
    * Paper selection
    * Plot Results
    * Keyword/Keyphrase Extraction
    * Summarization
    * Similarity
    * Preprocessing
    
Most of these features are build upon diverse open source projects.
In the following section we will describe the features and their basis in detail and propose optimization possibilities
for future work.

*All features can be used via the CLI without programming (see CLI section), as well as in code by using the proposed modules as library* 

### PDF extraction
The PDF extraction is implemented with the PDFMiner from https://github.com/pdfminer/pdfminer.six.
It enables the user to extract all text of a PDF in python. An outstanding feature of the PDFMiner is that it recognizes
the layout of the given PDF file and therefore is able to extract text from multicolumn pdf layouts. This is especially relevant
because many scientific papers have a two column layout, which other PDF extraction frameworks we tried failed on.


######Input:
pdfFilenamePath: This Input from type "String" describes the Path of the PDF, from which you want to extract the Text

######Output:
As output, you get the whole Text from the PDF as a string. 

######In code:
```
PDFminer.getPDFtext(pdfFilenamePath="")
```

##### Possible optimization / future work
One problem that occurs with the PDF extraction is that disadvantageous parts of the PDF, which contain no usable information
for our use case, are also extracted. This means for example the title page with the paper contributors etc. or food- / head- notes.
It would be beneficial to analyze ways to remove these parts from the extracted text or recognize them before extracting the text.
This would boost the performance of the NLP techniques like the similarity or keyword extraction when they are used in combination
with the pdf extraction.

### Reference Extraction
This module contains functions to extract references of paper pdfs and their respective abstracts.
Not for all references all 3 of the types are available.

```get_referenced_papers(pdf)```
The Reference Extraction uses the scholarcy REST API extract all references from an uploaded PDF.
The scholarcy reference extraction API returns a JSON string with all references in textual description
as well as different links to the references. These links can be of 3 different types:
* crossref => Is a https://dx.doi.org/ link with the respective doi.
* scholar_url => Is a link leading to the Google Scholar result of the specific paper
* oa_query => Leads either directly to a PDF version of the reference or to the paper page of the publishing journal


##### Input
Link to pdf or Path to local pdf file.
##### Output
Returns a dictionary with following format (If not all link types are available the respective key will be missing):

```json
{
  "id": "Id of refrence in the referencing paper",
  "entry": "Title of references",
  "crossref": "https://www.science.org/doi/10.1126/science.aba9757",
  "scholar_url": "https://scholar.google.co.uk/...", 
  "oa_query": "https://ref.scholarcy.com/...."
}
```

```get_reference_abstracts(pdf)```
Calls the get_refrenced_papers() function and passes the result to the AbstractExtraction.get_abstracts_of_reference_links() links 
to retieve available abstracts from the paper references.
##### Input
Link to pdf or Path to local pdf file.
##### Output
Returns a dictionary with the references link as key and the title, abstract and if the abstract is retrieved from the doi 
also the references (see: Abstractextraction.get_abstract_from_doi) of the respective reference.
```json
{"http://api.crossref.org/works/10.2196/19659": {"title":"paper title", "abstract": "paper abstract",
  "references": [
    {
        "key": "e_1_3_2_21_2",
        "doi-asserted-by": "publisher",
        "DOI": "10.1016/example_doi"
    }]
}
```
If the references for the paper aren't available´, "refernces" will be "None"

```cleanup_reference_abstracts```

### Abstract Extraction
The Abstract Extraction Module implements the following 3 functions to extract abstracts from difrent sources.
```
get_abstract_from_doi(doi)
```
Returns the title, abstract and if available the references of a paper by its given DOI.
To retrieve the abstract a request to the crossref API (see API section) with the given doi is made.
Since the crossref API offers also the references for some papers they are also returned if available.
This is done mainly to safe time in the automatic snowballing.

The crossref API offers abstracts of many free available papers. Nevertheless it is not possible to
retrieve abstracst of all papers by this api. 

######Inputs: 
doi: The digital object identifier (doi) of the paper whichs abstract should be extracted
######Output:
The ouput is a python dictionary with the following format:
```json
{"title": "paper title", "abstract": "paper abstract", "references": [
    {
        "key": "e_1_3_2_21_2",
        "doi-asserted-by": "publisher",
        "DOI": "10.1016/example_doi"
    }
  ]
} 
```

If the references for the paper aren't available´, "refernces" will be "None"


```
get_abstract_from_arxiv_id(arxiv_id)  
```
Returns the abstract and the title of any paper hosted by arXiv.org given by the respective arxiv_id.
To retrieve the abstract the arxiv API is used (See API section).
######Inputs: 
arxiv_id: The arxiv_id of the paper whichs abstract should be extracted
######Output:
The ouput is a python dictionary with the following format:
```json
{"title": "paper title", "abstract": "paper abstract", "references": "None"}
```
Since arXiv doesn't offer referecnes of papers they are not returned like in *get_abstract_from_doi(doi)*.
However the key "references" is filled with "None" to have a consistent output format of across the functions.


```
get_abstract_by_pdf(pdf)
```
This method trys to get the abstracts of a given pdf. 
The function makes a request to the scolarcy api, which then returns either the doi or the arxiv id, whichever is
available. And then uses the respective *get_abstract* function specified above with the received id to return the abstract of the given pdf.
######Inputs: 
pdf: Can either be the path to a local PDF file, or a URL to a PDF file. 
######Output:
The ouput is a python dictionary with the following format:
```json
{"title": "paper title", "abstract": "paper abstract", "references": "None"} if arXiv paper
{"title": "paper title", "abstract": "paper abstract", "references": {"key":"e_1_3_2_21_2","doi-asserted-by":"publisher","DOI":"10.1016/example_doi"}
} if paper with doi
{"title": "None", "abstract": "None", "references": "None"} If neither an arXiv id nor an doi could be extracted from the pdf
```

```
get_abstracts_of_reference_links(pdf)
```
The get_abstracts_of_reference_links function is especially made to retireve the abstracts from the reference_links retrieved of the scholarcy API by the ReferenceExtraction.get_referenced_papers() function.
The function tries to retrieve the abstracts for each retrieved references in the following three diffrent ways:
1. If for the reference a link of type "crossref" (meaning: https://dx.doi.org/10.1126/example_doi) is available, the doi is extracted from the link.
The extracted doi is than passed to the AbstractExtraction.get_abstracts_of_doi() function to retrieve the abstract of the reference.
2. If No croossref link is avaible it is checked if an arxiv link is available. In this case the arXiv_id is extracted is is passed to the AbstractExtract.get_abstract_from_arxiv_id() function to retrieve the title an the abstract of the reference.
3. If none of these links is available the a get request to the "oa_query" link is made. If the "content-type" of the response is application/pdf the response url is passed to the get_abstract_by_pdf() function to try to extract the abstract from the pdf url. 
If none of these 3 steps is succesfull no abstract for the reference is extracted.





### Paper Search
#### Automatic Snowballing 
The automatic snowballing feature performs a full automized forward snowballing, by measuring the similarity of abstracts
of the references of papers in a given snowballing seed set, with the abstracts of all the papers in the seed set.
If the similarity of a refrence with any of the seed set abstracts is higher than threshold *t*, the reference will
be added to the seed set as well. This is done for user specified number of iterations.

The starting seed set must consist of PDF files located in a specified folder. The papers in the seed set should be preselected papers of high relevance
for your research topic.
````
snowballing(seed_set_path, iterations, similarity_threshold)
````
##### *Input*

##### *Output*


The snowballing function starts by extracting the abstracts of the seed set papers by using the *get_abstract_by_pdf()* function of the
*AbstractExtraction* module and adding them to the *corpus_set* variable. After extracting the seed set abstracts, the refrences of the seed set 
and their respective abstracts are extracted by using the *get_reference_abstracts* function of the *ReferenceExtraction* module.
The reference abstracts are added to the *querry_set* variable. Then the *corpus_set* and the *querry_set* are passed as parameters to the
 *get_similar_references* method of the Similarities module to retrieve the similiraty of every retrieved abstract with every seed set abstract.
Those references that exceed the specified similiraty threshold are than added to two dictioniarys. The *result_set* and the *new_set*.
The snowballing prcoess is then continued in a while loop for the given number of iterations where in every iteration the *new_set* is appenden to the
*corpus_set*


### Paper Selection
This file contains two functions "paper_importance" and "plot_paper_selection" which can be used to select papers on the
basis of the similarity between the query and the papers you are interested in, and it can show the result in a plot. 
####paper_importance
```
PaperSelection.paper_importance(text=[], keywords=[])
```
This function makes it possible to compare Keywords or a research topic with one or more texts. Therefore, it uses the
keywords and the text and calculates the cosines similarity of those. As result, you get a value for of each keyword 
relating to all the papers you hand over the function.
######Inputs: 
text: The attribute takes a list of texts (strings). So it is possible to calculate the similarity between more than just 
one text. -> much more efficient. You can use a whole text, phrases or just the abstract. Feel free to try!

keywords: Also the attribute "keywords" is a list of strings. Those can represent a list of single keywords, phrases or sentences.
Which get compared with the list of texts you hand over.
######Output:
The function returns a dataframe from pandas. In this you have in  one axis the texts and on the other the several keywords.
It is a matrix where you can find the evaluation of all the papers and keywords.
####plot_paper_selection
```
PaperSelection.plot_paper_selection(df=pd.DataFrame())
```
This function makes it possible to plot the results from the function "paper_importance". This function creates an 
interactive plot, where in the x-axe are shown the several keywords and on the y-axe the score regarding the paper.
The different papers are shown in single traces on this plot. Since it is an interactive plot, it is possible to
inactivate or activate the single traces. 
######Inputs: 
The input is a dataframe, which contains the results of the "paper_importance". 
Just hand over the return of this function. 
######Output:
The function returns the object file of the plot. So it is possible to handle this or to save it afterwards. 
##### Possible optimization / future work
1. Probably it would be nice to implement a plot methode to all other functions, so it would be easy to evaluate 
them and have a good overview. 
2. Right now we assume that it doesn´t matter if we use keywords or a whole sentence to compare it with the text. 
It might be good the implement several functions. One for words ->Bert and the other for sentence -> SBert



###Keyword/Keyphrase Extractor
This file contains two methods, the "yake_extraction" and the "rake_phrase_extraction" both can be used to extract 
keyphrases but for single keyword extraction you can only use the "yake_extraction".


####yake_extraction
The yake extraction provides more than on possibility to extract keywords from the text. The function has a lot of input 
parameter. With them, it is possible to define a lot of properties. 
```
yake_extraction(text, number_of_keyphrases=10, language='en', words_in_keyphrase=10, deduplication_threshold=0.5)
```
######Inputs: 
text:This Parameter is the String where you want to extract the keywords/phrases.

number_of_keyphrases: With that integer you can define how many keywords/phrases you want to extract.

language: This string defines the language of the text, where you want to extract the data.

words_in_keyphrase: This Parameter is an integer which defines the number of words in a keyphrase. If you actually want 
to extract single keywords you might use the value "1" otherwise you get longer phrases.

deduplication_threshold: With that threshold it is possible to finetune the extraction. So that the several Keyphrases 
consists out of duplication. 
E.g.1 threshold -> low [Keyword, Keyword Extraction, Keywords out of text]
E.g.2 threshold -> high [Keyword, Extraction, Words out of text]

######Output:
As output this function returns a dictionary of all the phrases which you defined with "number_of_keyphrases" and the 
score of it. 
####rake_phrase_extraction
This function is a simple implementation to extract keyphrases out of an text. There are no more variables to define. 
```python 
rake_phrase_extraction(text, number_of_keywords=10)
```
######Inputs: 
The input of this function is first the text(string) where you want to extract the keyphrases from. The other input 
"number_of_keywords" is the number how many phrases you want to return.  
######Output:
As output this function returns a list of all the phrases which you defined with "number_of_keywords" and the 
score of it. 

##### Possible optimization / future work
1. One important task might be to evaluate the functionality of the extractors. 
2. Also it would be great to find out, which form of text works best. -> Just the abstract, the hole text and so on. 

### Summarization
The summarization function is implemented with the function from
https://gist.github.com/edubey/cc41dbdec508a051675daf8e8bba62c5 it creates a summarization out of a text. Therefor it 
builds up a similarity matrix between all sentences and the text and takes the most valued sentences as sentences for
the summarization. This file contain four functions for that: read_article, sentence_similarity, build_similarity_matrix
and generate_summary.

####read_article
This function reads the text and parse it into the single sentences and also it removes special characters out of the 
string.
```python 
read_article(text)
```
######Input
The input of this function is a text(string) that you want to summarize.
######Output
As an output it returns a list of all sentences without the special symbols in it.

####sentence_similarity
This function compares two sentences with each other and returns a value of the similarity of those both. Also it removes 
stopwords out of the sentences. This function is used to build up the similarity matrix. 
```python 
sentence_similarity(sent1, sent2, stopwords=None)
```
######Input
sent1: Is a string of sentence one.

sent2: Is a string of sentence two.

stopwords: This parameter can be a list where you can hand over the stopwords you want to remove.
######Output
The return of this function is a value, which represent the similarity of the two sentences above.

####build_similarity_matrix
The function gets the list of all sentences and calculates for all of them the similarity to build the matrix.
```python 
build_similarity_matrix(sentences, stop_words)
```
######Input
sentences: This is a List of all sentences and should be the return of the function "read_article"

stopwords: Here you can hand over a list of stopwords which get removed before calculating the similarity.
If the value is "none" no stopwords got removed.
######Output
The function returns a matrix in the size of (len(sentences) x len(sentences)) 

####generate_summary
This function concate all the other functions above. So you just need to call a single function to create a summary. 
```python 
generate_summary(file_name, top_n=5)
```
######Input
file_name: This is the input to give the function the Text you want to summarize

top_n: This parameter defines how long your summarize gonna be. E.g. top_n = 5, creates a summary out of the 5 highest
valued. 
######Output
The function returns the summary as a string.

###Similarity


###Text Preprocessing
This file is a implementation of some nltk functions to preprocess the text which you want to work with. This is not
always necessary, because some of those steps are already implemented in the other functions. 
Preprocessing steps: tokenize, remove_stopwords, lemmatizing, port_stemmer and position_tag. 

###tokenize
This function tokenize the text from the input.
```python 
tokenize(text)
```
######Input
text: String of the text which should be tokenized.
######Output
Returns a list with all tokens.
###remove_stopwords
```python 
remove_stopwords(text=str(""), stops=[])
```
######Input
text: This input parameter is a string from where the stopwords going to be removed. 

stops: Is a list with all the words you want to remove.
######Output

###lemmatizing
This function creates lemmas out of single words. 
```python 
lemmatizing(text=str(''))
```
######Input
text: This parameter is a string, which is going to be split up by the tokenize function
######Output
The output is a text with lemmas, no words.

###port_stemmer 
This function stems all words out of an text.
```python 
port_stemmer(text=str(''))
```
######Input
text: String that contains the text where the words are going to be stemmed. 
######Output
This function returns a text with stemmed words. 

###position_tag
This methode tags all the words in a text. E.g. Verb, adjective ...
```python 
position_tag(text)
```
######Input
text: String that contains the text where the words are going to be tagged.
######Output
Returns a text with all words and the relating tags. 


## Installation

Provide step-by-step examples and descriptions of how to set up a development environment.

## API reference
For small projects with a simple enough API, include the reference docs in this README. For medium-sized and larger
projects, provide a link to the API reference docs.

## Tests (optional: only if you have tests)
Describe and show how to run the tests with code examples.

## How to use and extend the project? (maybe)
Include a step-by-step guide that enables others to use and extend your code for their projects. Whether this section
is required and whether it should be part of the `README.md` or a separate file depends on your project. 
If the **very short** `Code Examples` from above comprehensively cover (despite being concise!) all the major 
functionality of your project already, this section can be omitted. **If you think that users/developers will need more 
information than the brief code examples above to fully understand your code, this section is mandatory.** If your 
project requires significant information on code reuse, place the information into a new `.md` file.

## Results
If you performed evaluations as part of your project, include your preliminary results that you also show in your final
project presentation, e.g., precision, recall, F1 measure and/or figures highlighting what your project does. 
If applicable, briefly describe the dataset your created or used first before presenting the evaluated use cases 
and the results.

If you are about to complete your thesis, include the most important findings (precision/recall/F1 measure) and refer 
to the corresponding pages in your thesis document.

## License
Include the project's license. Usually, we suggest MIT or Apache. Ask your supervisor. For example:

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with 
the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an 
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License

## License of this readme-template (remove this once you replaced this readme-template with your own content)
This file itself is partially based on [this file](https://gist.github.com/sujinleeme/ec1f50bb0b6081a0adcf9dd84f4e6271). 
