import os
import glob

"""Depreciated files"""
    
def renamefile(oldname, newname, MAKE_CHANGES=False):
    """Rename a file from oldname to newname. Search the current folder for any
    links in notebooks with the old filename and update them."""
    files = glob.glob('*.ipynb')
    if not oldname in files:
        print(f"ERROR: File {oldname} not found in directory")
        return
    oldstudentversion = f"{oldname[:-17]}"
    newstudentversion = f"{newname[:-17]}"
    cmd = f"git mv {oldname} {newname} "
    if MAKE_CHANGES:
        os.system(cmd)
    else:
        print(f"TEST: {cmd}")
    for file in glob.glob('*.ipynb'):
        if "INSTRUCTOR" in file:
            with open(file, encoding="utf-8") as f:
                s = f.read()
            if oldstudentversion in s:
                s = s.replace(oldstudentversion, newstudentversion)
                if MAKE_CHANGES:
                    print("writing changed file")
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(s)
                else:
                    print(f"TEST: Student File Reference in {file}")


def notebook(filename, datestr, MAKE_CHANGES=False):
    """Migrate a notebook from the filename to the new four digit date string"""
    files = glob.glob('*.ipynb')
    if not filename in files:
        print(f"ERROR: File {filename} not found in directory")
        return
    oldname = filename
    newname = f"{datestr}{oldname[4:]}"
    renamefile(oldname, newname, MAKE_CHANGES)
