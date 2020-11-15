import IPython.core.display as IP
import os
from IPython.core.display import Javascript, HTML
from IPython.display import display
import csv
import datetime
import calendar
import glob
import pathlib
import shutil
import time
import subprocess


def showsubmitted(this_notebook):

    ind = this_notebook.index("INST")-1
    assignment = this_notebook[:ind]

    directories = glob.glob(f'./submitted/*')

    Links = ''
    for d in directories:
        files = glob.glob(f"{d}/{assignment}/*.ipynb")
        myfile = f"{files[0]}"
        Links += f"<a href={myfile} target=\"_blank\">{d}</a></br>"
    # Make a link for review

    display(HTML(Links))


def showfeedback(this_notebook):

    ind = this_notebook.index("INST")-1
    assignment = this_notebook[:ind]

    directories = glob.glob(f'./feedback/*')

    Links = ''
    for d in directories:
        files = glob.glob(f"{d}/{assignment}/*.html")
        myfile = f"{files[0]}"
        Links += f"<a href={myfile} target=\"_blank\">{d}</a></br>"
    # Make a link for review

    display(HTML(Links))

def usenbgrader(this_notebook, coursefolder='./', tags={}):
    # Calculate Destination name
    ASSIGNMENT = this_notebook
    ind = ASSIGNMENT.index("INST")-1
    ext = ASSIGNMENT.index(".ipynb")
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + ASSIGNMENT[ext:]
    GradingFolder = 'AutoGrader'

    ASSIGNMENT_FOLDER = f'./{GradingFolder}/source/{ASSIGNMENT[:ind]}'
    SOURCE_ASSIGNMENT = f'{ASSIGNMENT_FOLDER}/{ASSIGNMENT[:ind]}_STUDENT{ASSIGNMENT[ext:]}'
    RELEASE_ASSIGNMENT = f'./{GradingFolder}/release/{ASSIGNMENT[:ind]}/{ASSIGNMENT[:ind]}_STUDENT{ASSIGNMENT[ext:]}'

    pathlib.Path(ASSIGNMENT_FOLDER).mkdir(parents=True, exist_ok=True)
    time.sleep(2)
    print(coursefolder, NEW_ASSIGNMENT, SOURCE_ASSIGNMENT)
    shutil.move(f"./{coursefolder}/{NEW_ASSIGNMENT}", SOURCE_ASSIGNMENT)
    # pathlib.Path(RELEASE_ASSIGNMENT).unlink()


    command = f'cd {GradingFolder}; nbgrader db assignment add {ASSIGNMENT[:ind]}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")
    
    
    command = f'cd {GradingFolder}; nbgrader generate_assignment {ASSIGNMENT[:ind]}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")
    
    #command = f'cd {GradingFolder}; nbgrader assign {ASSIGNMENT[:ind]}'
    #print(command)
    #returned_output = subprocess.check_output(command, shell=True)
    #print(f"Output: {returned_output.decode('utf-8')}")
#
    command = f'cd {GradingFolder}; nbgrader validate {ASSIGNMENT[:ind]}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    # Make a link for review
    display(
       HTML(f"<a href={RELEASE_ASSIGNMENT} target=\"blank\">{RELEASE_ASSIGNMENT}</a>"))


def unpackD2L(filename, this_notebook, coursefolder='./', destination='upziptemp'):
    from pathlib import Path
    from urllib.request import urlretrieve
    import zipfile
    import pathlib

    ind = this_notebook.index("INST")-1
    assignment = this_notebook[:ind]

    zfile = Path(filename)

    print(f"Unzipping {filename}")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(f"./{coursefolder}/{destination}")

    files = glob.glob(f'./{coursefolder}/{destination}/*.ipynb')

    SUBMITTED_ASSIGNMENT = f'./{coursefolder}/submitted/'
    for f in files:
        name = f.split(' - ')
        [first,last] = name[1].split(' ')
        directory = name[1].replace(' ', '_')
        
#        command=f"cd {coursefolder}; nbgrader db student add {directory} --last-name=${last} --first-name=${first}"
#        print(command)
#        returned_output = subprocess.check_output(command, shell=True)
        
        myfolder = SUBMITTED_ASSIGNMENT+directory+'/'+assignment
        pathlib.Path(myfolder).mkdir(parents=True, exist_ok=True)
        pathlib.os.rename(f, f"{myfolder}/{assignment}_STUDENT.ipynb")
    
#     command=f"cd {coursefolder}; ../upgrade.sh"
#     print(command)
#     returned_output = subprocess.check_output(command, shell=True)
    
#     command=f"cd {coursefolder}; nbgrader autograde {assignment}"
#     print(command)
#     returned_output = subprocess.check_output(command, shell=True)
        
