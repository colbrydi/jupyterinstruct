import IPython.core.display as IP
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import datetime
import calendar
import re        
        

def getname():
    IP.display(IP.Javascript(
        'Jupyter.notebook.kernel.execute("this_notebook = " + "\'"+Jupyter.notebook.notebook_name+"\'");'))

def nb2html(nb):
    html_exporter = HTMLExporter()
    html_exporter.template_file = 'basic'
    (body, resources) = html_exporter.from_notebook_node(nb)
    return (body, resources)

def generateTOCfromHTML(body):   
    headerlist = []
    toc = []
    body = body.replace(r'&#182;','')
    tree = BeautifulSoup(body)
    index = 0
    for header in tree.find_all(name='h1'):
        contents = header.prettify()
        if contents:
            name = re.match(r'[0-9]\.[^\s]*',header['id'])
            if name:
                index = index + 1
                name = name.string[3:]
                text = name.replace('-', ' ')
                toc.append(f"{index}. [{text}](#{name})")
                headerlist.append((name,text))
                print(toc[-1])

    index = 0
    for name, text in headerlist:
        print("\n\n")
        index = index + 1
        print(f"---\n<a name={name}></a>\n# {index}. {text}")

    return toc, headerlist


def makeindex(nb):
    htmltext = nb2html(nb)
    print(htmltext)
    html = generateTOCfromHTML(htmltext[0])

def readnotebook(filename):
    """Reads in a notebook and returns as a nbformat object"""
    with open(filename) as file:
        text = file.read()
        nb = nbformat.reads(text, as_version=4) 
    return nb

def writenotebook(filename,nb):
    text = nbformat.writes(nb)
    with open(filename, mode="w") as file:
        file.write(text)

def header_footer(filename=None, 
                  headerfile = "Header.ipynb", 
                  footerfile = "Footer.ipynb", 
                  nb = None):

    header_nb = readnotebook(headerfile)
    footer_nb = readnotebook(footerfile)
    if nb == None:
        nb = readnotebook(filename) 
    
    if header_nb.cells[0] == nb.cells[0]:
        print('header seems to be the same. Aborting...')
        print(header_nb.cells[0])
        return

    nb.cells = header_nb.cells + nb.cells + footer_nb.cells

    return nb


def init_thiscourse():
    """Generate a thiscourse.py file"""
    return
    
class InstructorNB():
    """Class for instructor notebooks. Allows instructors to make student versions"""
    contents = None
    this_notebook = ""
    student_folder = ""
    Autograder_folder = ""
    
    def checklinks(self):
        pass
    
    
    def __init__(self, 
                 filename, 
                 studnet_folder=None, 
                 Autograder_folder=None, 
                 thiscourse = None):
        
        if filename:
            self.this_notebook = filename
            
        print(f"Myfilename {self.this_notebook}")
        
        if filename:
            self.contents = readnotebook(self.this_notebook)

    def getDateString(self):
        pass
    
    def headerfooter(self):
        header_footer(nb=self.contents)
    
    def makeindex(self):
        makeindex(self.contents)
        
    def stripAnswer(self):
        pass
    
    def mergetags(self,tags={}):
        pass
    
    def makestudent(self, tags=None, student_folder=None, filename=None):
        if filename:
            self.this_notebook = filename
        if student_folder:
            self.student_folder = student_folder
        merge(self.this_notebook, studentfolder=self.studentfolder, tags=tags)
        
        
getname()
   
        
        
        