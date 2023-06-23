import os
# https://pyfpdf.readthedocs.io/en/latest/ReferenceManual/index.html
from fpdf import FPDF
from PyPDF2 import PdfMerger

cwd = os.getcwd()

def initPDF():   
    pdf = FPDF()
    pdf.set_font("Arial", size = 12)
    return pdf

pdf = initPDF()
pdfPages = [] #added backwards
pdf_path = os.path.join(cwd, "checklist.pdf")
temp_pdf_path = os.path.join(cwd, "temp.pdf")
pdf_width = 200
pdf_height = 10
pdf_ln = True
pdf_align = "L"

directory = os.path.join(cwd, "checklists")
readme_path = os.path.join(cwd, "README.md")

readme_content = {
    "why": "The use of this is to help software developers write better software and have better habits when working.",
    "book": '''This was inspired by {}, which is a book by Atul 
Gawande that highlights the power of checklists in improving performance and reducing errors. Gawande argues 
that even experts can benefit from using checklists to ensure consistency and enhance teamwork. He provides 
examples from various industries, such as medicine and aviation, to demonstrate how checklists can save lives 
and improve outcomes. The book emphasizes the importance of simplicity, standardization, and communication in 
checklist design and implementation. Overall, it advocates for the systematic use of checklists to enhance 
productivity and safety in complex tasks.''',
    "call_to_arms": "However, you as the developer are responsible for knowing when its time to creativly ignore the checklist and do things differently.",
    "checklists": None,
}

book_link = "https://a.co/d/9DpHQHJ"
book_name = "The Checklist Manifesto"

content_md = {
    "why": readme_content["why"][:],
    "book": readme_content["book"][:].format(f"<a href='{book_link}'>{book_name}</a>"),
    "call_to_arms": readme_content["call_to_arms"][:],
    "checklists": ""
}

content_txt = {
    "why": readme_content["why"][:],
    "book": readme_content["book"][:].format(f"{book_name}"),
    "call_to_arms": readme_content["call_to_arms"][:],
    "checklists": []
}

def checkCwd():
    global cwd
    name = os.path.basename(__file__)
    path = os.path.join(cwd, name)
    if not os.path.exists(path):
        raise Exception("must run script from its own location")

def appendContentMd(new_content):
    global content_md
    content_md["checklists"] = content_md["checklists"] + new_content

def appendContentTxt(new_content, addToLast=False):
    global content_txt
    if addToLast:
        if len(content_txt["checklists"]) == 0:
            content_txt["checklists"] = [new_content]
        else:
            content_txt["checklists"][-1] = content_txt["checklists"][-1] + new_content
    else:
        content_txt["checklists"].append(new_content)
        

def appendChecklist(path):
    with open(path, "r") as file:
        title = file.readline().split(":")[1].strip()
        use = file.readline().split(":")[1].strip()

    path = path.replace(cwd, ".")

    appendContentMd(f"<a href='{path}'>{title}</a> - {use}<br>")
    appendContentTxt(f"{title} - {use}\n",  True)
    
def makeReadme(dirpath, depth=0):
    items = os.listdir(dirpath)
    items = sorted(items, key=lambda x: os.path.isdir(os.path.join(dirpath, x)))

    for item in items:
        appendContentTxt("") 
        for i in range(0, depth):
            #appendContentMd("  ")
            appendContentTxt("  ", True) 
        appendContentMd("* ")
        appendContentTxt("* ", True)

        item_path = os.path.join(dirpath, item)
        
        if os.path.isdir(item_path):
            appendContentMd(f"<a href='{item_path.replace(cwd, '.')}'>{item}</a><br>")
            appendContentTxt(f"{item}\n", True)
            addDirToPdf(item_path, item)         
            makeReadme(item_path, depth + 1)
        else:
            addChecklistToPdf(item_path)
            appendChecklist(item_path)

def writeReadme():
    global readme_path
    global readme_content
    with open(readme_path, "w") as file:
        content = f'''
# Intro
{content_md["why"]}<br><br>
{content_md["book"]}<br><br>
{content_md["call_to_arms"]}<br><br>
# Checklists
{content_md["checklists"]}
        '''
        file.write(content)

def writeTextToPdf(text, addPage=True, pdf=pdf):
    if addPage:
        pdf.add_page()

    chunk_size = int(pdf_width / 2.1)

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

    pdf = initPDF()
    writeContentToPdf(pdf)
    pdf.output(temp_pdf_path)

    # Create an instance of PdfFileMerger
    pdf_merger = PdfMerger()

    # Add the PDF files to be merged
    pdf_merger.append(temp_pdf_path)
    pdf_merger.append(pdf_path)

    # Save the merged PDF to a new file
    pdf_merger.write(pdf_path)

    # Close the PdfFileMerger instance
    pdf_merger.close()

    os.remove(temp_pdf_path)


def writeContentToPdf(pdf=pdf):
    writeTextToPdf("Intro\n", pdf=pdf)
    writeTextToPdf(content_txt["why"], False, pdf=pdf)
    writeTextToPdf("\n", False, pdf=pdf)
    writeTextToPdf(content_txt["book"], False, pdf=pdf)
    writeTextToPdf("\n", False, pdf=pdf)
    writeTextToPdf(content_txt["call_to_arms"], False, pdf=pdf)
    writeTextToPdf("\n", False, pdf=pdf)
    writeTextToPdf("Checklists\n", pdf=pdf)
    for item in content_txt["checklists"]:
        writeTextToPdf(item, False, pdf=pdf)

checkCwd()
makeReadme(directory)
writeReadme()
writePdf()