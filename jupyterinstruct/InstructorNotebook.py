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


def merge(this_notebook, studentfolder='./', tags={}):
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
               include=['application/javascript'])
    nbfile = nbfilename(this_notebook)

    nb = InstructorNB(filename=this_notebook)

    if nbfile.isDate:
        tags['DUE_DATE'] = nbfile.getlongdate()
        tags['MMDD'] = nbfile.prefix

    nb.removecells(searchstring="#ANSWER#")
    nb.isInstructor = False

    tags['NEW_ASSIGNMENT'] = str(nbfile)

    nb.mergetags(tags)

    studentfile = f"{studentfolder}{tags['NEW_ASSIGNMENT']}"
    nb.writenotebook(studentfile)

    # Make a link for review
    display(
        HTML(f"<a href={studentfile} target=\"blank\">{studentfile}</a>"))


def getname():
    """Get the current notebook's name. This is actually a javascript command and 
    requires some time before the name is stored in the global namespace as ```this_notebook```
    """
    # TODO: Save the contents of the current notebook
    IP.display(IP.Javascript(
        'Jupyter.notebook.kernel.execute("this_notebook = " + "\'"+Jupyter.notebook.notebook_name+"\'");'))


getname()


def nb2html(nb):
    """Helper function to convert a notebook to html for parsing"""
    html_exporter = HTMLExporter()
    html_exporter.template_file = 'basic'
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
    contents = None
    this_notebook = ""
    student_folder = ""
    Autograder_folder = ""

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

        if filename:
            self.this_notebook = filename

        print(f"Myfilename {self.this_notebook}")

        if filename:
            self.contents = readnotebook(self.this_notebook)

    def writenotebook(self, filename=None):
        """Write this notebook to a file"""
        if not filename:
            filename = this_notebook
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

    def removebefore(self, searchstring="#END_HEADER#"):
        """Remove all cells efore cell with ```searchstring``` keyword (default #END_HEADER#)"""
        index = 0
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                self.contents.cells = self.contents.cells[index+1:]
                return
            index = index+1

    def removeafter(self, searchstring="#START_FOOTER#"):
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

    def makestudent(self, tags=None, student_folder=None, filename=None):
        """Make a Student Version of the notebook"""
        if filename:
            self.this_notebook = filename
        if student_folder:
            self.student_folder = student_folder
        merge(self.this_notebook, studentfolder=self.studentfolder, tags=tags)
