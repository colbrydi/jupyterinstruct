from jupyterinstruct.nbfilename import nbfilename

def test_full_fn():
    filename = "1010-This_is_a_test_in-class-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(x.isDate)
    assert(x.isInstructor)
    assert(x.isInClass)
    assert(not x.isPreClass)
    assert(not new == filename)
    
def test_date_fn():
    filename = "1212-test.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new == filename)
    assert(x.isDate)
    assert(not x.isInstructor)
    assert(not x.isInClass)
    assert(not x.isPreClass)


def test_INSTRUCTOR_fn():
    filename = "01-test-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(new == filename)
    assert(not x.isDate)
    assert(x.isInstructor)
    assert(not x.isInClass)
    assert(not x.isPreClass)
    
def test_in_class_fn():
    filename = "0130_Software_Review_in-class-assignment-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(not new == filename)
    assert(x.isDate)
    assert(x.isInstructor)
    assert(x.isInClass)
    assert(not x.isPreClass)
    
    
def test_in_class_fn():
    filename = "0130_Software_Review_pre-class-assignment-INSTRUCTOR.ipynb"
    x = nbfilename(filename)
    new = x.makestring()
    assert(not new == filename)
    assert(x.isDate)
    assert(x.isInstructor)
    assert(not x.isInClass)
    assert(x.isPreClass)

