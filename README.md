# JupyterInstruct
Written by [Dirk Colbry](http://colbrydi.github.io/)

<img alt="JupyterInstruct logo with a cartoon Jupyter writing on a green chalkboard. Image created by Tamara Colbry" src="https://raw.githubusercontent.com/colbrydi/jupyterinstruct/master/docs/images/JupyterInstruct_icon.png" style="float:right" width=300px> 

The JupyterInstruct Python package is designed for INSTRUCTORS to organize and adjust course curriculum. Each assignment is given it's own jupyter notebook and all student reading, videos, images are included in the notebook.  Each notebook also contains notes for instructors that will be automatically removed. The main design goals for this project include: 

- Tools to help instructors maintain course materials all in one place including instructor notes and answers. 
- Tools to help migrate curriculum form one semester to the next.
- Tools to automatically generate websites and ebooks from notebooks. 
- Notebook validation tools to identify common problems with links, images and accessibility.
- Tools to interface nbgrader with the MSU jupyterhub servers and MSU Desire2Learn course management systems. 

## Installation

This package is currently under development and is not avaliable via pipy.  to install use the following command:

```pip install git+https://github.com/colbrydi/jupyterinstruct```

To install as a user on Jupyterhub try the following instead:

```pip install -user git+https://github.com/colbrydi/jupyterinstruct```

## Command line tools

Many of the core jupyterinstruct tools have a command line interface option.  These include:

- ```jupyterinstruct``` - list of all of the command line tools.
- ```validatenb NOTEBOOKNAME``` - Validate a notebook for errors.
- ```publishnb -o OUTPUTFOLDER NOTEBOOKNAME``` - Publish notebook to a website.
- ```renamenb OLDFILENAME NEWFILENAME``` - Rename a notebook
- ```makestudentnb -o OUTPUTFOLDER NOTEBOOKNAME``` - Make a student version of the notebook

**_NOTE_**: The MSU jupyterhub server terminal currently defaults to tcsh. To best utilize these tools type 'bash' at the command prompt when starting a terminal. 

```
> bash
> jupyterinstruct
```


## Package UML dependancies

<img alt="Package UML dependances" src="https://raw.githubusercontent.com/colbrydi/jupyterinstruct/master/docs/images/packages.png">


## Usage

Please check out the [Example.ipynb](https://colbrydi.github.io/jupyterinstruct/Examples) for some instructions on how to use Jupyterinstruct. 

[Click here for package documentation](https://colbrydi.github.io/jupyterinstruct/jupyterinstruct/index.html)

## Accessable Jupyter Condtent

Also included in this git repository is a notebook demonstrating best practices for generating Accessable content in Jupyter notebooks.

- [Accessable Jupyter Content](Accessable_Jupyter_content_for_INSTRUCTORS)


