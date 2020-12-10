<img alt="JupyterInstruct logo with a cartoon Jupyter writing on a green chalkboard. Image created by Tamara Colbry" src="https://raw.githubusercontent.com/colbrydi/jupyterinstruct/main/docs/images/JupyterInstruct_icon.png" style="float:right"> 
# JupyterInstruct

The JupyterInstruct module is designed for INSTRUCTORS to organize and adjust course curriculum. Each assignment is given it's own jupyter notebook and all student reading, videos, images are included in the notebook.  Each notebook also contains notes for instructors that will be automatically removed. 

* Student curriculum - This is the main content of the notebooks.  The intention is for these notebooks to contain all resources students need for the course.
* Instructor Notes and Answers - Each notebook also contains instructor notes and answers using the ###ANSWER### tag.  any cell that contains the ###ANSWER### tag will be removed when automatically generating the student version of the notebook.
* Information tags - Each course can include a ```thiscourse.py``` file which populates a dictionary of "tags". The tag key is a tag string (typically uppercase) such as ```GITURL``` and the tag value is a string. When generating the student version of a notebook the code will search for tag serounded by ```###``` escape charicters (ex. ```###GITURL###``` and replace each instance with the string. ```.
