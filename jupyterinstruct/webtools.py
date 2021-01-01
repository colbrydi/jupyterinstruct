"Tools for generating course websites from course folder."""

from jupyterinstruct.InstructorNotebook import InstructorNB, nb2html
from pathlib import Path
from nbconvert.preprocessors import ExecutePreprocessor
import shutil
from IPython.display import Markdown
from jupyterinstruct.nbfilename import nbfilename

import pandas


def makecsvschedule(csvfile = 'CMSE314-001-NLA-S21_Schedule.csv', 
                    assignmentsfolder = './mth314-s21-student/assignments/',
                    sections= ["Section 001", "Section 002", "Section 003", "Section 004-005"],
                    times = ["Tu Th 10:20AM - 11:40AM", 
                             "M W 12:40PM - 2:00PM", 
                             "Tu Th 1:00PM - 2:20PM", 
                             "M W 12:40PM - 2:00PM"]):
    
    df = pandas.read_csv(csvfile)

    webfolder = Path(assignmentsfolder)

    output = ""
    files = set()
    mdfiles = set()
    webfiles= set()

    
    for file in webfolder.glob('*.md'):
        mdfiles.add(str(file.name))
    
    for file in webfolder.glob('*.html'):
        webfiles.add(str(file.name))
    
    for file in webfolder.glob('*.ipynb'):
        files.add(str(file.name))

    
    schedulefiles = []

    for section, tm in zip(sections, times):
        schedule = f"# MTH314 {section} \n\n {tm}\n\n"
        schedule += "| Date | Assignment | Link to Notebook |\n"
        schedule += "|------|------------|------------------|\n"
        for i, row in df.iterrows():
            file = row['Assignment']
            if isinstance(file,str):
                if 'ipynb' in file:
                    nbfile = nbfilename(file)
                    nbfile.isInstructor = False
                    
                    schedule += f"| {row[section]} |"
                    
                    webname = f"{nbfile.basename()}.html"
                    
                    if webname in webfiles:
                        schedule += f" [{nbfile.basename()}]({webname}) |"
                    else:
                        schedule += f" {nbfile.basename()} |"
                        
                    if str(nbfile) in files:
                        schedule += f" [ipynb]({str(nbfile)}) |\n"
                    else:
                        schedule += f"      |\n"
                else:
                    webname = f"{file}.md"
                    
                    schedule += f"| {row[section]} |"

                    if webname in mdfiles:
                        schedule += f" [{file}]({webname}) |       |\n"
                    else:
                        webname = f"{file}.html"
                        if webname in webfiles:
                            schedule += f" [{file}]({webname}) |       |\n"
                        else:
                            schedule += f" {file} |      |\n"


        name = section.replace(' ','_')
        schedulefile = f"{assignmentsfolder}{name}.md" 
        with open(schedulefile, "w") as file_object:
                file_object.write(schedule)      
        schedulefiles.append(schedulefile) 
    return schedulefiles
                    

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
    schedule += "| Due Date | Assignment Number | Type | Topic | Link to Notebook |\n"
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
                
    indexfile = Path(assignment_folder,'Schedule.md')
                     
    # Read in the file
    with open(indexfile, 'w') as file:
        file.write(schedule)
        
    return str(indexfile) 

def publish(notebook, outfolder='./', execute=True):

    #Copy Notebookfile
    from_file = Path(notebook)
    out_path = Path(outfolder)
    to_file = Path(out_path,from_file.name)
    
    if not from_file == to_file:
        shutil.copy(from_file, to_file)  # For newer Python.
    else:
        print('Source and destination are the same')

    destination = Path(out_path,str(from_file.stem)+".html")
    nb = InstructorNB(notebook)
    
    try:
        ep = ExecutePreprocessor(timeout=30, 
                                 kernel_name='python3', 
                                 allow_errors=True)
        ep.preprocess(nb.contents)

        nb.removeoutputerror()
    except Exception as e:
        print(f"   WARNING: Notebook preprocess Timeout (check for long running code)\n {e}")
    
    (body, resources) = nb2html(nb)
    
    # Read in the file
    with open(destination, 'w') as file:
        file.write(body)
    return destination

def publish2folder(notebook, website_folder='./',  csvfile=None):
    '''Copy the notebook to the website_folder/assignment_folder and make an html copy of it. 
    Automatically generate the index.md schedule file'''
    
    destination = publish(notebook, str(Path(website_folder)))
    
    if csvfile == None:
        print("generating schedule from file dates")
        output = makedateschedule(website_folder)
    else:
        print(f"generating schedule from csv file {csvfile}")
        output =  makecsvschedule(csvfile, website_folder)
        
     #Make a link for review
    return Markdown(f"[{destination}]({destination})\n\n{output}")
