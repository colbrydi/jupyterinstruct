from jupyterinstruct.nbfilename import nbfilename

def test_full_fn():
    filename = "1010-This_is_a_test-in-class-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new == filename)
    assert(x.isInstructor)
    assert(x.isDate)
    assert(x.isInClass)
    assert(not x.isPreClass)
    
def test_date_fn():
    filename = "1212-test.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new = filename)

def test_INSTRUCTOR_fn():
    filename = "01-test-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new = filename)
    
def test_in_class_fn():
    filename = "0130_Software_Review_in-class-assignment-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new = filename)
    
    
def test_in_class_fn():
    filename = "0130_Software_Review_pre-class-assignment-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new = filename)
