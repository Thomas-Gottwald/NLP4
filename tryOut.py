import src.modules.PDFMiner as pdfM
import src.modules.ReferenceExtraction as RE
import src.modules.AbstractExtraction as AE
import src.modules.Similarities as Sim


# PDF Extraction
# text = pdfM.get_pdf_text("./tests/test_paper/rsos.201199.pdf")
# print(text)


# Reference Extraction
# references = RE.get_referenced_papers("./tests/test_paper/rsos.201199.pdf")
# print(references)

# refeAbst = RE.get_reference_abstracts("./tests/test_paper/rsos.201199.pdf")
# print(refeAbst)


# Abstract Extraction # TODO vervollständigen
# abst = AE.get_abstract_from_doi()

# abst = AE.get_abstract_from_arxiv_id()

# abst = AE.get_abstract_by_pdf()

# Similarities
# similarity = Sim.pdf_similarity("./tests/test_paper/rsos.201199.pdf", "./tests/test_paper/15.pdf")
# print(similarity)

# similarity = Sim.pdf_similarity(
#     "./tests/test_paper/rsos.201199.pdf",
#     "./src/modules/snowballing_seed_set/2111.10594v1.Misrepresenting_Scientific_Consensus_on_COVID_19_The_Amplification_of_Dissenting_Scientists_on_Twitter.pdf",
# )
# print(similarity)
