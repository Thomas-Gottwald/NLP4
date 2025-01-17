
---
## NLP To the Rescue! (NLP4)

This project is an attempt to create a system which uses natural language processing (NLP) techniques to aid authors in performing systematic literature 
reviews (SLR). This system offers some implementations of NLP techniques like for example text similarity and key word extraction tailored for the use in a SLR.
Hereby the current state of the project is focused on aiding the author in the search of relevant studies and the
selection of relevant studies.


## Motivation
Performing a systematic literature review is usually a time-consuming task and can take up to 12 Months ([Feng et al, 2017](https://ieeexplore.ieee.org/document/8305926)).
These tasks are for example: 
* Defining the research question
* Search relevant studies
* Select relevant studies
* Extract data from studies  
For more details about the specific task in an SLR see: [https://flexiblelearning.auckland.ac.nz/philson/47.html](https://flexiblelearning.auckland.ac.nz/philson/47.html)

Natural language processing has the potential to aid an author in doing these task or even completely automate some of them and thereby
reduce the time to conduct a full SLR.

This project should give a starting point for future development of additional NLP techniques to automate or aid the specified tasks
in a SLR.


## Features
As already mentioned the current state of the proposed system, focuses on aiding the author in the search of relevant studies and the
section of relevant studies. 
Therefore we implement the following features:
* Feature list
    * [PDF Extraction](#PDF-extraction)
    * [Abstract Extraction](#Abstract-Extraction)
    * [Reference Extraction](#Reference-Extraction)
    * [Similarity](#Similarities)
    * [Automatic Snowballing (Paper Search)](#Paper-Search)
    * [Paper selection](#Paper-Selection)
    * [Plot Results](#plot_paper_selection)
    * [Keyword/Keyphrase Extraction](#Keyword/Keyphrase-Extractor)
    * [Summarization](#Summarization)
    * [Preprocessing](#Text-Preprocessing)
    
Some of these features are build upon diverse open source projects.
In the following section we will describe the features and their basis in detail and propose optimization possibilities
for future work.

*All features can be used via the CLI without programming (see [CLI section](#Command-line-interface-(cli))), as well as in code by using the proposed modules as library* 

### PDF extraction
The PDF extraction is implemented with the PDFMiner from https://github.com/pdfminer/pdfminer.six.
It enables the user to extract all text of a PDF in python. An outstanding feature of the PDFMiner is that it recognizes
the layout of the given PDF file and therefore is able to extract text from multicolumn pdf layouts. This is especially relevant
because many scientific papers have a two column layout, which other PDF extraction frameworks we tried failed on.

#### get_PDF_text
```python 
getPDFtext(pdfFilenamePath="")
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>  
*pdfFilenamePath*: This Input from type "String" describes the Path of the PDF, from which you want to extract the Text

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
As output, you get the whole Text from the PDF as a string. 



#### Possible optimization / future work
One problem that occurs with the PDF extraction is that disadvantageous parts of the PDF, which contain no usable information
for our use case, are also extracted. This means for example the title page with the paper contributors etc. or food- / head- notes.
It would be beneficial to analyze ways to remove these parts from the extracted text or recognize them before extracting the text.
This would boost the performance of the NLP techniques like the similarity or keyword extraction when they are used in combination
with the pdf extraction.

### Reference Extraction
This module contains functions to extract references of paper pdfs and their respective abstracts.

#### get_referenced_papers
```python 
get_referenced_papers(pdf)
```

The Reference Extraction uses the [scholarcy](#API-reference) API to extract all references from an uploaded PDF.
The scholarcy reference extraction API returns a JSON string with all references in textual description
as well as different links to the references. These links can be of 3 different types:
* crossref => Is a https://dx.doi.org/ link with the respective doi.
* scholar_url => Is a link leading to the Google Scholar result of the specific paper
* oa_query => Leads either directly to a PDF version of the reference or to the paper page of the publishing journal

* Not for all references all 3 of the types are available.

<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*pdf:* Link to pdf or Path to local pdf file.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns a dictionary with following format (If not all link types are available the respective key will be missing):

```json
{
  "id": "Id of reference in the referencing paper",
  "entry": "Title of references",
  "crossref": "https://www.science.org/doi/10.1126/science.aba9757",
  "scholar_url": "https://scholar.google.co.uk/...", 
  "oa_query": "https://ref.scholarcy.com/...."
}
```
#### get_reference_abstracts
```python 
get_reference_abstracts(pdf)
```
Calls the [get_referenced_papers()](#get_referenced_papers) function and passes the result to the [AbstractExtraction.get_abstracts_of_reference_links()](#get_abstracts_of_reference_links) links 
to retrieve available abstracts from the paper references.

**<span style="font-size:15px;">Input:</span>**   
*pdf*: Link to pdf or Path to local pdf file.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns a dictionary with the references link as key and the title, abstract and if the abstract is retrieved from the doi 
also the references (see: [Abstractextraction.get_abstract_from_doi](#get_abstract_from_doi)) of the respective reference.
```json
{"http://api.crossref.org/works/10.2196/19659": {"title":"paper title", "abstract": "paper abstract",
  "references": [
    {
        "key": "e_1_3_2_21_2",
        "doi-asserted-by": "publisher",
        "DOI": "10.1016/example_doi"
    }]
}}
```
If the references for the paper aren't available´, "reference" will be "None"

### Abstract Extraction
The Abstract Extraction Module implements the following 4 functions to extract abstracts from different sources.
#### get_abstract_from_doi
```python 
get_abstract_from_doi(doi)
```
Returns the title, abstract and if available the references of a paper by its given DOI.
To retrieve the abstract a request to the crossref API [(see API section)](#api-reference) with the given doi is made.
Since the crossref API offers also the references for some papers they are also returned if available.
This is done mainly to safe time in the automatic snowballing.

The crossref API offers abstracts of many free available papers. Nevertheless, it is not possible to
retrieve abstract of all papers by this api. 

<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*doi*: The digital object identifier (doi) of the paper which abstract should be extracted

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The output is a python dictionary with the following format:
```json
{"title": "paper title", "abstract": "paper abstract", "references": [
    {
        "key": "e_1_3_2_21_2",
        "doi-asserted-by": "publisher",
        "DOI": "10.1016/example_doi"
    }]
} 
```

If the references for the paper aren't available, "reference" will be "None"

#### get_abstract_from_arxiv_id
```python 
get_abstract_from_arxiv_id(arxiv_id)  
```
Returns the abstract and the title of any paper hosted by arXiv.org given by the respective arxiv_id.
To retrieve the abstract the arxiv API is used [(see API section)](#api-reference).

<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*arxiv_id*: The arxiv_id of the paper which's abstract should be extracted

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The output is a python dictionary with the following format:
```json
{"title": "paper title", "abstract": "paper abstract", "references": "None"}
```
Since arXiv doesn't offer references of papers they are not returned like in [*get_abstract_from_doi(doi)*](#get_abstract_from_doi).
However, the key "references" is filled with "None" to have a consistent output format of across the functions.

#### get_abstract_by_pdf
```python 
get_abstract_by_pdf(pdf)
```
This method trys to get the abstracts of a given pdf. 
The function makes a request to the scolarcy api, which then returns either the doi or the arxiv id, whichever is
available. And then uses the respective *get_abstract* function specified above with the received id to return the abstract of the given pdf.

<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*pdf*: Can either be the path to a local PDF file, or a URL to a PDF file. 

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The output is a python dictionary with the following format:
```python
{"title": "paper title", "abstract": "paper abstract", "references": "None"} # if arXiv paper
{"title": "paper title", "abstract": "paper abstract", "references": {"key":"e_1_3_2_21_2","doi-asserted-by":"publisher","DOI":"10.1016/example_doi"}
} # if paper with doi
{"title": "None", "abstract": "None", "references": "None"} # If neither an arXiv id nor an doi could be extracted from the pdf
```

#### get_abstracts_of_reference_links
```python  
get_abstracts_of_reference_links(pdf)
```
The get_abstracts_of_reference_links function is especially made to retrieve the abstracts from the reference_links retrieved of the scholarcy API by the [ReferenceExtraction.get_referenced_papers()](*get_referenced_papers*) function.
The function tries to retrieve the abstracts for each retrieved references in the following three different ways:
1. If for the reference a link of type "crossref" (meaning: https://dx.doi.org/10.1126/example_doi) is available, the doi is extracted from the link.
The extracted doi is than passed to the [AbstractExtraction.get_abstracts_of_doi()](#get_abstract_from_doi) function to retrieve the abstract of the reference.
2. If No crossref link is available it is checked if an arxiv link is available. In this case the arXiv_id is extracted is passed to the [AbstractExtract.get_abstract_from_arxiv_id()](#get_abstract_from_arxiv_id) function to retrieve the title and the abstract of the reference.
3. If none of these links is available a get request to the "oa_query" link is made. If the "content-type" of the response is application/pdf the response url is passed to the [AbstractExtraction.get_abstract_by_pdf()](#get_abstract_by_pdf) function to try to extract the abstract from the pdf url. 
If none of these 3 steps is successful no abstract for the reference is extracted.
In case one of the steps is successful the retrieved abstract will be added to a dictionary with the respective link as key and the respective abstract dictionary as value.


<ins>**<span style="font-size:13px;">Input:</span>**</ins>  
*reference_links*: Input should be the output of the ReferenceExtraction.get_referenced_papers() function

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Ouput is a dictionary with the following format:
```json
 {"http://api.crossref.org/works/10.1126/science.aba9757": {"title": "paper title", "abstract": "paper abstract", "references": {"key":"e_1_3_2_21_2","doi-asserted-by":"publisher","DOI":"10.1016/example_doi"}},
  "https://arxiv.org/pdf/1706.05924.pdf": {"title": "paper title", "abstract": "paper abstract", "references": "None"}
 }
```
##### Possible optimization / future work
Since the current approach to extract papers from pdf files is quite slow, due to the fact that we need to request first the 
scholarcy api and then either the crossref or arxiv api, it would be useful to find a solution to extract the abstracts directly
from the pdf files.

### Similarities
The similarities module implements the [sentence-transformers/allenai-specter](https://huggingface.co/sentence-transformers/allenai-specter) model, which is an implementation of the [SPECTER-Model](https://arxiv.org/abs/2004.07180).
The SPECTER-Model is a transformer to generate document-level embeddings of scientific documents based on [Sci-BERT](https://arxiv.org/abs/1903.10676).
It is trained with consideration of the relatedness of scientific documents citing each other. This means that the embedding representations of papers are closer
to each other when one cites the other.

The  [sentence-transformers/allenai-specter](https://huggingface.co/sentence-transformers/allenai-specter) implementation
of the SPECTER-Model enables to create SPECTER embeddings of titles and abstracts of papers.


#### specter_query_reference_similarity
```python 
specter_query_reference_similarity(corpus_set, query_set)
```
This function generates the SPECTER embeddings and calculates the cosine similarity of each reference in query_set
with each reference in the corpus set and return the similarities. It uses the sentence_transformers.util.semantic_search
from the [sentence-transformers/allenai-specter](https://huggingface.co/sentence-transformers/allenai-specter) model for this. 

<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*corpus_set:* List of dictionary's containing title and abstract of papers
```json
[{"title": "paper title", "abstract": "paper abstract", "references": {"key":"e_1_3_2_21_2","doi-asserted-by":"publisher","DOI":"10.1016/example_doi"}},
{"title": "paper title", "abstract": "paper abstract", "references": "None"}]
```
*query_set: Dictionary containing paper id's as key and title and abstract as value* 
```json
{"10.1177/0093650214565914": {
            "title": "Paper title",
            "abstract": "Paper abstract"},
  "10.117/9090": "..."
}
```

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Output is a dictionary containing the similarity score of each query_set paper with each corpus_set paper with the following format:
```json
{"10.1177/0093650214565914": [[{"corpus_id": 0, "score": 0.8752286434173584}, {"corpus_id": 1, "score": 0.6487678289413452}]]}
```

#### specter_1to1_cosine
```python 
specter_1to1_cosine(first, second)
```
Creates the SPECTER embeddings of two passed strings and returns their cosine similarity

<ins>**<span style="font-size:13px;">Input:</span>**</ins>     
*first*: First string for comparison  
*second*: Second string for comparison

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns similarity of both strings as float number.

#### pdf_similarity
```python 
pdf_similarity(first, second, only_abstract=False)
```
Creates the SPECTER embeddings of two passed PDFs and returns their cosine similarity.

<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*first*: First string for comparison  
*second*: Second string for comparison  
*only_abstract*: If true it will first try to extract the abstracts of the specified pdf and only calculate the
similarity of the abstracts.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns similarity of both pdfs/abstracts as float number.


### Paper Search
#### Automatic Snowballing 
The automatic snowballing feature performs a full automized forward snowballing, by measuring the similarity of abstracts
of the references of papers in a given snowballing seed set, with the abstracts of all the papers in the seed set.
If the similarity of a reference abstract with any of the seed set abstracts is higher than a threshold *similarity_threshold*, the reference will
be added to the seed set as well. This is done for a user specified number of iterations.
Unfortunately the snowballing is quite slow at the moment and needs about three to five minutes per paper per iteration (Also depending on
the numbers of references the papers have). 

The starting seed set must consist of PDF files located in a specified folder. The papers in the seed set should be preselected papers of high relevance
for your research topic.
```python 
snowballing(seed_set_path, iterations, min_similarity=0.85, result_file="snowballing_result.json")
```
The snowballing function starts by extracting the abstracts of the seed set papers by using the [*get_abstract_by_pdf()*](#get_abstract_by_pdf) function of the
*AbstractExtraction* module and adding them to the *corpus_set* variable. After extracting the seed set abstracts, the references of the seed set 
and their respective abstracts are extracted by using the [*get_reference_abstracts*](#get_reference_abstracts) function of the *ReferenceExtraction* module.
The reference abstracts are added to the *query_set* variable. Then the *corpus_set* and the *query_set* are passed as parameters to the
 [*get_similar_references*](#get_similar_references) function to retrieve the similarity of every retrieved abstract with every seed set abstract.
Those references that exceed the specified similarity threshold are than added to two dictionary. The *result_set* and the *new_set*.
The snowballing process is then continued in a while loop for the given number of iterations where in every iteration the *new_set* is appended to the
*corpus_set*

**<span style="font-size:15px;">Input:</span>**   
*seed_set_path*: Path to the folder containing the papers to start with(the seed set)  
*iterations*: Number of iterations to for the snowballing process  
*min_similarity*: Minimum similarity a reference needs to have with the seed set to be taken up in the *result_set*  
*result_file*: A path to a json file in with the result should be saved  

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Save the json result of the snowballing in the *result_file* 

#### get_similar_references
```python 
get_similar_references(corpus_set, query_set, min_similarity):
```
Calculates the similarity's of each *query_set* (the new_references) paper with each *corpus_set* (seed_set/current result_set) paper
and only returns those papers of the *query_set* (with their achieved similarity) that have a higher similarity than min_similarity with one of the *corpus_set*
papers.

**<span style="font-size:15px;">Input:</span>**   
*corpus_set:* List of dictionary's containing title and abstract of papers
```json
[{"title": "paper title", "abstract": "paper abstract", "references": {"key":"e_1_3_2_21_2","doi-asserted-by":"publisher","DOI":"10.1016/example_doi"}},
{"title": "paper title", "abstract": "paper abstract", "references": "None"}]
```
*query_set: Dictionary containing paper id's as key and title and abstract as value* 
```json
{"10.1177/0093650214565914": {
            "title": "Paper title",
            "abstract": "Paper abstract"},
  "10.117/9090": "..."
}
```
*min_similarity*: Minimum similarity to return the reference

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns a dictionary with each paper of the query_set that exceeds the min_similarity with one of the corpus_set papers:
```json
{
  "10.1177/0093650214565914": {
    "title": "Test Title",
    "abstract": " This study joins a growing body of research that demonstrates the behavioral consequences of hostile media perceptions. Using survey data from a nationally representative U.S. sample, this study tests a moderated-mediation model examining the direct and indirect effects of hostile media perceptions on climate change activism. The model includes external political efficacy as a mediator and political ideology and internal political efficacy as moderators. The results show that hostile media perceptions have a direct association with climate activism that is conditioned by political ideology: Among liberals, hostile media perceptions promote activism, whereas among conservatives, they decrease activism. Hostile media perceptions also have a negative, indirect relationship with activism that is mediated through external political efficacy; however, this relationship is conditioned by both ideology and internal political efficacy. Specifically, the indirect effect manifests exclusively among conservatives and moderates who have low internal efficacy. Theoretical, normative, and practical implications are discussed. ",
    "similarity": "0.8984190225601196, similar to corpus_set Papers"
  }
}
```
##### Possible optimization / future work
The whole snowballing process is right now really slow, this is mainly caused by the slow extraction of references and abstracts via the
different APIs. Here another approach for retrieving these would be nice. 

### Paper Selection
This module contains four functions which can be used to select papers on the
basis of the similarity between the query and the papers you are interested in, and it can show the result in a plot. 
#### paper_importance
```python 
paper_importance(text=[], keywords=[])
```
This function makes it possible to compare Keywords or a research topic with one or more texts. Therefore, it uses the
keywords and the text and calculates the cosines similarity of those. As result, you get a value for of each keyword 
relating to all the papers you hand over the function.

<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*text*: The parameter takes a list of texts (strings). So it is possible to calculate the similarity between more than just 
one text. -> much more efficient. You can use a whole text, phrases or just the abstract. Feel free to try!

*keywords*: Also the attribute "keywords" is a list of strings. Those can represent a list of single keywords, phrases or sentences.
Which get compared with the list of texts you hand over.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The function returns a dataframe from pandas. In this you have in  one axis the texts and on the other the several keywords.
It is a matrix where you can find the evaluation of all the papers and keywords.
#### plot_paper_selection
```
plot_paper_selection(df=pd.DataFrame())
```
This function makes it possible to plot the results from the function "paper_importance". This function creates an 
interactive plot, where in the x-axe are shown the several keywords and on the y-axe the score regarding the paper.
The different papers are shown in single traces on this plot. Since it is an interactive plot, it is possible to
inactivate or activate the single traces. 

<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*df*: The input is a dataframe, which contains the results of the "paper_importance". 
Just hand over the return of this function. 

<ins><ins>**<span style="font-size:13px;">Output:</span>**</ins></ins>  
The function returns the object file of the plot. So it is possible to handle this or to save it afterwards. 

#### snowballing_paper_importance
```python 
snowballing_paper_importance(snowballing_result_path, keywords=[]):
```
Calculates the paper importance like in [PaperSelection.paper_importance](#paper_importance)
but for the snowballing results and adds the similarity with the keywords to the snowballing_result json.

<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*snowballing_result_path*: json file resulting from [PaperSearch.snowballing()](#Automatic-Snowballing)

<ins><ins>**<span style="font-size:13px;">Output:</span>**</ins></ins>  
Returns json file with keyword similarity of each paper in the file added.

#### plot_snowballing_importance
```python 
plot_snowballing_importance(snowballing_result_path)
```
Plots the result of the [PaperSelection.snowballing_paper_importance](#snowballing_paper_importance), by transforming the json to a pandas data frame and passing it to the PaperSelecton.plot_paper_selection function

<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*snowballing_result_path*: json file resulting from [PaperSelection.snowballing_paper_importance](#snowballing_paper_importance)

<ins><ins>**<span style="font-size:13px;">Output:</span>**</ins></ins>  
The function returns the object file of the plot. So it is possible to handle this or to save it afterwards. 

plot
##### Possible optimization / future work
1. Probably it would be nice to implement a plot methode to all other functions, so it would be easy to evaluate 
them and have a good overview. 
2. Right now we calculate the importance under the assumption that it doesn´t matter if we use keywords or a whole sentence to compare it with the text. 
It might be good the implement several functions. One for words ->Bert and the other for sentence -> SBert

   
### Keyword/Keyphrase Extractor
This file contains two methods, the "yake_extraction" and the "rake_phrase_extraction" both can be used to extract 
keyphrases but for single keyword extraction you can only use the "yake_extraction".


#### yake_extraction
The yake extraction provides more than on possibility to extract keywords from the text. The function has a lot of input 
parameter. With them, it is possible to define a lot of properties. 
```python 
yake_extraction(text, number_of_keyphrases=10, language='en', words_in_keyphrase=10, deduplication_threshold=0.5)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
*text*:This Parameter is the String where you want to extract the keywords/phrases.
*number_of_keyphrases*: With that integer you can define how many keywords/phrases you want to extract.  
*language*: This string defines the language of the text, where you want to extract the data.  
*words_in_keyphrase*: This Parameter is an integer which defines the number of words in a keyphrase. If you actually want 
to extract single keywords you might use the value "1" otherwise you get longer phrases.  
deduplication_threshold: With that threshold it is possible to finetune the extraction. So that the several Keyphrases 
consists out of duplication.  
E.g.1 threshold -> low [Keyword, Keyword Extraction, Keywords out of text]  
E.g.2 threshold -> high [Keyword, Extraction, Words out of text]

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
As output this function returns a dictionary of all the phrases which you defined with "number_of_keyphrases" and the 
score of it. 
#### rake_phrase_extraction
This function is a simple implementation to extract keyphrases out of a text. There are no more variables to define. 
```python 
rake_phrase_extraction(text, number_of_keywords=10)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>    
The input of this function is first the text(string) where you want to extract the keyphrases from. The other input 
"number_of_keywords" is the number how many phrases you want to return.  

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
As output this function returns a list of all the phrases which you defined with "number_of_keywords" and the 
score of it. 

##### Possible optimization / future work
1. One important task might be to evaluate the functionality of the extractors. 
2. Also it would be great to find out, which form of text works best. -> Just the abstract, the whole text and so on. 

### Summarization
The summarization function is implemented with the function from
https://gist.github.com/edubey/cc41dbdec508a051675daf8e8bba62c5 it creates a summarization out of a text. Therefor it 
builds up a similarity matrix between all sentences and the text and takes the most valued sentences as sentences for
the summarization. This file contains four functions for that: read_article, sentence_similarity, build_similarity_matrix
and generate_summary.

#### read_article
This function reads the text and parse it into the single sentences, and also it removes special characters out of the 
string.
```python 
read_article(text)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
The input of this function is a text(string) that you want to summarize.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  >
As an output it returns a list of all sentences without the special symbols in it.

#### sentence_similarity
This function compares two sentences with each other and returns a value of the similarity of those both. Also, it removes 
stopwords out of the sentences. This function is used to build up the similarity matrix. 
```python 
sentence_similarity(sent1, sent2, stopwords=None)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*sent1*: Is a string of sentence one.  
*sent2*: Is a string of sentence two.  
*stopwords*: This parameter can be a list where you can hand over the stopwords you want to remove.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The return of this function is a value, which represent the similarity of the two sentences above.

#### build_similarity_matrix
The function gets the list of all sentences and calculates for all of them the similarity to build the matrix.
```python 
build_similarity_matrix(sentences, stop_words)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*sentences*: This is a List of all sentences and should be the return of the function "read_article"  
*stopwords*: Here you can hand over a list of stopwords which get removed before calculating the similarity.
If the value is "none" no stopwords got removed.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The function returns a matrix in the size of (len(sentences) x len(sentences)) 

#### generate_summary
This function concatenates all the other functions above. So you just need to call a single function to create a summary. 
```python 
generate_summary(file_name, top_n=5)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
file_name: This is the input to give the function the Text you want to summarize  
top_n: This parameter defines how long your summarize going to be. E.g. top_n = 5, creates a summary out of the 5 highest
valued. 

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The function returns the summary as a string.


### Text Preprocessing
This file is a implementation of some nltk functions to preprocess the text which you want to work with. This is not
always necessary, because some of those steps are already implemented in the other functions. 
Preprocessing steps: tokenize, remove_stopwords, lemmatizing, port_stemmer and position_tag. 

### tokenize
This function tokenize the text from the input.
```python 
tokenize(text)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
text: String of the text which should be tokenized.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns a list with all tokens.
### remove_stopwords
```python 
remove_stopwords(text=str(""), stops=[])
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
text: This input parameter is a string from where the stopwords going to be removed.  
stops: Is a list with all the words you want to remove.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  

### lemmatizing
This function creates lemmas out of single words. 
```python 
lemmatizing(text=str(''))
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*text*: This parameter is a string, which is going to be split up by the tokenize function

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
The output is a text with lemmas, no words.

### port_stemmer 
This function stems all words out of an text.
```python 
port_stemmer(text=str(''))
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
text: String that contains the text where the words are going to be stemmed. 

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
This function returns a text with stemmed words. 

### position_tag
This methode tags all the words in a text. E.g. Verb, adjective ...
```python 
position_tag(text)
```
<ins>**<span style="font-size:13px;">Input:</span>**</ins>   
*text*: String that contains the text where the words are going to be tagged.

<ins>**<span style="font-size:13px;">Output:</span>**</ins>  
Returns a text with all words and the relating tags. 

### Command line interface (cli)
Instead of using the above described modules and their function in code or as a library you can simply use most of these function with simple cli commands which will be explainend in the following section.
All cli commands need to be called from the path NLP4/src/modules.

For a detailed description about parameters and functionality of each cli command call the respective command with "--help" flag.

##### Explanation of all function
```cli
pipenv run cli.py --help
```
##### Summarization
Uses [Summarization.generate_summary()](#generate_summary) to summarize given text
```cli
pipenv run cli.py summarization --text"your text"
```
##### paper_selection
Calls [PaperSelection.paper_importance](#paper_importance) and PaperSelection.plot_paper_selection with the passed arguments
```cli
pipenv run cli.py paper_selection  --text="["text1", "text2"]" --keywords="["kw1", "kw2"]"
```
##### snowballing
Runs the [automated snowballing](#snowballing) with the papers with the passed_seed set. If none is passed, default path NLP4/src/seed_set will be used.
```cli
pipenv run cli.py snowballing --seed_set_path"path to seed_set" --iterations=1  --min_similarity=0.85
```

##### snowballing_paper_selection
Calls [PaperSelection.snowballing_paper_importance](#snowballing_paper_importance ) with the given snowballing_result_file and the specified key_words
```cli snowballing_paper_selection
pipenv run cli.py snowballing_paper_selection --snowballing_result_path="path to snowballing result" --keywords="["test","test2"]"
```
##### pdf_similarity
Compares the similarity of two passed pdf with [Similarities.pdf_similarity](#pdf_similarity) with the specified files.
```cli 
pipenv run cli.py pdf_similarity --paper1="Path To paper" --paper2="Path To paper" --only_abstract=False
```

##### extract_keywords_pdf
Extracts key_phrases of given PDF with [KeywordKeyphraseExtractor.yake_extraction](#yake_extraction).
```cli 
pipenv run cli.py extract_keywords_pdf --pdf="path to pdf"

```

##### extract_keyphrases_pdf
Extracts key_phrases of given PDF with [KeywordKeyphraseExtractor.rake_phrase_extraction](#rake_phrase_extraction).
```cli 
pipenv run cli.py extract_keyphrases_pdf --pdf="path to pdf" 
```


## Getting started
To set up a development environment and to use the CLI, simply run the following commands:

```console
# Clone the project
git clone https://github.com/fwUniGit/NLP4.git
cd {project_directory}
# Install pipenv and dependencies
pip install pipenv
pipenv install 
```
The project is now setup you can now either use and extend the code(e.g. as library) or use the CLI commands like shown:
```console
cd src/modules #Navigate to the modules task
pipenv run cli.py --help #Run CLI help to get an overview over all function 
```
For example try to run a snowballing by placing a few papers inside: /src/seed_set 
and then simply run: 
```cli
pipenv run cli.py snowballing --iterations=1  --min_similarity=0.85
```


## API reference
#### Scholarcy Reference Extraction API
The [Scholarcy Reference Extraction API](https://ref.scholarcy.com/api/) is an open REST API for extracting, parsing 
and resolving bibliographic references from PDF, Word (.docx), and text (.txt) documents.
You can either make a GET request with the link to a file of ap paper or an POST request with the file of the paper appended. 
The API will then extract the references from paper and return the in a json string in the response. 
The JSON string contains all references in textual description
as well as different links to the references. These links can be of 3 different types:
* crossref => Is a https://dx.doi.org/ link with the respective doi.
* scholar_url => Is a link leading to the Google Scholar result of the specific paper
* oa_query => Leads either directly to a PDF version of the reference or to the paper page of the publishing journal

* Not for all references all 3 of the types are available.

##### Example Response:
```json
{
  "filename": "15.pdf",
  "metadata": {
    "arxiv": null,
    "doi": "10.1371/journal.pone.0098679",
    "isbn": null,
    "date": 2014
  },
  "references": [
    "1. Bastian M, Heymann S, Jacomy M (2009) Gephi: an open source software for exploring and manipulating networks. In: International AAAI Conference on Weblogs and Social Media. Association for the Advancement of Artificial Intelligence.",
    "2. Diminescu D (2008) The connected migrant: an epistemological manifesto. Social Science Information 47: 565–579."
  ],
  "bibtex": "@incollection{bastian2009a,\n  author = {Bastian, M. and Heymann, S. and Jacomy, M.},\n  date = {2009},\n  title = {Gephi: an open source software for exploring and manipulating networks},\n  booktitle = {International AAAI Conference on Weblogs and Social Media. Association for the Advancement of Artificial Intelligence},\n  language = {}\n}\n@article{diminescu2008a,\n  author = {Diminescu, D.},\n  date = {2008},\n  title = {The connected migrant: an epistemological manifesto},\n  journal = {Social Science Information},\n  volume = {47},\n  pages = {565–579},\n  language = {}\n}",
  "reference_links": [
    {
      "id": "1",
      "entry": "1. Bastian M, Heymann S, Jacomy M (2009) Gephi: an open source software for exploring and manipulating networks. In: International AAAI Conference on Weblogs and Social Media. Association for the Advancement of Artificial Intelligence.",
      "scholar_url": "https://scholar.google.co.uk/scholar?q=Bastian%2C%20M.%20Heymann%2C%20S.%20Jacomy%2C%20M.%20Gephi%3A%20an%20open%20source%20software%20for%20exploring%20and%20manipulating%20networks%202009",
      "oa_query": "https://ref.scholarcy.com/oa_version?query=Bastian%2C%20M.%20Heymann%2C%20S.%20Jacomy%2C%20M.%20Gephi%3A%20an%20open%20source%20software%20for%20exploring%20and%20manipulating%20networks%202009"
    },
    {
      "id": "2",
      "entry": "2. Diminescu D (2008) The connected migrant: an epistemological manifesto. Social Science Information 47: 565–579.",
      "scholar_url": "https://scholar.google.co.uk/scholar?q=Diminescu%2C%20D.%20The%20connected%20migrant%3A%20an%20epistemological%20manifesto%202008",
      "oa_query": "https://ref.scholarcy.com/oa_version?query=Diminescu%2C%20D.%20The%20connected%20migrant%3A%20an%20epistemological%20manifesto%202008"
    }
  ]
}
```
#### Crossref REST API
The [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/) is an API which gives the user access to all kind of meta data of many papers
by making a request with the doi of the paper. 
We mainly use the metadata "reference" containing the references of the paper and "abstract", containing the abstract of the paper.
For more information about the crossref API we recommend taking a look at it's documentation: [https://www.crossref.org/documentation/retrieve-metadata/rest-api/](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)


#### ArXiv API
The [arXiv API](https://arxiv.org/help/api/) allows access to all the arXiv data. This contains data like tiles, abstracts, authors and links to pdf files.
Unfortunately the arxiv API enables no access to references. To use the arxiv api we use this python wrapper: [https://pypi.org/project/arxiv/]("https://pypi.org/project/arxiv/")

## Tests
We implemented unit test with a code coverage of 97%. We couldn't cover 99% because some functions
like the reference_extraction have some very rare exceptions when for example the scholarcy request
responses with an 503 error. For these cases we couldn't find test examples.

## Project structure 
The Python Project structure and the github workflows including the typing, linting and testing are generated from
[https://github.com/ag-gipp/PythonProjectTemplate](https://github.com/ag-gipp/PythonProjectTemplate)

## License
This project is licensed under the terms of MIT license. Please see the LICENSE file for details.
