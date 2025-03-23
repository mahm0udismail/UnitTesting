# UnitTesting
 Unit testing using python

pytest -v tests/unit/test_helper_fun.py

PYTHONPATH=. pytest -ra tests/unit/test_helper_fun.py



# Pytest Command Explanation

### 1. Run Tests from a Specific Class but Exclude Certain Methods  
The command `pytest -k 'MyClass and not method'` runs tests that contain "MyClass" in their names but exclude those containing "method".  
It helps filter specific test cases when debugging or running targeted tests. 

### 2. Run Multiple Functions Starting with the Same Prefix  
If you have multiple test functions (not inside a class) and want to run only those that start with a specific prefix, use:  
`pytest -k 'test_prefix'`

### 3. Run Tests by Collection Arguments  
You can run specific test files, classes, or functions using collection arguments.  
For example, `pytest test_example.py::MyClass::test_feature1` runs only `test_feature1` inside `MyClass`.  
This allows for precise test execution and faster debugging.  

### 4. Run Tests by Markers  
Use `pytest -m slow` to run only tests marked as `@pytest.mark.slow`.  
This helps separate slow tests from regular ones, allowing for selective execution.  
To avoid warnings, define markers in `pytest.ini`.  

### 5. Run Tests from a File List  
You can run tests listed in a text file using `pytest @tests_to_run.txt`.  
This method is useful for rerunning failed tests or executing specific sets of tests efficiently.  
The file should contain one test per line, e.g.:  
```
 tests/test_example.py
 tests/test_auth.py::test_login
 tests/test_api.py::TestAPI::test_get_request
```

### 6. Fixtures in Pytest  
Fixtures in `pytest` prepare the test environment before running a test. They execute setup code before the test starts and can include teardown logic after the test finishes.

📌 **How do fixtures work?**  
- `pytest` looks for required fixtures in test function parameters.  
- If found, the fixture runs before the test starts.  
- If it includes teardown logic, it executes after the test finishes.  

🔹 **How often does a fixture run?**  
Depends on its **scope**:  
- `@pytest.fixture(scope="function")` ✅ Runs before each test (default).  
- `@pytest.fixture(scope="class")` ✅ Runs once per test class.  
- `@pytest.fixture(scope="module")` ✅ Runs once per test file.  
- `@pytest.fixture(scope="session")` ✅ Runs once per test session.  

### **7. Using `request.addfinalizer` and `yield` for Teardown in Fixtures**  

Fixtures in **pytest** support teardown logic using either:
1. **`request.addfinalizer()`** – Registers a function to run after the test.
2. **`yield`** – Executes teardown code after yielding the fixture's value.

---

#### ✅ **Using `request.addfinalizer` for Cleanup**
```python
import pytest

@pytest.fixture
def setup_resource(request):
    resource = {"connection": "Active"}
    print("\n🔹 Setting up resource:", resource)

    def cleanup():
        resource["connection"] = "Closed"
        print("\n🔸 Cleaning up resource:", resource)

    request.addfinalizer(cleanup)  # Register finalizer function
    return resource

def test_example(setup_resource):
    assert setup_resource["connection"] == "Active"
```

---

#### ✅ **Using `yield` for Cleanup**
```python
import pytest

@pytest.fixture
def setup_resource():
    resource = {"connection": "Active"}
    print("\n🔹 Setting up resource:", resource)
    yield resource
    resource["connection"] = "Closed"
    print("\n🔸 Cleaning up resource:", resource)

def test_example(setup_resource):
    assert setup_resource["connection"] == "Active"
```

---

### 🔹 **Comparison: `request.addfinalizer` vs `yield`**
| Feature | `request.addfinalizer` | `yield` |
|---------|------------------------|---------|
| Multiple cleanup functions | ✅ Yes (can register multiple) | ❌ No (only one teardown block) |
| Readability | ❌ Less readable | ✅ More readable |
| Compatibility | ✅ Works with old pytest versions | ✅ Recommended for modern pytest |

📌 **Best Practice:** Use `yield` for simple cases and `request.addfinalizer` if multiple cleanup steps are needed. 🚀