import os.path
import pandas as pd
import PyPDF2
from bs4 import BeautifulSoup
import re
import os
import fitz
from pathlib import Path
from thefuzz import fuzz, process
import argparse
import sys


class tocExtractor():
    def find_toc(self, fdir, common_keyword, toc_keyword_1, toc_keyword_2):
        doc = fitz.open(fdir)
        for pageNum in range(doc.pageCount):
            if pageNum > 10:
                break
            page = doc.loadPage(pageNum)
            pageText = page.getText('text')
            pageHTML = page.getText('html')
            if len(pageText) < 15:
                continue
            text = pageText.strip()
            if fuzz.partial_ratio(common_keyword.lower(), text.lower()) > 90 and \
                    (fuzz.partial_ratio(toc_keyword_1.lower(), text.lower()) > 90 or
                     fuzz.partial_ratio(toc_keyword_2.lower(), text.lower()) > 90):
                soup = BeautifulSoup(pageHTML, 'html.parser')
                return self.extract_toc(soup)
        return None

    def extract_toc(self, soup):
        findAllP = soup.findAll('p')
        textAndStyle = [p['style'].split(';') + [f"text:{p.find('span').text}"] for p in findAllP]
        textAndStyleDict = [{element.split(':')[0]: element.split(':')[1] for element in elementList} for elementList in
                            textAndStyle]
        df_textAndStyle = pd.DataFrame(textAndStyleDict)
        df_textAndStyle.sort_values('top', inplace=True)

        df_groupby_textAndStyle = df_textAndStyle.groupby('top')
        outlines_list = []
        prev_left_positions = []
        for idx, df in enumerate(df_groupby_textAndStyle):
            if len(df[1]) == 1:
                continue
            ## Group the page title and page numbers on the same position from the top.
            outlinePageGroup = [row[1]['text'] for row in df[1].iterrows()]
            if idx+1 == len(df_groupby_textAndStyle) and not all(df[1]['left'].isin(prev_left_positions)):
                break
            outlines_list.append(outlinePageGroup)
            prev_left_positions = list(df[1]['left'].values)
        return self.process_outline(outlines_list)

    def process_outline(self, raw_outline_list):
        new_outline_list = []
        for outline in raw_outline_list:
            title = None
            pageNum = self.find_integer(outline)
            englishText = self.find_eng(outline)
            chineseText = self.find_chi(outline)
            if pageNum is None:
                continue
            elif englishText is None:
                if chineseText:
                    title = chineseText
                else:
                    continue
            elif chineseText is None:
                title = englishText
            new_outline_list.append([title, pageNum + 1])
        return new_outline_list

    def find_integer(self, input_list):
        for element in input_list:
            try:
                pageNum = element.strip()
                return int(pageNum)
            except:
                continue

        for element in input_list:
            ## pattern: 4-8
            if re.search(r'[0-9]{1,5}[\s]*-[\s]*[0-9\s]{1,5}', element):
                pageNum = re.findall(r'[0-9]{1,5}[\s]*-[\s]*[0-9\s]{1,5}', element)[0].split("-")[0].strip()
                return int(pageNum)

            ## pattern: 4 to 8
            if re.search(r'[0-9]{1,5}[\s]*to[\s]*[0-9\s]{1,5}', element):
                pageNum = re.findall(r'[0-9]{1,5}[\s]*to[\s]*[0-9\s]{1,5}', element)[0].split("to")[0].strip()
                return int(pageNum)
        return None

    def find_eng(self, input_list):
        for element in input_list:
            if re.search(r'[a-zA-Z\s]+', element):
                return "".join(re.findall(r'[a-zA-Z\s]+', element)).strip()


    def find_chi(self, input_list):
        for element in input_list:
            if re.search(r'[\u4e00-\u9fff]+', element):
                return "".join(re.findall(r'[\u4e00-\u9fff]+', element)).strip()

    def pdf_extract_page(self, pdfPath, pageNum, tocPath):
        if not os.path.exists(tocPath):
            os.mkdir(tocPath)
        with open(pdfPath, 'rb') as read_stream:
            pdf_reader = PyPDF2.PdfFileReader(read_stream)
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(pageNum))
            ouput = os.path.join(tocPath, f'{Path(pdfPath).stem}_page_{pageNum}')
            with open(ouput, 'wb') as out:
                pdf_writer.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script extracts Table of Contents from PDF files using keywords."
                                                 " Tested on Hong Kong Stock Exchange (HKEX) reports.")
    parser.add_argument("--fileDir", "-f", required=True, help='Full file location')
    parser.add_argument("--common_keyword", "-c", required=True, help='Common keyword found in the ToC section of '
                                                                      'reports. Example: "Management Discussion and Analysis"')
    parser.add_argument("--toc_keyword_1", "-k1", required=True, help='Keyword of the ToC title. Example: "Table of '
                                                                      'Contents" or "Contents"')
    parser.add_argument("--toc_keyword_2", "-k2", required=True, help='Keyword of the ToC title different to -k1. '
                                                                      'Example: "Table of Contents" or "Contents"')
    args = parser.parse_args(sys.argv[1:])

    extractor = tocExtractor()
    extractor.find_toc(args.fileDir, args.common_keyword, args.toc_keyword_1, args.toc_keyword_2)
