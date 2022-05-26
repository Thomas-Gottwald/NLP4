import src.modules.PDFMiner as pdfM
from tqdm import tqdm
import os
import platform


def get_local_path():
    cwd = os.getcwd()
    if platform.system() == "Windows":
        cwd = cwd[0].lower() + cwd[1:]

    file_name = "checkout.py"
    path = os.path.realpath(__file__)

    path = path.replace(cwd, ".", 1)
    path = path.replace(file_name, "")

    return path


path = get_local_path()
# text = pdfM.get_pdf_text("./tests/test_paper/rsos.201199.pdf")
text = pdfM.get_pdf_text(os.path.join(path, "./../Literature/s13643-019-1074-9.pdf"))


lines = text.splitlines(keepends=True)

abstract = ""
for l in lines:

    if len(l) > 1:
        abstract += l
    else:
        if len(abstract) > 500:
            break
        else:
            abstract = ""

print(len(abstract))
print(abstract)


file = open(os.path.join(path, "pdf_text.txt"), "w", encoding="utf-8", newline="\n")

file.write(text)

file.close()
