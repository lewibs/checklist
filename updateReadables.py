import os
# https://pyfpdf.readthedocs.io/en/latest/ReferenceManual/index.html
from fpdf import FPDF

cwd = os.getcwd()

pdf = FPDF()
pdf.set_font("Arial", size = 12)
pdfPages = [] #added backwards
pdf_path = os.path.join(cwd, "checklist.pdf")
pdf_width = 200
pdf_height = 10
pdf_ln = True
pdf_align = "L"

directory = os.path.join(cwd, "checklists")
readme_path = os.path.join(cwd, "README.md")
readme_content = '''
# Intro
The use of this is to help software developers write better software and have better habits when working

This was inspired by <a href="https://a.co/d/9DpHQHJ">The Checklist Manifesto</a>, which is a book by Atul 
Gawande that highlights the power of checklists in improving performance and reducing errors. Gawande argues 
that even experts can benefit from using checklists to ensure consistency and enhance teamwork. He provides 
examples from various industries, such as medicine and aviation, to demonstrate how checklists can save lives 
and improve outcomes. The book emphasizes the importance of simplicity, standardization, and communication in 
checklist design and implementation. Overall, it advocates for the systematic use of checklists to enhance 
productivity and safety in complex tasks.

However, you as the developer are responsible for knowing when its time to creativly ignore the checklist and 
do things differently.

# Checklists
'''

def checkCwd():
    global cwd
    name = os.path.basename(__file__)
    path = os.path.join(cwd, name)
    if not os.path.exists(path):
        raise Exception("must run script from its own location")

def appendContent(new_content):
    global readme_content
    readme_content = readme_content + new_content

def appendChecklist(path):
    with open(path, "r") as file:
        title = file.readline().split(":")[1].strip()
        use = file.readline().split(":")[1].strip()

    path = path.replace(cwd, ".")

    appendContent(f"<a href='{path}'>{title}</a> - {use}<br>\n")
    
def makeReadme(dirpath, depth=0):
    items = os.listdir(dirpath)
    items = sorted(items, key=lambda x: os.path.isdir(os.path.join(dirpath, x)))

    for item in items:
        for i in range(0, depth):
            appendContent("  ") 
        appendContent("* ")

        item_path = os.path.join(dirpath, item)
        
        if os.path.isdir(item_path):
            appendContent(f"<a href='{item_path.replace(cwd, '.')}'>{item}</a>" + "<br>\n")
            addDirToPdf(item_path, item)         
            makeReadme(item_path, depth + 1)
        else:
            addChecklistToPdf(item_path)
            appendChecklist(item_path)

def writeReadme():
    global readme_path
    global readme_content
    with open(readme_path, "w") as file:
        file.write(readme_content)

def writeTextToPdf(text, addPage=True):
    global pdf

    if addPage:
        pdf.add_page()

    #check if its already been split
    if isinstance(text, list):
        text = text.splitlines()

        for line in text:
            writeTextToPdf(line, False)
    else:
        chunk_size = int(pdf_width / 2)

        start = 0
        end = chunk_size

        while start < len(text):
            # Check if the chunk ends in the middle of a word
            if end < len(text) and not text[end].isspace() and not text[end-1].isspace():
                # Find the last space character before the end position
                while end > start and not text[end-1].isspace():
                    end -= 1

            chunk = text[start:end]
            pdf.cell(pdf_width, pdf_height, txt = chunk, ln = pdf_ln, align = pdf_align)

            start = end
            end = min(start + chunk_size, len(text))  # Update the end position

            if start == end:
                break

def addDirToPdf(path, dirName):
    global pdf
    pdf.add_page()
    pdf.cell(pdf_width, pdf_height, txt = dirName, ln = pdf_ln, align = "C")

def addChecklistToPdf(path):
    global pdf
    pdf.add_page()
    
    # open the text file in read mode
    f = open(path, "r")
    
    for x in f:
        pdf.cell(pdf_width, pdf_height, txt = x, ln = pdf_ln, align = pdf_align)


def writePdf():
    global pdf
    pdf.output(pdf_path) 


writeTextToPdf(readme_content)
checkCwd()
makeReadme(directory)
writeReadme()
writePdf()
##printReadme()
