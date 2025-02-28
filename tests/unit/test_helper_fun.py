import pytest
from helper_fun import safe_divide

def test_safe_divide():
    assert safe_divide(10, 2) == 5
    
    e = safe_divide(10, 0)
    assert isinstance(e, Exception)
    assert str(e) == "division by zero" 