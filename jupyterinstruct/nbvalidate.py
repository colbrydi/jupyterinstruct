''' Jupyter notebook validator.  These functions check for common errors in student notebooks including:

- Extra Tags of the from ###TAG### (used by jupyterinstruct)
- Link to URL errors
- Link to file errors
- Empty Links
- Missing anchor links (#) in notebook
- Valid iframe links (for youtube videos)
- Image Link error
- Image alt text empty
- Image missing alt text

Usage
=====

from jupyterinstruct.nbvalidate import validate
validate(filename="Accessable_Jupyter_content_for_INSTRUCTORS.ipynb")
'''

import re
import os
import requests
import nbformat
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
from pathlib import Path
from nbconvert.preprocessors import ExecutePreprocessor
from sys import platform


def checkurl(url):
    '''Check if url is a valid link. timeout 5 seconds'''
    try:
        request = requests.get(url, timeout=5)
    except Exception as e:
        return 1

    output = 0
    if not request.status_code < 400:
        output = 1
    return output

def truncate_string(data, depth=75):
    info = (data[:depth] + '..') if len(data) > depth else data
    return info

def validate(filename):
    '''Function to validate links and content of a IPYNB'''
    print(f"Validating Notebook {filename}")

    errorcount = 0

    parts = Path(filename)
    foldername = parts.parent

    # Read in the file
    with open(filename, 'r',encoding = 'utf8') as file:
        jsontext = file.read()


    # TODO: check for ###NAME### triple hash
    extra_tags = set(re.findall('#\w+#', jsontext))
    for tag in extra_tags:
        print(f"   - ERROR: Extra Tag {tag}")
        errorcount += 1

    wrong_emphasis = set(re.findall(r'\<[^\>\/]*\>\*\*', jsontext))
    for emphasis in wrong_emphasis:
        print(f"   - ERROR: Wrong emphasis- {emphasis} ** should be first")
        errorcount += 1

    nb = nbformat.reads(jsontext, as_version=4)  # ipynb version 4

    # may be needed for video verification
    try:
        ep = ExecutePreprocessor(timeout=10,
                                 kernel_name='python3',
                                 allow_errors=True)
        ep.preprocess(nb)
    except Exception as e:
        print(truncate_string(f"   WARNING: Notebook preprocess Timeout (check for long running code)\n {e}"))
        errorcount += 1

    # Process the notebook we loaded earlier
    (body, resources) = HTMLExporter().from_notebook_node(nb)

    # print(body)
    soup = BeautifulSoup(body, 'html.parser')

    #Make a dictionary of in-file anchors for checking later.
    anchorlist = dict()
    links = soup.find_all('a', href=False)
    for link in links:
        if link.has_attr('name'):
            anchorlist[link['name']] = False
        else:
            print(truncate_string(f"   ERROR: Missing 'name' attribute in link {link}"))
            errorcount += 1


    # check all hyperlinks
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        try:
            if len(href) > 0:
                if href[0] == "#":
                    anchorlist[href[1:]] = True
                else:
                    if href[0:4] == "http":
                        error = checkurl(href)
                        if error:
                            print(f'   ERROR: Link not found - {href}')
                            errorcount += error
                    else:
                        if not os.path.isfile(f'{foldername}/{href}'):
                            print(f'   ERROR: File Doesn\'t Exist - {href}')
                            errorcount += 1
            else:
                print(f"   Empty Link - {link}")
                errorcount += 1
        except Exception as e:
            print(truncate_string(f"   WARNING: Timeout checking for link {link}\n {e}"))
            errorcount += 1

    #Verify hyperlinks to infile anchors
    for anchor in anchorlist:
        if not anchorlist[anchor]:
            print(f"   ERROR: Missing anchor for {anchor}")
            errorcount += 1

    # Verify video links
    iframes = soup.find_all('iframe')
    for frame in iframes:
        error = checkurl(frame['src'])
        if error:
            print(f'   ERROR: Iframe LINK not found - {href}')
            errorcount += error

    # Verify img links and alt text
    images = soup.find_all('img')
    for img in images:
        image = img['src']
        if not image[0:4] == 'data':
            error = checkurl(img['src'])
            if error:
                print(f'   ERROR: Image LINK not found - {href}')
                errorcount += error

        # Check the image alt text is present and valid.
        if img.has_attr('alt'):
            if img['alt'] == "":
                print(truncate_string(f'   ERROR: Empty Alt text in image - {href}'))
                errorcount += 1
        else:
            print(truncate_string(f'   ERROR: No Alt text in image - {img["src"]}'))
            errorcount += 1

    return errorcount



if __name__ == "__main__":
    import sys
    errors = 0
    for filename in sys.argv[1:]:
        errors += validate(filename)
