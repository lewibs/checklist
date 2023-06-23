import os

cwd = os.getcwd()
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

def appendChecklist(path, depth):
    with open(path, "r") as file:
        title = file.readline().split(":")[1].strip()
        use = file.readline().split(":")[1].strip()

    path = path.replace(cwd, "..")

    appendContent(f"<a href='{path}'>{title}</a> - {use}\n")
    
def makeReadme(dirpath, depth=0):
    items = os.listdir(dirpath)
    items.reverse()

    for item in items:
        for i in range(0, depth):
                appendContent("  ") 

        item_path = os.path.join(dirpath, item)
        
        if os.path.isdir(item_path):
            appendContent("\n" + item + "\n")
            makeReadme(item_path, depth + 1)
            appendContent("\n")
        else:
            appendChecklist(item_path, depth)

def writeReadme():
    global readme_path
    global readme_content
    with open(readme_path, "w") as file:
        file.write(readme_content)

def printReadme():
    with open(readme_path, 'r') as file:
        print(file.read())

checkCwd()
makeReadme(directory)
writeReadme()
printReadme()
