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
        'nbconvert',
        'beautifulsoup4',
        'pytest',
    ],
    packages=[
        'jupyterinstruct',
    ],
)
