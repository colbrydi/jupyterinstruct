"""makestudent is a Depreciated library - only maintained for reverse compatibility.
   Use InstructorNotebook instead.
"""
from jupyterinstruct import InstructorNotebook as inb
import warnings

def merge(this_notebook, studentfolder='./', tags={}):
    print("merge is deprecated, use InstructorNotebook.makestudent() instead")
    warnings.warn(
        "merge is deprecated, use InstructorNotebook.makestudent() instead",
        DeprecationWarning
    )
    inb.makestudent(this_notebook, studentfolder=studentfolder, tags=tags)


def getname():
    print("getname is deprecated, use InstructorNotebook.getname() instead")
    warnings.warn(
        "getname is deprecated, use InstructorNotebook.getname() instead",
        DeprecationWarning
    )
    inb.getname()

