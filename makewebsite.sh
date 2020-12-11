pdoc3 --force --html --output-dir ./docs jupyterinstruct
python makeindex.py ./README.md > docs/index.html
jupyter nbconvert --log-level=0 --no-prompt --to html Accessable_Jupyter_content_for_INSTRUCTORS.ipynb --output ./docs/Accessable_Jupyter_content.html
 
 
