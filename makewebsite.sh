pdoc3 --force --html --output-dir ./docs jupyterinstruct
python makeindex.py ./README.md > docs/index.html
jupyter nbconvert --log-level=0 --no-input --no-prompt --allow-errors --to html Assessable_Jupyter_content_for_INSTRUCTORS.ipynb --output ./docs/Assessable_Jupyter_content.html
 
 
