import re
import pdfplumber
import sys


def addPageNo(pdfsource, txtdes):
    open(txtdes, 'w').close()
    with pdfplumber.open(pdfsource) as pdf:
        txtdesObj = open(txtdes, 'a', encoding='utf-8')
        # Page-by-page search for text that matches heading formatting
        for p in range(0, len(pdf.pages)):  
            text = pdf.pages[p].extract_text()
            pattern = re.compile('((?:["第"][\s][1-9][\s]["章"][\s]+(?:[\u4e00-\u9fa5a-zA-Z0-9-_——]+[\s])+)'
                                 '|(?:(?:[1-9][.])+[1-9][\s]+(?:[\u4e00-\u9fa5a-zA-Z0-9-_——]+[\s])+))')
            matchtitle = pattern.findall(text)
            if matchtitle:
                for title in matchtitle:
                    result = title + ';' + str(pdf.pages[p].page_number)
                    print(result)
                    # Hierarchical relationship between print titles
                    for tab in range(0, result.count(".", 0, 8)):  
                        txtdesObj.write('\t')
                    txtdesObj.write(result)
                    txtdesObj.write('\n')
        txtdesObj.flush()
        txtdesObj.close()


if __name__ == '__main__':
    sourcepdf = sys.argv[1]
    # despdf = sys.argv[2]
    addPageNo(sourcepdf, 'bookMark'+sourcepdf[0:-4]+'.txt')
