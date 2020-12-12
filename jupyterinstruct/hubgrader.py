"""Interface between InstructorNotebooks and a non standard nbgrader installation.  These tools help put the files in the right place so that instructors can use the nbgrader installation on jupyterhub.erg.mus.edu.
"""

from jupyterinstruct.nbfilename import nbfilename
from pathlib import Path
from IPython.core.display import Javascript, HTML
import subprocess
import shutil
import time
import pathlib



class gradernames():
    """Create a class of names that follow the nbgrader naming convention:
    
    The typical nbgrader folder sturcture is as follows:

       grading_folder
       |
       |--source_folder
         |
         |--core_assignment_name
           |
           |--Student_file.ipynb 
       |--release_folder
         |
         |--core_assignment_name
           |
           |--Student_file.ipynb 
       |--submittedfolder
         |
         |--Student_Name
           |
           |--core_assignment_name
             |
             |--Student_file.ipynb 
       |--autograded_folder
         |
         |--Student_Name
           |
           |--core_assignment_name
             |
             |--Student_file.ipynb  
       |--feedback_folder
         |
         |--Student_Name
           |
           |--core_assignment_name
             |
             |--Student_file.html
    """
    
    def __init__(self, filename, grading_folder='./AutoGrader'):
        
        nbfile = nbfilename(filename)
        if nbfile.isInstructor:
            raise Exception("Instructor file error: Input student version filename not the instructor version.") 
        
        corefile = Path(filename)

        if not corefile.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), this_notebook)

        self.core_assignment_name = corefile.stem 
        
        self.grading_folder = Path(grading_folder)
 
        self.source_folder = Path(self.grading_folder, 'source', self.core_assignment_name)
        self.source_file = Path(self.source_folder, f'{self.core_assignment_name}-STUDENT.ipynb')
                                
        self.release_folder = Path(self.grading_folder, 'release', self.core_assignment_name)
        self.release_file = Path(self.release_folder, f'{self.core_assignment_name}-STUDENT.ipynb')
                                
        #Give OS time to make folders (Helps bugs on some systems)
        time.sleep(2)
    

def importnb(this_notebook):
    """ Import a student ipynb file into the current instructorsnbgrading system. 
    The file should be marked as an assignment by nbgrader."""
    
    print(f"IMPORTING {this_notebook}")
    
    if not Path(this_notebook).exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), this_notebook)

    gname = gradernames(this_notebook)
    
    #Make folder paths
    gname.grading_folder.mkdir(parents=True, exist_ok=True)
    gname.source_folder.mkdir(parents=True, exist_ok=True)
    gname.release_folder.mkdir(parents=True, exist_ok=True)

    shutil.move(this_notebook, gname.source_file)

    command = f'cd {gname.grading_folder}; nbgrader db assignment add {gname.core_assignment_name}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    command = f'cd {gname.grading_folder}; nbgrader generate_assignment --force {gname.core_assignment_name}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    command = f'cd {gname.grading_folder}; nbgrader validate {gname.core_assignment_name}'
    print(command)
    returned_output = subprocess.check_output(command, shell=True)
    print(f"Output: {returned_output.decode('utf-8')}")

    # Make a link for review
    display(
        HTML(f"<a href={gname.release_file} target=\"blank\">{gname.release_file}</a>"))
    return gname.release_file


def unpackD2L(filename, this_notebook, coursefolder='./', destination='upziptemp'):
    print("unpackD2L will be deprecated in the future and moved to a different package (See documentation for updates)")
    warnings.warn(
        "unpackD2L will be deprecated in the future and moved to a different package (See documentation for updates)",
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
