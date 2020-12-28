'''The base notebook class object.
Instuctor notebooks have extra content intended only for instructors. This class manages the extra content and enables instructors to generate student versions of the notebooks.  
'''
import IPython.core.display as IP
import IPython.core.display as display
from IPython.core.display import Javascript, HTML

from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import datetime
import calendar
import re

from pathlib import Path
import os


import nbformat

from jupyterinstruct.nbvalidate import validate
from jupyterinstruct.nbfilename import nbfilename


def renamefile(oldname, newname, MAKE_CHANGES=False, force=False):
    """Function to rename a file using git and updates all links to the file and checks.
    
    Parameters
    ----------
    oldname : string
        Current name of the file
    newname : string
        New name for file
    MAKE_CHANGES : boolean
        Dry run name change to see what files are affected.
    force : boolean
        Ignore warnings and force the copy
    """
   
    old_nbfile = nbfilename(oldname)
    if not oldname == str(old_nbfile):
        print(f"WARNING: old file {oldname} does not conform to naming standard")
        if not force:
            print(f"   Set force=True to change anyway")
            return
        oldstudentversion = f"{oldname[:-17]}"
    else:
        old_nbfile.isInstructor = False
        oldstudentversion = str(old_nbfile)

    new_nbfile = nbfilename(newname)
    if not newname == str(new_nbfile):
        print(f"ERROR: new file {newname} does not conform to naming standard")
        print(f"       using {str(new_nbfile)}")
    
    #STEP 1. Move instructor file to new name
    cmd = f"git mv {oldname} {str(new_nbfile)} "
    if MAKE_CHANGES:
        os.system(cmd)
    else:
        print(f"TEST: {cmd}")
        
    #Forcing new file to conform to the file standard
    new_nbfile.isInstructor = False
    newstudentversion = str(new_nbfile)
    
    print(f" Replaceing {oldstudentversion} with {newstudentversion}")

    directory = Path('.')
    for file in directory.glob('*.ipynb'):
        temp_np_file = nbfilename(str(file))
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


def changeprefix(filename, datestr, MAKE_CHANGES=False, force=False):
    """Migrate a notebook from the filename to the new four digit date string
    
    Parameters
    ----------
    filename : string
        Current name of the Instructor notebook with the date prefix
    datestring : string
        New Datestring of the form MMDD (MONTH, DAY)
    MAKE_CHANGES : boolean
        Dry run name change to see what files are affected.
    force : boolean
        Ignore warnings and force the copy
    """
    
    nbfile = nbfilename(filename)
    if not nbfile.isDate:
        print("ERROR: file not formated as a date file")
        return

    directory = Path('.')
    files = directory.glob('*.ipynb')
    if not Path(filename).exists():
        print(f"ERROR: File {filename} not found in directory")
        return
    oldname = filename
    newname = f"{datestr}{oldname[4:]}"
    renamefile(oldname, newname, MAKE_CHANGES, force)


def makestudent(filename, studentfolder='./', tags={}):
    """Make a student from an instructor noatebook
    
    Parameters
    ----------
    filename : string
        Current name of the Instructor notebook with the date prefix
    studentfolder : string
        Name of folder to save the student notebook
    tags: dictionary
        Dictionary of Tag values (key) and replacment text (values). 
    """
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
               include=['application/javascript'])

    nb = InstructorNB(filename=filename)
    
    studentfile = nb.makestudent(tags=tags, studentfolder=studentfolder)
    
    nb.writenotebook(studentfile)
    
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
    """Run javascript in the current notebook to clear all output and save the notebook."""    
    IP.display(IP.Javascript("IPython.notebook.clear_all_output()"),
               include=['application/javascript'])
    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
               include=['application/javascript'])


getname()


def nb2html(nb):
    """Helper function to convert a notebook to html for parsing
    
    Parameters
    ----------
    nb : InstructorNotebook
        Input Notebook
    Returns
    -------
    (string, string)
        body and resurcers from teh html_export file
    """
    html_exporter = HTMLExporter()
    #html_exporter.template_file = 'basic'
    (body, resources) = html_exporter.from_notebook_node(nb)
    return (body, resources)


def generateTOCfromHTML(body):
    """Generate the Table of Contents from html headers
    
    Parameters
    ----------
    body : string
        html input string
    """
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
    with open(filename, 'w', encoding='utf-8') as file:
        nbformat.write(nb, file)

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

    def removeoutputerror(self):
        '''Loop though output cells and delete any with 'error' status'''
        for cell in self.contents.cells:
            if 'outputs' in cell:
                for output in cell['outputs']:
                    if output['output_type'] == 'error':
                        cell['outputs'] = []
                 
    def removecells(self, searchstring="#ANSWER#", verbose=True):
        """Remove with ```searchstring``` keyword (default #ANSWER#)"""
        newcells = []
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                if verbose:
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
        if found >= 0:
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
    
    
    def incertbefore(self, searchstring="###STARTHEADER###", notebook="", verbose=True):
        """Incert cells from notebook before all cells that have  ```searchstring``` keyword"""
        incertbook = readnotebook(notebook)
        newcells = []
        for cell in self.contents.cells:
            if searchstring in cell['source']:
                if verbose:
                    print(f"\incerting {cell['source']}\n")
                newcells = newcells + incertbook.cells    
            newcells.append(cell)
        self.contents.cells = newcells
        
    def incertafter(self, searchstring="###ENDHEADER###", notebook="", verbose=True):
        """Incert cells from notebook after all cells that have  ```searchstring``` keyword"""
        incertbook = readnotebook(notebook)
        newcells = []
        for cell in self.contents.cells:
            newcells.append(cell)
            if searchstring in cell['source']:
                if verbose:
                    print(f"\nincerting {cell['source']}\n")
                newcells = newcells + incertbook.cells    
        self.contents.cells = newcells

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
                cell['execution_count'] = None

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

    def makestudent(self, tags=None, studentfolder=''):
        """Make a Student Version of the notebook"""
        
        instructor_fn = self.filename
        
        instructorfile = nbfilename(instructor_fn)

        # TODO: check all links in the directory for name change.
        if not str(instructorfile) == instructor_fn:
            print(f"WARNING: Instructor file name is wrong {instructorfile} != {instructor_fn}")
            
        
        IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
                   include=['application/javascript'])

        studentfile = nbfilename(instructor_fn)

        if studentfile.isDate:
            tags['DUE_DATE'] = studentfile.getlongdate()
            tags['MMDD'] = studentfile.prefix

        self.removecells(searchstring="#ANSWER#",verbose=False)
        self.stripoutput()

        # Remove INSTRUCTOR from name
        studentfile.isInstructor = False
        self.filename = str(studentfile)

        tags['NEW_ASSIGNMENT'] = str(studentfile)
        print(tags['NEW_ASSIGNMENT'])
        self.mergetags(tags)

        student_fn = f"{studentfolder}{studentfile}"
        
        
        if Path(instructor_fn) == Path(student_fn):
            print("ERROR: student file will overrite instructor. Aborting")
            print(f"   {instructor_fn} --> {student_fn}")
            return
                  
        # Make a link for review
        IP.display(HTML(f"<a href={student_fn} target=\"blank\">{student_fn}</a>"))

        return student_fn 
