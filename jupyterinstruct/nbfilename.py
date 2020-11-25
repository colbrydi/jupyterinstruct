import IPython.core.display as IP
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import datetime
import calendar
import re


class nbfilename():
    """Class to work with instructor filenames of the following format:
    MMDD--TITLE_STRING_[pre,in]-class-assignment-INSTRUCTOR.ipynb
    """

    def __init__(self, filename=""):
        """Input a filename and parse using above syntax"""
        self.prefix = ""
        self.namestring = ""
        self.attributes = set()
        self.extention = 'ipynb'
        self.isInstructor = False
        self.isStudent = False
        self.isInClass = False
        self.isPreClass = False
        self.isAssignment = False
        self.isDate = False
        self.date = ""
        self.title = None
        self.input_name = filename
        self.parsestr(filename)

    def parsestr(self, filename=None):
        """Parse the filestring and populate the nbfilename object"""
        if not filename:
            filename = self.input_name
        else:
            self.namestring = filename

        attribute_list = ['INSTRUCTOR', 'STUDENT', 'in-class', 'pre-class']
        self.parts = re.split('-|_| |\.', filename)

        if '' in self.parts:
            self.parts.remove('')

        self.prefix = self.parts[0]
        self.parts.remove(self.prefix)

        if len(self.prefix) == 4 and self.prefix.isdigit():
            if not self.prefix == '0000':
                self.isDate = True

        if self.isDate:
            self.setDate()

        self.extention = self.parts[-1]
        if self.parts[-1] == 'ipynb':
            self.parts.remove('ipynb')
        else:
            if '.' in filename:
                self.extention = parts[-1]
                parts.remove[parts[-1]]
        if len(self.parts) > 0:
            if self.parts[-1] == 'INSTRUCTOR':
                self.isInstructor = True
                del self.parts[-1]

        if len(self.parts) > 3:
            if self.parts[-1] == 'assignment' or self.parts[-1] == 'class':
                if self.parts[-1] == 'assignment':
                    self.isAssignment = True
                    del self.parts[-1]

                if self.parts[-1] == 'class':
                    del self.parts[-1]
                    if self.parts[-1] == 'in':
                        self.isInClass = True
                        del self.parts[-1]
                    else:
                        if self.parts[-1] == 'pre':
                            self.isPreClass = True
                            del self.parts[-1]
        self.title = "_".join(self.parts)


        
    def basename(self):
        """Regenerate the filename string from the parsed data"""

        string = self.getPrefix()

        if self.title:
            string = string+"-"

        if self.isPreClass:
            string = string+"-"

        string = string + self.title

        if self.isInClass:
            string = string+'_in-class-assignment'
        if self.isPreClass:
            string = string+'_pre-class-assignment'
        return string

    def makestring(self):
        string = self.basename()
        
        if self.isInstructor:
            string = string + '-INSTRUCTOR'
            
        string = string + "." + self.extention
        return string        
        
    def daydifference(self, day, month, year):
        """Compare two dates and calcualte the number of days difference"""
        old_date = datetime.datetime(self.year, self.month, self.day)
        new_date = datetime.datetime(year, month, day)
        datediff = new_date - old_date
        return datediff.days

    def adjustdays(self, days=0):
        """Ajust the date strig based on number of days. Don't forget to add years"""
        old_date = datetime.datetime(self.year, self.month, self.day)
        datediff = datetime.timedelta(days=days)
        new_date = old_date+datediff
        self.day = new_date.day
        self.month = new_date.month
        self.year = new_date.year

    def setDate(self, datestr=None, YEAR=2021):
        """Set the date based on the prefix or a new datestring"""
        if not datestr:
            datestr = self.prefix

        if len(datestr) != 4:
            self.isDate = False

        if not datestr.isdigit():
            self.isDate = False

        if self.isDate:
            self.month = int(datestr[0:2])
            self.day = int(datestr[2:4])
            self.year = YEAR

        if not datestr == self.prefix:
            self.prefix = datestr

        return (self.day, self.month, self.year)

    def getlongdate(self):
        """Return the long form of the date string"""
        if self.isDate:
            my_date = datetime.datetime(self.year, self.month, self.day)
            weekday = calendar.day_name[my_date.weekday()]

            mnth = calendar.month_name[self.month]
            return f'{weekday} {mnth} {self.day}'
        else:
            print("Not a date")
            return ""

    def getPrefix(self):
        """Return the file prefix fromt the date variables"""
        if self.isDate:
            self.prefix = f"{self.month:02}{self.day:02}"
        return self.prefix

    def __str__(self):
        """Return the namestring"""
        return self.makestring()
