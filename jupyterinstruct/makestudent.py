from jupyterinstruct import InstructorNotebook as inb

"""makestudent is depreciated"""


def merge(this_notebook, studentfolder='./', tags={}):
    inb.makestudent(this_notebook, studentfolder=studentfolder, tags=tags)

def getname():
    inb.getname()
