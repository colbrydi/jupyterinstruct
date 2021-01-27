"""Interface between InstructorNotebooks and a non standard nbgrader installation.  These tools help put the files in the right place so that instructors can use the nbgrader installation on jupyterhub.erg.mus.edu.

Usage
-----

from jupyterinstruct import hubgrader 
output = hubgrader.importnb(studentfile)

"""


from jupyterinstruct.nbfilename import nbfilename
from pathlib import Path
from IPython.core.display import Javascript, HTML
import subprocess
import shutil
import time
import pathlib
from pathlib import Path

def makestudents(filename="students.csv"):
    """Generate student accounts in nbgrader from a CSV file exported from D2L"""
    import pandas as pd
    import subprocess

    namefile = pd.read_csv(filename)
    for index, row in namefile.iterrows():
        first = row['First Name']
        last = row['Last Name']
        email = f"{row['Email']}@msu.edu"
        name = f"{first}_{last}"
        command = f"nbgrader db student add {name} --last-name={last} --first-name={first} --email={email}"
        print(command)
        returned_output = subprocess.check_output(command, shell=True)

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
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 
                                    _notebook)

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

def quick_review_D2L(zipfile="nbTester_data.zip", folder='unziptemp'):
    from jupyterinstruct import webtools
    
    destination_folder=Path(folder)

    unpackD2L(zipfile, destination=str(destination_folder))

    files = destination_folder.glob('*.ipynb')
    markdown = ""
    for file in files:
        htmlfile = webtools.publish(str(file), outfolder=str(destination_folder), execute=True, removeerrors=False)
        markdown += f"- [{htmlfile}]({htmlfile})\n"
    return markdown

def D2L_2_nbgrader(zipfile, assignment, destination='AutoGrader/submitted', tempfolder='upziptemp'):
    unpackD2L(zipfile, destination=tempfolder)
    expandfiles(assignment, source=tempfolder, destination=destination)
          
def expandfiles(assignment, source='upziptemp', destination='AutoGrader/submitted'):
    nbfile = nbfilename(assignment)
    nbfile.isInstructor = False
    nbfile.isStudent = False
    sourcefolder = Path(source)
    ipynbfiles = sourcefolder.glob('*.ipynb')
    for thisfile in ipynbfiles:
        print(thisfile.stem)
        myfolder = Path(destination / Path(thisfile.stem) / Path(nbfile.basename()))
        myfolder.mkdir(parents=True, exist_ok=True)
        nbfile.isStudent = True
        thisfile.rename(myfolder / Path(assignment + nbfile.basename()) )
    

def unpackD2L(filename, destination='upziptemp'):
    import warnings
#     print("unpackD2L will be deprecated in the future and moved to a different package (See documentation for updates)")
#     warnings.warn(
#         "unpackD2L will be deprecated in the future and moved to a different package (See documentation for updates)",
#         DeprecationWarning
#     )
 
    #from urllib.request import urlretrieve
    import zipfile

    zfile = Path(filename)
    destination_folder = Path(destination)

    print(f"Unzipping {filename}")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(str(destination_folder))

    files = destination_folder.glob('*.ipynb')

    for f in files:
        name = str(f).split(' - ')
        [first, last] = name[1].split(' ')
        newfile = Path(name[1].replace(' ', '_')+'.ipynb')
        #print(destination_folder / newfile)
        f.rename(Path(destination / newfile))

          
def sendfeedback(assignment_name, 
                 subject='MTH314 Assignment Feedback', 
                 graded_message=None,
                 empty_feedback=None,
                 cc='',
                 bcc='',
                 feedback_folder = f"./AutoGrader/feedback/",
                 EMAILtest=True):
    
    import getpass
    import smtplib
    import subprocess
    import smtplib
    from email.mime.text import MIMEText
    from pathlib import Path
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from os.path import basename

          
    if(EMAILtest):
        print("TESTING Only, Emails will NOT be sent")
    else:
        for i in range(0,3):
            print("WARNING, DANGER!!!!, Emails are being Sent")
          
    #Get the current username for the "from" email
    usr=getpass.getuser()
    fromAddress=usr+"@msu.edu"
    print(f"My email is {fromAddress}\n\n")
                 
    #Pull in student names and emails from the nbgrader database
    command = "nbgrader db student list > temp.names"
    returned_output = subprocess.check_output(command, shell=True)
    s = smtplib.SMTP('smtp.egr.msu.edu')
    getdb = open("temp.names", 'r')
    lines = getdb.readlines()
    
    emails = []
    tags =dict()
    tags['assignment_name']=assignment_name
    for line in lines:
        part = line.split(' ')
        if not part[0] == 'There':
            folder = part[0]
            tags['last'] = part[1][1:-1]
            tags['first'] = part[2][:-1]

            toAddress = part[4][:-1]
            pth = Path(f"{feedback_folder}{folder}/{assignment_name}/")
            files = list(pth.glob('*.html'))

            if files:
                message=graded_message
            else:
                message=empty_feedback
            
            if not message == None:
                print(f"Emailing {tags['last']} {tags['first']}")

                newmessage=message

                for j,tag in enumerate(tags):
                    newmessage = newmessage.replace(f"<<<{tag}>>>", tags[tag])

                msg = MIMEMultipart()
                msg.attach(MIMEText(newmessage))
                msg['Subject'] = subject
                msg['From'] = fromAddress
                msg['To'] = toAddress

                #Attach feedback
                if files:
                    feedback_file = files[0]        
                    print(f"Attaching file {feedback_file}")
                    with open(feedback_file, "rb") as attachment_file:
                        part = MIMEApplication(attachment_file.read(),Name=basename(feedback_file))
                    # After the file is closed
                    part['Content-Disposition'] = f'attachment; filename="{basename(feedback_file)}"'
                    msg.attach(part)
                else:
                    feedback_file="NONE"

                rcpt = toAddress.split(",")
                if cc:
                    rcpt = cc.split(",") + rcpt
                    msg['Cc'] = cc
                if bcc:
                    rcpt = bcc.split(",") + rcpt
                    msg['Bcc'] = bcc

                #TODO Add code to verify all << have been found
                #print(rcpt)
                if EMAILtest:
                    print('To:',toAddress)
                    print('From:',fromAddress)
                    if cc:
                        print('CC:',cc)
                    if bcc:
                        print('BCC:', bcc)
                    print('Subject:', subject)
                    print('Attachment:', feedback_file)
                    print(newmessage)
                else:
                    try:
                        # Send the message via engineering SMTP server.
                        print('Connecting to SMTP and sending message to', toAddress)
                        s.sendmail(fromAddress, rcpt, msg.as_string())
                    except SMTPException:
                        print("Error: unable to send email to", toAddress)
                print("\n\n")
    s.quit()
