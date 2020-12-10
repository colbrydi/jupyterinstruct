import IPython.core.display as IP
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import datetime
import calendar
import re
import IPython.core.display as IP
from IPython.core.display import Javascript, HTML


from jupyterinstruct.nbfilename import nbfilename

import os
import requests
import nbformat
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
from pathlib import Path
from nbconvert.preprocessors import ExecutePreprocessor

def checkurl(url):
    request = requests.get(url, timeout=5)
    output = 0
    if not request.status_code < 400:

        output = 1
    return output


def validate(filename):
    '''Function to validate links and content of a IPYNB'''
    print(f"Validating Notebook {filename}")
    
    parts = Path(filename)
    foldername = parts.parent
    
    # Read in the file
    with open(filename, 'r') as file:
        text = file.read()

    nb = nbformat.reads(text, as_version=4) #ipynb version 4
    
    #may be needed for video verification
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)
    ep.preprocess(nb)

    # Process the notebook we loaded earlier
    (body, resources) = HTMLExporter().from_notebook_node(nb)

    #print(body)
    soup = BeautifulSoup(body, 'html.parser')
    anchorlist = dict()
    links = soup.find_all('a',href=False)
    for link in links:
        anchorlist[link['name']] = False
        
    errorcount = 0
    
    links = soup.find_all('a',href=True)
    for link in links:
        href = link['href']
        try:
            if len(href) > 0:
                if href[0] == "#":
                    anchorlist[href[1:]] = True
                else:
                    if href[0:4] == "http":
                        error = checkurl(href)
                        if error:
                            print(f'   LINK ERROR - {href}') 
                            errorcount += error
                    else:
                        if not os.path.isfile(f'{foldername}/{href}'):
                            print(f'   File Doesn\'t Exist - {href}')
                            errorcount +=1
            else:
                print(f"   Empty Link - {link}")
                errorcount +=1
        except Exception as e:
            print(f"   Timeout Warning for  {link}\n {e}")
            errorcount +=1
            
    for anchor in anchorlist:
        if not anchorlist[anchor]:
            print(f"   Missing anchor for {anchor}")
            errorcount +=1
            
    ##Verify video links
    iframes = soup.find_all('iframe')    
    for frame in iframes:
        error = checkurl(frame['src'])
        if error:
            print(f'   Iframe LINK ERROR - {href}') 
            errorcount += error
            
    ##Verify img links     
    images = soup.find_all('img')    
    for img in images:
        image = img['src']
        if not image[0:4]=='data':
            error = checkurl(img['src'])
            if error:
                print(f'   Image LINK ERROR - {href}') 
                errorcount += error

    return errorcount
        


def renamefile_new(oldname, newname, MAKE_CHANGES=False, force=False):

    old_nbfile = nbfilename(oldname)
    if not oldname == str(old_nbfile):
        print(f"ERROR: file {oldname} does not conform to naming standard")
        if not force:
            print(f"   Set force=True to change anyway")
            return
        
    new_nbfile = nbfilename(newname)
    if not newname == str(new_nbfile):
        print(f"ERROR: file {newname} does not conform to naming standard")
        print(f"       using {str(new_nbfile)}")
        
    cmd = f"git mv {oldname} {str(new_nbfile)} "
    
    old_nbfile.isInstructor = False
    new_nbfile.isInstructor = False
    
    if MAKE_CHANGES:
        os.system(cmd)
    else:
        print(f"TEST: {cmd}")
    
    directory = Path('.')
    for file in directory.glob('*.ipynb'):
        temp_np_file = nbfile(str(file))
        if temp_np_file.isInstructor:
            with open(file, encoding="utf-8") as f:
                s = f.read()
            if oldstudentversion in s:
                s = s.replace(oldstudentversion, newstudentversion)
                if MAKE_CHANGES:
                    print("writing changed file")
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(s)
                else:
                    print(f"TEST: Student File Reference in {file}")

