# ToC Extractor
This script extracts "Table of Contents" from PDF files using keywords. This is particularly useful for PDFs without a pre-defined outline, as this module will go through the pages to find the ToC page and extract the outline titles as well as their respective page numbers. Tested on Hong Kong Stock Exchange (HKEX) reports.


## Installation 
Clone this repository and install requirements.
```
git clone git@github.com:jiwooshim/tocExtractor.git
pip install -r requirements.txt
```

## Usage
### Input arguments
| Parameter | Required | Description |
| -- | -- | -- |
| -f --fireDir | True | Full file location |
| -c --common_keyword | True | Common keyword found in the ToC section of all reports. This is used to help identify the ToC better.  Example: "Management Discussion and Analysis" |
| -k1 --toc_keyword_1 | True | Keyword of the ToC title. Example: "Table of Contents" |
| -k2 --toc_keyword_2 | True | Keyword of the Toc title different to -k1. Example: "Contents" |


### Example
#### tocExtractor in a script
Check [example.py](https://github.com/jiwooshim/tocExtractor/blob/main/example.py).
#### tocExtractor in terminal
```
python3 tocExtractor -f /home/jiwooshim/tocExtractor/sample.pdf -c "Management Discussion and Analysis" -k1 "Table of Contents" -k2 "Contents"
```

## Output
This module simply outputs the PDF outline. If imported and used in a script, the variable can be saved as a list.
#### Output example for sample.pdf
```
[['Corporate Information', 3], ['Financial Highlights', 4], ['Chairmans Statement', 5], ['Management Discussion and Analysis', 6], ['Profiles of Directors and Senior Management', 11], ['Corporate Governance Report', 15], ['Report of the Directors', 24], ['Independent Auditors Report', 32], ['Consolidated Income Statement', 33], ['Consolidated Balance Sheet', 34], ['Consolidated Statement of Changes in Equity', 35], ['Consolidated Cash Flow Statement', 36], ['Balance Sheet', 37], ['Notes to Financial Statements', 38], ['Five Year Financial Summary', 79], ['Notice of Annual General Meeting', 80], ['Glossary of Terms', 84]]
```