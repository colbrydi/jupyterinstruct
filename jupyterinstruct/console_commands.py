import argparse
import sys




def renamenb():
    from jupyterinstruct.InstructorNotebook import renamefile
 
    parser = argparse.ArgumentParser(description='rename notebook')

    parser.add_argument('input', help=' input filenames')
    parser.add_argument('output', help=' output filename')

    args = parser.parse_args()
    
    print('\n\n')
    print(args)
    print('\n\n')
    
    renamefile(args.input, args.output)

def publishnb():
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
    from jupyterinstruct.nbvalidate import validate
    
    parser = argparse.ArgumentParser(description='validate notebook file')

    parser.add_argument('files', help=' inputfilenames', nargs='+')

    args = parser.parse_args()

    for filename in args.files:
        validate(filename)
    
if __name__ == "__main__":
    validatenb()