"""makestudent is a Depreciated library - only maintained for reverse compatibility.
   Use InstructorNotebook instead.
"""


from jupyterinstruct.nbfilename import nbfilename
from pathlib import Path
from IPython.core.display import Javascript, HTML
import subprocess
import shutil
import time
import pathlib
from jupyterinstruct import InstructorNotebook as inb



def merge(this_notebook, studentfolder='./', tags={}):
    warnings.warn(
        "merge is deprecated, use InstructorNotebook.makestudent() instead",
        DeprecationWarning
    )
    inb.makestudent(this_notebook, studentfolder=studentfolder, tags=tags)


def getname():
    warnings.warn(
        "getname is deprecated, use InstructorNotebook.getname() instead",
        DeprecationWarning
    )
    inb.getname()


# LEGACY CODE: NEED TO REFACTOR TO NEW FORMAT


def usenbgrader(this_notebook, coursefolder='./', tags={}):
    warnings.warn(
        "usenbgrader will be deprecated in the future.",
        DeprecationWarning
    )
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
    # print(command)
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


def usenbgrader_new(instructor_notebook, coursefolder='./', GradingFolder='AutoGrader'):
    warnings.warn(
        "usenbgrader will be deprecated in the future.",
        DeprecationWarning
    )
    nbfile = nbfilename(instructor_notebook)
    nbfile.isInstructor = False

    # Calculate Destination name
    student_notebook = str(nbfile)
    basename = nbfile.basename()
    studentfile = basename+"_STUDENT.ipynb"

    # Create the assignment folder inside the gradingfolder/source directory.
    # Assignment folder should have the basename of the student file.
    SOURCE_FOLDER = Path(f'./{GradingFolder}/source/{basename}')
    RELEASE_FOLDER = Path(f'./{GradingFolder}/release/{basename}')

    # Clean out Autograder folders
    if SOURCE_FOLDER.exists():
        print(f'REMOVING {str(SOURCE_FOLDER)}')
        shutil.rmtree(SOURCE_FOLDER)
    if RELEASE_FOLDER.exists():
        print(f'REMOVING {str(RELEASE_FOLDER)}')
        shutil.rmtree(RELEASE_FOLDER)

    # Create Source folder
    SOURCE_FOLDER.mkdir(parents=True, exist_ok=True)

    # Copy the STUDENT file to the SOURCE_FOLDER (also applend the STUDENT end of thefile.
    shutil.move(f"./{coursefolder}/{student_notebook}",
                f"{SOURCE_FOLDER}/{studentfile}")

    # Add the assignment basename to teh
    command = f'cd {GradingFolder}; nbgrader db assignment add {basename}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    # Generate student version of assignment and put in relase folder
    command = f'cd {GradingFolder}; nbgrader generate_assignment {basename}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    # validate student version of assignment
    command = f'cd {GradingFolder}; nbgrader validate {basename}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    # STUDENT_FILE = Path(f'{coursefolder}/{student_notebook}'
    #SOURCE_ASSIGNMENT = Path(f'{ASSIGNMENT_FOLDER}/{ASSIGNMENT[:ind]}_STUDENT{ASSIGNMENT[ext:]}')
    #NEW_ASSIGNMENT = basename + ASSIGNMENT[ext:]
    RELEASE_ASSIGNMENT = Path(str(RELEASE_FOLDER)+"/"+studentfile)

    # Make a link for review
    display(
        HTML(f"<a href={RELEASE_ASSIGNMENT} target=\"blank\">{RELEASE_ASSIGNMENT}</a>"))


def unpackD2L(filename, this_notebook, coursefolder='./', destination='upziptemp'):
    warnings.warn(
        "usenbgrader will be deprecated in the future.",
        DeprecationWarning
    )
    
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
        [first, last] = name[1].split(' ')
        directory = name[1].replace(' ', '_')

        command = f"cd {coursefolder}; nbgrader db student add {directory} --last-name=${last} --first-name=${first}"
        print(command)
        returned_output = subprocess.check_output(command, shell=True)

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
