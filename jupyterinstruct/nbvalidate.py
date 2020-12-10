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
'''

import re
import os
import requests
import nbformat
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
from pathlib import Path
from nbconvert.preprocessors import ExecutePreprocessor


def checkurl(url):
    '''Check if url is a valid link. timeout 5 seconds'''
    request = requests.get(url, timeout=5)
    output = 0
    if not request.status_code < 400:

        output = 1
    return output


def validate(filename):
    '''Function to validate links and content of a IPYNB'''
    print(f"Validating Notebook {filename}")

    parts = Path(filename)
    foldername = parts.parent

    # Read in the file
    with open(filename, 'r') as file:
        text = file.read()

    # TODO: check for ###NAME### triple hash
    extra_tags = set(re.findall('#\w+#', text))
    for tag in extra_tags:
        print(f"   - Extra Tag {tag}")

    nb = nbformat.reads(text, as_version=4)  # ipynb version 4

    # may be needed for video verification
    ep = ExecutePreprocessor(
        timeout=600, kernel_name='python3', allow_errors=True)
    ep.preprocess(nb)

    # Process the notebook we loaded earlier
    (body, resources) = HTMLExporter().from_notebook_node(nb)

    # print(body)
    soup = BeautifulSoup(body, 'html.parser')
    anchorlist = dict()
    links = soup.find_all('a', href=False)
    for link in links:
        anchorlist[link['name']] = False

    errorcount = 0

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
                            print(f'   LINK ERROR - {href}')
                            errorcount += error
                    else:
                        if not os.path.isfile(f'{foldername}/{href}'):
                            print(f'   File Doesn\'t Exist - {href}')
                            errorcount += 1
            else:
                print(f"   Empty Link - {link}")
                errorcount += 1
        except Exception as e:
            print(f"   Timeout Warning for  {link}\n {e}")
            errorcount += 1

    for anchor in anchorlist:
        if not anchorlist[anchor]:
            print(f"   Missing anchor for {anchor}")
            errorcount += 1

    # Verify video links
    iframes = soup.find_all('iframe')
    for frame in iframes:
        error = checkurl(frame['src'])
        if error:
            print(f'   Iframe LINK ERROR - {href}')
            errorcount += error

    # Verify img links
    images = soup.find_all('img')
    for img in images:
        image = img['src']
        if not image[0:4] == 'data':
            error = checkurl(img['src'])
            if error:
                print(f'   Image LINK ERROR - {href}')
                errorcount += error

        # Check the image alt text is present and valid.
        if img.has_attr('alt'):
            if img['alt'] == "":
                print(f'   Empty Alt text in image - {href}')
                errorcount += error
        else:
            print(f'   No Alt text in image - {img["src"]}')
            errorcount += error

    return errorcount


if __name__ == "__main__":
    errors = 0
    for filename in argv[1:]:
        errors += validate(filename)
