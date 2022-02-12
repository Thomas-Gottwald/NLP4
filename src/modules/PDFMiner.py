from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def getPDFText(pdfFilenamePath,throwError:bool=True):
    output_string = StringIO()
    with open(pdfFilenamePath,'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    print(output_string.getvalue())

    retstr = StringIO()
    parser = PDFParser(open(pdfFilenamePath,'rb'))
    try:
        document = PDFDocument(parser)
    except Exception as e:
        errMsg=f"error {pdfFilenamePath}:{str(e)}"
        print(errMsg)
        if throwError:
            raise e
        return ''
    if document.is_extractable:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr,retstr,  laparams = LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.create_pages(document)
        for pageNumber, page in enumerate(pages):
            if pageNumber != 0:
                interpreter.process_page(page)

        return retstr.getvalue()
    else:
        print(pdfFilenamePath,"Warning: could not extract text from pdf file.")
        return ''

