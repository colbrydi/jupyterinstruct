'''
Written by Nathaniel Hawkins
Tuesday, October 2nd, 2018
Updated: 24 October, 2018

This file will parse a Jupyter Notebook and look for code cells
that contain an ANSWER tag, indicating a solution to a question
in an instructor's Jupyter Notebook. Once found, those cells are deleted,
making a version for students to use that does not contain solutions.

This code checks markdown and code cells for answer tags
and now parses meta-data to find appropriate locations for
editing. It will scan the notebook for any other location where
ANSWER comes up to ensure answers are removed.

NOTE: ANY CELL THAT HAS A FIRST LINE WHICH CONTAINS "ANSWER" (in all caps) WILL BE DELETED.


Example:

To make a student version, simply run:

`python makeStudentVersion.py FULL_FILENAME_WITH_PATH.ipynb`

** The script will look for the word "INSTRUCTOR" (in all caps)
in the filename in order to generate a newly made "STUDENT"
version. The full filename will need to include that in order
for the script to run.

For example:

`python makeStudentVersion.py Day_NN_assignment_INSTRUCTOR.ipynb`

would make the file `Day_NN_assignment_STUDENT.ipynb` with all
code cells containing ##ANSWER## as the first line removed. If any
other cells contain "ANSWER", it will print a warning message.


Make sure that before running this script you restart and
clear output. If the notebook output isn't cleared, then the script
won't be able to parse the cells properly and remove the ##ANSWER##
cells.
'''

import numpy as np
import sys

ASSIGNMENT = sys.argv[1]
ind = ASSIGNMENT.index("INST")
ext = ASSIGNMENT.index(".ipynb")
NEW_ASSIGNMENT = ASSIGNMENT[:ind] + "STUDENT" + ASSIGNMENT[ext:]

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

with open(NEW_ASSIGNMENT, 'w+', encoding="utf-8") as f:
    for l in new_lines:
        f.write(l)

for line in new_lines:
	if "ANSWER" in line:
		print("WARNING! Some answer content may remain in the file. Please double check file contents before administering to students.")
		break
