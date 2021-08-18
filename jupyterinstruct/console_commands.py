"""
Command line tools for workign with jupyter notebooks.

- jupyterinstruct - list of all of the command line tools.
- validatenb NOTEBOOKNAME - Validate a notebook for errors.
- publishnb -o OUTPUTFOLDER NOTEBOOKNAME - Publish notebook to a website.
- renamenb OLDFILENAME NEWFILENAME - Rename a notebook
- makestudentnb -o OUTPUTFOLDER NOTEBOOKNAME - Make a student version of the notebook
- makenbindex NOTEBOOKNAME - Make a markdown index from a notebook
         
"""
import argparse
import sys

def makenbindex():
    """ Make a markdown index from the jupyter notebook 
    print to screen."""
    from jupyterinstruct.InstructorNotebook import renamefile

    parser = argparse.ArgumentParser(description='rename notebook')

    parser.add_argument('input', help=' input filenames')

    args = parser.parse_args()

    print('\n\n')
    print(args)
    print('\n\n')
    from jupyterinstruct import InstructorNotebook as inb
    notebook = inb.InstructorNB(args.input)
    notebook.makeTOC()

def renamenb():
    """Rename Instructor notebook using git and fix all 
    student links in files."""
    from jupyterinstruct.InstructorNotebook import renamefile
 
    parser = argparse.ArgumentParser(description='rename notebook')

    parser.add_argument('input', help=' input filenames')
    parser.add_argument('output', help=' output filename', nargs='*')

    args = parser.parse_args()
    
    print('\n\n')
    print(args)
    print('\n\n')
    
    renamefile(args.input, args.output)
    
def makestudentnb():
    """Make a student version of an instructor notebook. """
    from jupyterinstruct.InstructorNotebook import makestudent
    
    parser = argparse.ArgumentParser(description='Make a student version.')

    parser.add_argument('-outputfolder', '-w', metavar='outputfolder', 
                        default='./',
                        help=' Name of the destination Folder')
    parser.add_argument('files', help=' inputfilenames', nargs='+')
#     parser.add_argument('-coursefile', '-c', metavar='coursefile',
#                         default='thiscourse.py',
#                         help=' Course file which creates tags')
    
    try:
        import thiscourse.py
        tags = thiscourse.tags
    except:
        print('thiscourse not found')
        tags = {}

    args = parser.parse_args()

    for filename in args.files:
        makestudent(filename, studentfolder=args.outputfolder, tags=tags)
        
def publishnb():
    """ Publish jupyter notebook as html file.
    """
    from jupyterinstruct.webtools import publish
    
    parser = argparse.ArgumentParser(description='Publish notebook to folder.')

    parser.add_argument('-webfolder', '-w', metavar='webfolder', 
                        default='./',
                        help=' Name of the destination Folder')
    parser.add_argument('files', help=' inputfilenames', nargs='+')

    args = parser.parse_args()

    for filename in args.files:
        publish(filename,outfolder=args.webfolder)
        
def validatenb():
    """Run Validator on jupyter notebook."""
    from jupyterinstruct.nbvalidate import validate
    
    parser = argparse.ArgumentParser(description='validate notebook file')

    parser.add_argument('files', help=' inputfilenames', nargs='+')

    args = parser.parse_args()

    for filename in args.files:
        validate(filename)

def listcommands():
    print(__doc__)
        
if __name__ == "__main__":
    listcommands()
    makestudentnb()