#            echo "folder name is ${d}"
#    name=`echo $d | cut -d '/' -f3`
#    first=`echo $name | cut -d '_' -f1`
#    last=`echo $name | cut -d '_' -f2`
#    echo nbgrader db student add ${name} --last-name=${last} --first-name=${first}
#    nbgrader db student add ${name} --last-name=${last} --first-name=${first}

def getname():
    print("getting name")
    IP.display(IP.Javascript(
        'Jupyter.notebook.kernel.execute("this_notebook = " + "\'"+Jupyter.notebook.notebook_name+"\'");'))


def convert(this_notebook, studentfolder='./'):
    import os
    from IPython.core.display import Javascript, HTML
    from IPython.display import display

    print("Save Current Notebook")
    IP.display(IP.Javascript("Python.notebook.save_notebook()"),
               include=['application/javascript'])

    # Calculate Destination name
    ASSIGNMENT = this_notebook
    ind = ASSIGNMENT.index("INST")
    ext = ASSIGNMENT.index(".ipynb")
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

    print("Removing existing student version")
    command = f"rm {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    print("Stripping out ANSWER feilds")
    command = f"python ./instruct/makeStudentVersion.py {this_notebook}"
    os.system(command)

    # Move to the working directory
    print("Moving to working directory")
    command = f"mv {NEW_ASSIGNMENT} {studentfolder}"
    os.system(command)

    # Strip output
    print("Striping output cells")
    command = f"python ./instruct/nbstripout {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    # Make a link for review
    display(HTML(
        f"<a href={studentfolder}{NEW_ASSIGNMENT} target=\"_blank\">{NEW_ASSIGNMENT}</a>"))


def merge(this_notebook, studentfolder='./', tags={}):

    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),
               include=['application/javascript'])

    # Calculate Destination name
    ASSIGNMENT = this_notebook
    ind = ASSIGNMENT.index("INST")-1
    ext = ASSIGNMENT.index(".ipynb")
    #NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + ASSIGNMENT[ext:]

    tags['NEW_ASSIGNMENT'] = NEW_ASSIGNMENT
    
    try:
        month = int(NEW_ASSIGNMENT[0:2])
        day = int(NEW_ASSIGNMENT[2:4])

        print(f"TESTING {day} {month} {tags['YEAR']}")
        my_date = datetime.datetime(int(tags['YEAR']), month, day)
        #my_date = date.today()
        weekday = calendar.day_name[my_date.weekday()]

        mnth = calendar.month_name[month]
        tags['DUE_DATE'] = f'{weekday} {mnth} {day}'
        tags['MMDD'] = NEW_ASSIGNMENT[0:4]
    except:
        print("Date not found")

    print("Removing existing student version")
    command = f"rm {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    with open(ASSIGNMENT, 'r+', encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []
    LIMIT = len(lines)

    i = 0
    while i < LIMIT:
        if '"code"' in lines[i]:
            found = False
            next_ind = i

            while not found:
                if '"source"' in lines[next_ind]:
                    found = True
                next_ind += 1

            if "ANSWER" in lines[next_ind]:
                del new_lines[-1]
                temp = lines[i:]
                i = i + temp.index("  },\n") + 1
            else:
                new_lines.append(lines[i])
                i += 1

        if '"markdown"' in lines[i]:
            found = False
            next_ind = i

            while not found:
                if '"source"' in lines[next_ind]:
                    found = True
                next_ind += 1

            if "ANSWER" in lines[next_ind]:
                del new_lines[-1]
                temp = lines[i:]
                i = i + temp.index("  },\n") + 1
            else:
                new_lines.append(lines[i])
                i += 1
        else:
            new_lines.append(lines[i])
            i += 1

    print("Finding and replacing mailmerge tags")
    lines = []
    for row in new_lines:
        for key in tags:
            if (key in row):
                if key == 'LINKS':
                    linkstr = '\\n\",\n'
                    for link in tags[key]:
                        linkstr=linkstr+f'    \"- [{link}]({tags[link]})\\n\",\n'
                    print("link found")
                    linkstr=linkstr+f'    \"\\n'
                    row = row.replace(f"###{key}###", linkstr)
                else:
                    row = row.replace(f"###{key}###", tags[key])
                print(row)
        lines.append(row)

    with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as f:
        for l in lines:
            f.write(l)

    for line in lines:
        if "ANSWER" in line:
            print("WARNING! Some answer content may remain in the file. Please double check file contents before administering to students.")
            break

    # Move to the working directory
    print("Moving to working directory")
    command = f"mv {NEW_ASSIGNMENT} {studentfolder}"
    os.system(command)

    # Strip output
    print("Striping output cells")
    command = f"python ./instruct/nbstripout {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    # Make a link for review
    display(HTML(
        f"<a href={studentfolder}{NEW_ASSIGNMENT} target=\"blank\">{NEW_ASSIGNMENT}</a>"))
thisnotebook=getname()