try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupyterinstruct",
    version="0.0.1dev",
    author="Dirk Colbry",
    author_email="colbrydi@msu.edu",
    description="Instructor tools used with Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        'jupyter',
        'IPython',
        'nbformat',
        'nbgrader',
        'nbconvert',
        'beautifulsoup4',
    ],
    entry_points = {
        'console_scripts': [
            'jupyterinstruct=jupyterinstruct.console_commands:listcommands',
            'validatenb=jupyterinstruct.console_commands:validatenb',
            'publishnb=jupyterinstruct.console_commands:publish',
            'renamenb=jupyterinstruct.console_commands:rename',
            'makestudentnb=jupyterinstruct.console_commands:makestudent',
         ],
    },
    packages=[
        'jupyterinstruct',
    ],
)