def notebook(filename, datestr, MAKE_CHANGES=False, force=False):
    """Migrate a notebook from the filename to the new four digit date string"""
    
    nbfile = nbfilename(filename)
    if not nbfile.isDate:
        print("ERROR: file not formated as a date file")
        return 
    
    directory = Path('.')
    files = directory.glob('*.ipynb')
    if not Path(filename).isfile():
        print(f"ERROR: File {filename} not found in directory")
        return
    oldname = filename
    newname = f"{datestr}{oldname[4:]}"
    renamefile(oldname, newname, MAKE_CHANGES, force)

def makestudent(this_notebook, studentfolder='./', tags={}):
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
               include=['application/javascript'])

    nb = InstructorNB(filename=this_notebook)
    studentfile = nb.makestudent(tags=tags, studentfolder=studentfolder)
    return studentfile

def getname():
    """Get the current notebook's name. This is actually a javascript command and 
    requires some time before the name is stored in the global namespace as ```this_notebook```
    """
    # TODO: Save the contents of the current notebook
    IP.display(IP.Javascript(
        'Jupyter.notebook.kernel.execute("this_notebook = " + "\'"+Jupyter.notebook.notebook_name+"\'");'))
    
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
           include=['application/javascript'])

def cleanNsave():
    IP.display(IP.Javascript("IPython.notebook.clear_all_output()"),
           include=['application/javascript'])
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
           include=['application/javascript'])

getname()


def nb2html(nb):
    """Helper function to convert a notebook to html for parsing"""
    html_exporter = HTMLExporter()
    #html_exporter.template_file = 'basic'
    (body, resources) = html_exporter.from_notebook_node(nb)
    return (body, resources)


def generateTOCfromHTML(body):
    """Generate the Table of Contents from html headers"""
    headerlist = []
    toc = []
    body = body.replace(r'&#182;', '')
    tree = BeautifulSoup(body)
    index = 0
    for header in tree.find_all(name='h1'):
        contents = header.prettify()
        if contents:
            name = re.match(r'[0-9]\.[^\s]*', header['id'])
            if name:
                index = index + 1
                name = name.string[3:]
                text = name.replace('-', ' ')
                toc.append(f"{index}. [{text}](#{name})")
                headerlist.append((name, text))
                print(toc[-1])

    index = 0
    for name, text in headerlist:
        print("\n\n")
        index = index + 1
        print(f"---\n<a name={name}></a>\n# {index}. {text}")

    return toc, headerlist


def makeTOC(nb):
    """Make an index from markdown headers in a notebook"""
    htmltext = nb2html(nb)
    html = generateTOCfromHTML(htmltext[0])


def readnotebook(filename):
    """Reads in a notebook and returns as a nbformat object"""
    with open(filename) as file:
        text = file.read()
        nb = nbformat.reads(text, as_version=4)
    return nb


def writenotebook(filename, nb):
    """Writes out the notebook object"""
    text = nbformat.writes(nb)
    with open(filename, mode="w") as file:
        file.write(text)


