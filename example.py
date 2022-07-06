import tocExtractor


extractor = tocExtractor.tocExtractor()
fdir = "/home/jiwooshim/PycharmProjects/tocExtractor/sample.pdf"
mda_keyword = "Management Discussion and Analysis"
toc_keyword_1 = "Table of Contents"
toc_keyword_2 = "Contents"

doc_outline = extractor.find_toc(fdir, mda_keyword, toc_keyword_1, toc_keyword_2)
print(doc_outline)