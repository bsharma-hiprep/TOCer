"""
works up to contents_text extraction part. 
for patterns to work reliably, need to preprocess the ocr text, i.e. full_text to match a general structure of the TOC. 
Need to think about how to generalize the TOC structure matching well. 
Verdict: not useful for now. dont use.
"""
import re

def parse_contents_page_generalized(text):
    contents_start = text.find("Contents")
    if contents_start == -1:
        contents_start = text.find("Table of Contents")
    if contents_start == -1:
        print("Contents page not found")
        return []

    # Capture the entire contents section
    contents_end = text.find("Index")
    if contents_end == -1:
        contents_end = text.find("Bibliography")
    if contents_end == -1:
        contents_end = len(text)

    contents_end = text.find("__page", contents_end)
    if contents_end == -1:
        contents_end = len(text)

    contents_text = text[contents_start:contents_end]

    # Regular expressions for different hierarchical levels
    patterns = {
        "intro": re.compile(r'(Foreword|Preface)', re.IGNORECASE),
        "part": re.compile(r'^(Part\s*\d*|^\d+)\s+[A-Z]', re.IGNORECASE),
        "chapter": re.compile(r'^\d+\.\s*[A-Za-z]', re.IGNORECASE),
        "subsection": re.compile(r'^\d+\.\d+\s*[A-Za-z]', re.IGNORECASE),
        "conclusion": re.compile(r'(Appendix|Notes|Bibliography|Index)', re.IGNORECASE)
    }

    # Process the contents text line by line
    structure = []
    lines = contents_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for level, pattern in patterns.items():
            match = pattern.search(line)
            if match:
                page_number = re.findall(r'\d+', line)
                if page_number:
                    page_number = int(page_number[-1])  # Take the last number found as page number
                    structure.append((match.group(), page_number, level))
                break

    return structure


structure = parse_contents_page_generalized(full_text)
structure
