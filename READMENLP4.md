
---
## NLP To the Rescue! (NLP4)
A short description of the project’s purpose and main functionality. **What** does the project do?
This project is an attempt to create a system which uses NLP techniques to aid authors in performing systematic literature 
reviews (SLR). This system offers some implementations of NLP techniques like text similarity and key word extraction.
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
*What makes your project stand out? Include screenshots, code snippets, logos, etc.*
As already mentioned the current state of the proposed system focuses on aiding the author in the search of relevant studies and the
section of relevant studies. 
Therefore we implement the following features:
* Feature list
    * PDF Extraction
    * Keyword Extractor
    * Keyphrase Extractor
    * Reference Extraction
    * Summarization
    * Similarity
    * Preprocessing
    * Automatic Snowballing
    * Paper selection
    * Plot Results
Most of these features are build upon diverse open source projects.
In the following section we will describe the features and their basis in detail and propose optimazition possbillities
for future work.

*All features can be used via the CLI without programming as well as in code by using the respective functions* 
All CLI commands expect the user to be called from the project root path "NLP4/"

### PDF extraction
The PDF extraction is implemented with the PDFMiner from:
https://stackoverflow.com/questions/5725278/how-do-i-use-pdfminer-as-a-library/26351413#26351413

https://github.com/pdfminer/pdfminer.six.

It enables the user to extract all text of a PDF in python. An outstanding feature of the PDFMiner is that it recognizes
the layout of the given PDF file and therefore is able to extract text from diverse PDFs. This is especially relevant
because many scientific papers have a two column layout which other PDF extraction frameworks we tried failed on.

#####Usage:

######In code:
```python
PDFminer.getPDFtext(pdfFilenamePath="", ignore_references = "True")
```
###### Via CLI
Via CLI the user is able to extract the text from the given PDF file to a given .txt file

```sh
pipenv run python main.py functions extractPdfToText <pdfPath> <txtPath>
```

##### Possible optimization / future work
One problem that occurs with the PDF extraction is that disadvantageous parts of the PDF, which contain no usable information
for our usecase, are also extracted. This means for example the title page with the paper contibutors etc. or food- / head- notes.
It would be beneficial to analyze ways to remove these parts from the extracted text or recognize them before extracting the text.
This would boost the performance of the NLP techniques like the similarity or keyword extraction when they are used in combination
with the pdf extraction.

### Abstract Extraction
The Abstract Extraction Module implements the following 3 functions to extract abstracts from difrent sources.
```python
get_abstract_from_doi(doi)
```
Returns the abstract of a paper by its given DOI by querrying the crossref API for the doi.
The crossref API offers abstracts of many free available papers. Nevertheless it is not possible to
retrieve abstracst of all papers by this api.


```python
get_abstract_from_arxiv_id(arxiv_id)
```
Returns the abstract of any paper hosted by arXiv.org given by the respective arxiv_id.
To retrieve the abstract the arxiv api is used.


```python
get_abstract_by_pdf(pdf)
```
This method trys to get the abstracts of a given pdf. Here The pdf parameter can eiter be the path to
a local pdf file or an online link like (https://arxiv.org/pdf/xxxxxx.pdf).
The function makes a request to the scolarcy api, which then returns either the doi or the arxiv id, whichever is
available. And the uses the respective get_abstract function specified above to return the abstract of the given pdf.
### Reference Extraction
The Reference Extraction uses an the scholarcy REST API which extracts all references from an uploaded PDF.
The scholarcy reference extraction API returns a JSON string with all references in textual description
as well as different links to the references. These links can be of 3 diffrent types:
* crossref => Is a https://dx.doi.org/ link with the respective doi.
* scholar_url => Is a link leading to the google scholar result of the specific paper
* oa_querry => Leads either directly to a PDF version of the reference or to the paper page of the publishing journal

Not for all references all 3 of the types are available.


### Automatic Snowballing
The automatic snowballing feature performs a full automized forward snowballing, by extracting all references
of all PDFs inside a specified folder. The folder defines the seed set for the snowballing. The default path for
the seed set is NLP/seed_set. With the ReferenceExtraction feature the abstracts of the 

### Paper Selection

### Keyword Extractor

### Keyphrase Extractor


## Installation
Provide step-by-step examples and descriptions of how to set up a development environment.

## API reference
For small projects with a simple enough API, include the reference docs in this README. For medium-sized and larger projects, provide a link to the API reference docs.

## Tests (optional: only if you have tests)
Describe and show how to run the tests with code examples.

## How to use and extend the project? (maybe)
Include a step-by-step guide that enables others to use and extend your code for their projects. Whether this section is required and whether it should be part of the `README.md` or a separate file depends on your project. If the **very short** `Code Examples` from above comprehensively cover (despite being concise!) all the major functionality of your project already, this section can be omitted. **If you think that users/developers will need more information than the brief code examples above to fully understand your code, this section is mandatory.** If your project requires significant information on code reuse, place the information into a new `.md` file.

## Results
If you performed evaluations as part of your project, include your preliminary results that you also show in your final project presentation, e.g., precision, recall, F1 measure and/or figures highlighting what your project does. If applicable, briefly describe the dataset your created or used first before presenting the evaluated use cases and the results.

If you are about to complete your thesis, include the most important findings (precision/recall/F1 measure) and refer to the corresponding pages in your thesis document.

## License
Include the project's license. Usually, we suggest MIT or Apache. Ask your supervisor. For example:

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License

## License of this readme-template (remove this once you replaced this readme-template with your own content)
This file itself is partially based on [this file](https://gist.github.com/sujinleeme/ec1f50bb0b6081a0adcf9dd84f4e6271). 