def header_footer(filename=None,
                  headerfile="Header.ipynb",
                  footerfile="Footer.ipynb",
                  nb=None):
    """Adds a header and footer to a notebook"""
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

    def checklinks(self):
        pass

    def maketaglist(self):
        tags = {}
        for cell in self.contents.cells:
            sttring = cell['source']
            taglist = re.findall(r'###[^\n #]*###', cell['source'])
            for tag in taglist:
                tags[tag[3:-3]] = ''
        return tags

    def gen_thiscourse_py(self):
        tags = self.maketaglist()
        codestring = "def tags():\n"
        codestring += "    tags = {}\n"
        for tag in tags:
            codestring += f"    tags['{tag}']='{tags[tag]}'\n"
        codestring += "    return tags\n\n"
        return codestring

    def __init__(self,
                 filename,
                 studnet_folder=None,
                 Autograder_folder=None,
                 thiscourse=None):

        self.filename = ""

        if filename:
            self.filename = filename

        print(f"Myfilename {self.filename}")

        if filename:
            self.contents = readnotebook(self.filename)
        else:
            contents = None

    def writenotebook(self, filename=None):
        """Write this notebook to a file"""
        if not filename:
            filename = self.filename
        writenotebook(filename, self.contents)

    def removecells(self, searchstring="#ANSWER#"):
        """Remove with ```searchstring``` keyword (default #ANSWER#)"""
        newcells = []
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                print(f"\nREMOVING {cell['source']}\n")
            else:
                newcells.append(cell)
        self.contents.cells = newcells

    def removebefore(self, searchstring="#ENDHEADER#"):
        """Remove all cells efore cell with ```searchstring``` keyword (default #END_HEADER#)"""
        index = 0
        found = -1
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                found = index
            index = index+1
        if found >=0:
            self.contents.cells = self.contents.cells[found+1:]
        return
       

    def removeafter(self, searchstring="#STARTFOOTER#"):
        """Remove all cells efore cell with ```searchstring``` keyword (default #START_FOOTER#)"""
        index = 0
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                self.contents.cells = self.contents.cells[:index]
                return
            index = index+1

    def replacecell(self, searchstring="###TOC###", cellfile="Footer.ipynb"):
        """Replace a cell based on a search string with the contents of a file"""
        nb_cells = readnotebook(cellfile)
        newcells = []
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                print(f"\nREMOVING {cell['source']}\n")
                newcells.append(nb_cells)
            else:
                newcells.append(cell)
        self.contents.cells = newcells
   
    def stripoutput(self):
        for cell in self.contents.cells:
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                cell['execution_count']= None

    def headerfooter(self, headerfile="Header.ipynb", footerfile="Footer.ipynb", ):
        """Append Header and Footer files to the current notebook"""
        header_footer(headerfile=headerfile,
                      footerfile=footerfile, nb=self.contents)

    def makeTOC(self):
        """Print out an index for the current notebook. Currently this can be cut and pasted into the notebook"""
        makeTOC(self.contents)

    def mergetags(self, tags={}):
        """Function to replace tags in the entire document"""
        for cell in self.contents.cells:
            source_string = cell['source']
            for key in tags:
                if (key in source_string):
                    if key == 'LINKS':
                        linkstr = '\n'
                        for link in tags[key]:
                            linkstr = linkstr+f' - [{link}]({tags[link]})\n'
                        linkstr = linkstr+f'\n'
                        source_string = source_string.replace(
                            f"###{key}###", linkstr)
                    else:
                        source_string = source_string.replace(
                            f"###{key}###", tags[key])
            cell['source'] = source_string

    def makestudent(self, tags=None, studentfolder='', filename=None):
        """Make a Student Version of the notebook"""
        if filename:
            self.filename = filename
            
        IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
                   include=['application/javascript'])
        
        nbfile = nbfilename(self.filename)        
        
        if nbfile.isDate:
            tags['DUE_DATE'] = nbfile.getlongdate()
            tags['MMDD'] = nbfile.prefix

        self.removecells(searchstring="#ANSWER#")
        self.stripoutput()

        #Remove INSTRUCTOR from name
        nbfile.isInstructor = False
        self.filename = str(nbfile)

        tags['NEW_ASSIGNMENT'] = str(nbfile)
        print(tags['NEW_ASSIGNMENT'])
        self.mergetags(tags)

        studentfile = f"{studentfolder}{tags['NEW_ASSIGNMENT']}"
        self.writenotebook(studentfile)

        #TODO: check all links in the directory for name change.
        if not self.filename == filename:
            print("WARNING: file may be changing {self.filename} != {filename}")
            
        # Make a link for review
        display(
            HTML(f"<a href={studentfile} target=\"blank\">{studentfile}</a>"))
        
        return studentfile

