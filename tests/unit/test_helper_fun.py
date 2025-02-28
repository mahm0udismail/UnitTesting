import pytest
from helper_fun import safe_divide

def test_safe_divide():
    assert safe_divide(10, 2) == 5
    
    e = safe_divide(10, 0)
    assert isinstance(e, Exception)
    assert str(e) == "division by zero" 

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (8, 4, 2),
    (7, 0, "division by zero" )
])
def test_safe_divide_with_parametrize(a, b, expected):
    assert safe_divide(a, b) == expected

@pytest.mark.slow
def test_slow_function():
    import time
    time.sleep(2)  
    assert True

# This test will be skipped
@pytest.mark.skip(reason="Skipping this test for now")
def test_skip_example():
    assert 1 + 1 == 2  

# This test will fail, but pytest won't count it as a failure
@pytest.mark.xfail(reason="This is a known issue")
def test_xfail_example():
    assert 1 + 1 == 3  