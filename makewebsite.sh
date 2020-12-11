# Simple script to create website from the current folder

MODULENAME=jupyterinstruct

# Generate automatic documentation
pdoc3 --force --html --output-dir ./docs $MODULENAME 

# Convert project README.md as the website index.html page
python makeindex.py ./README.md > docs/index.html

# Convert Jupyter Notebooks

for notebook in *.ipynb;
do
	echo $notebook
	jupyter nbconvert --log-level=0 --no-prompt --to html $notebook 
done
mv *.html ./docs/
 
#Make UML Diagram
pyreverse -ASmy -o png $MODULENAME
mv *.png ./docs/images
 
