"Tools for generating course websites from course folder."""

from jupyterinstruct.InstructorNotebook import InstructorNB, nb2html
from pathlib import Path
from nbconvert.preprocessors import ExecutePreprocessor
import shutil
from IPython.display import Markdown
from jupyterinstruct.nbfilename import nbfilename

def makedateschedule(assignment_folder='assignments'):
    '''Make an index.md file inside the assignment_folder with references to html and ipynb files'''
    S_path = Path(assignment_folder)
    StudentFiles = S_path.glob(f"*.ipynb")

    nameset = set()
    for file in StudentFiles:
        nbfile = nbfilename(file)
        if nbfile.isDate:
            nameset.add(str(nbfile))

    I_path = Path('.')
    InstructorFiles = I_path.glob(f"*.ipynb")

    schedule = ""
    schedule += "| Date | Assignment Number | Type | Topic | Link to Notebook |\n"
    schedule += "|------|--------|------|-------|----------|\n"

    for file in sorted(InstructorFiles):
        nbfile = nbfilename(str(file))
        if(nbfile.isInstructor and nbfile.isDate):
            nbfile.isInstructor = False
            thisfile = str(nbfile)

            filetype = " "
            if nbfile.isPreClass:
                filetype = "Pre-Class Assignment"
            if nbfile.isInClass:
                filetype = "In-Class Assignment"
            nbfile.isInClass = False
            nbfile.isPreClass = False

            if thisfile in nameset:
                schedule += f"|  {nbfile.getlongdate()}, 2021  | {nbfile.basename()[0:4]} | {filetype} | [{nbfile.basename()[5:]}](./{thisfile[:-6]}.html) | [ipynb](./{str(thisfile)}) |\n"
            else:
                schedule += f"| {nbfile.getlongdate()}, 2021   | {nbfile.basename()[0:4]} | {filetype} | {nbfile.basename()[5:].replace('_',' ')} |\n"
                
    indexfile = Path(assignment_folder,'index.md')
                     
    # Read in the file
    with open(indexfile, 'w') as file:
        file.write(schedule)
        
    return schedule


def publish2folder(notebook, website_folder, assignment_folder='assignments', datefile=None):
    '''Copy the notebook to the website_folder/assignment_folder and make an html copy of it. 
    Automatically generate the index.md schedule file'''

    #Copy Notebookfile
    from_file = Path(notebook)
    full_path = Path(website_folder,assignment_folder)
    to_file = Path(full_path,from_file.name)
    shutil.copy(from_file, to_file)  # For newer Python.

    
    destination = Path(full_path,str(from_file.stem)+".html")
    nb = InstructorNB(notebook)
    
    (body, resources) = nb2html(nb.contents)
    
    # Read in the file
    with open(destination, 'w') as file:
        file.write(body)
    
    if datefile == None:
        output = makedateschedule(full_path)
        
     #Make a link for review
    return Markdown(f"[{destination}]({destination})\n\n{output}")
    