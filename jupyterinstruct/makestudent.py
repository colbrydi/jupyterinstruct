import IPython.core.display as IP

def getname():
    IP.display(IP.Javascript('Jupyter.notebook.kernel.execute("this_notebook = " + "\'"+Jupyter.notebook.notebook_name+"\'");'))

def convert(this_notebook, studentfolder='./'):
    import os
    from IPython.core.display import Javascript, HTML
    from IPython.display import display

    print("Save Current Notebook")
    IP.display(IP.Javascript("Python.notebook.save_notebook()"),include=['application/javascript'])

    #Calculate Destination name
    ASSIGNMENT =  this_notebook
    ind = ASSIGNMENT.index("INST")
    ext = ASSIGNMENT.index(".ipynb")
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

    print("Removing existing student version")
    command = f"rm {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    print("Stripping out ANSWER feilds")
    command = f"python ./instruct/makeStudentVersion.py {this_notebook}"
    os.system(command)

    #Move to the working directory
    print("Moving to working directory")
    command = f"mv {NEW_ASSIGNMENT} {studentfolder}"
    os.system(command)

    #Strip output
    print("Striping output cells")
    command = f"python ./instruct/nbstripout {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    # Make a link for review
    display(HTML(f"<a href={studentfolder}{NEW_ASSIGNMENT} target=\"_blank\">{NEW_ASSIGNMENT}</a>"))


def merge(this_notebook, studentfolder='./', tags={}):
    import os
    from IPython.core.display import Javascript, HTML
    from IPython.display import display
    import csv    
    import datetime
    import calendar

    IP.display(IP.Javascript("IPython.notebook.save_notebook()"),include=['application/javascript'])
    
    #Calculate Destination name
    ASSIGNMENT =  this_notebook
    ind = ASSIGNMENT.index("INST")-1
    ext = ASSIGNMENT.index(".ipynb")
    #NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]
    NEW_ASSIGNMENT = ASSIGNMENT[:ind] + ASSIGNMENT[ext:]

    try:
        month=int(NEW_ASSIGNMENT[0:2])
        day=int(NEW_ASSIGNMENT[2:4])
        
        print(f"TESTING {day} {month} {tags['YEAR']}")
        my_date = datetime.datetime(int(tags['YEAR']), month, day)
        #my_date = date.today()
        weekday=calendar.day_name[my_date.weekday()];
        
        mnth=calendar.month_name[month]
        tags['DUE_DATE']=f'{weekday} {mnth} {day}' 
        tags['MMDD']=NEW_ASSIGNMENT[0:4]
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
    lines=[]
    for row in new_lines:
        for key in tags:
            if (key in row):
                row = row.replace(f"###{key}###",tags[key])
                print(row)
        lines.append(row)    
            
    with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as f:
        for l in lines:
            f.write(l)

    for line in lines:
        if "ANSWER" in line:
            print("WARNING! Some answer content may remain in the file. Please double check file contents before administering to students.")
            break

    #Move to the working directory
    print("Moving to working directory")
    command = f"mv {NEW_ASSIGNMENT} {studentfolder}"
    os.system(command)

    #Strip output
    print("Striping output cells")
    command = f"python ./instruct/nbstripout {studentfolder}{NEW_ASSIGNMENT}"
    os.system(command)

    # Make a link for review
    display(HTML(f"<a href={studentfolder}{NEW_ASSIGNMENT} target=\"blank\">{NEW_ASSIGNMENT}</a>"))
