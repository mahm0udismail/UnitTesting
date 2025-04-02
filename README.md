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

### **8. Running multiple assert statements safely**  
Use `autouse=True` in pytest fixtures to execute shared setup steps automatically before each test in the same class without explicitly calling the fixture. This helps avoid redundant setup calls and ensures a clean test environment.  

#### Example:  
```python
import pytest

@pytest.fixture(scope="class", autouse=True)
def setup():
    print("\n🔹 Setting up before each test")

class TestExample:
    def test_one(self):
        print("✅ Running test_one")

    def test_two(self):
        print("✅ Running test_two")
```
📌 **Output:** The setup runs before each test in `TestExample`, without needing to reference it explicitly.


### **9. Parametrizing Fixtures in Pytest**  
Parametrizing fixtures allows running the same test multiple times with different data by using **`@pytest.fixture(params=[...])`**. It helps reduce redundancy and improves test coverage. Example:  

```python
@pytest.fixture(params=[("Alice", 25), ("Bob", 30), ("Charlie", 35)])
def user_data(request):
    return {"name": request.param[0], "age": request.param[1]}

def test_user_age(user_data):
    assert user_data["age"] > 20
```

### **10. Using Marks with Parametrized Fixtures**  

You can use `pytest.mark` with parametrized fixtures to skip specific tests or expect failures based on certain conditions.  
This helps in better organizing tests and managing different scenarios efficiently.  

#### ✅ **Example:**  
```python
import pytest

@pytest.fixture(params=[("Lisa", True), ("Mike", False), ("Meredith", True)])
def customer_data(request):
    return request.param

@pytest.mark.parametrize("name, is_active", [("Alice", True), ("Bob", False)])
def test_customer_status(customer_data, name, is_active):
    customer_name, active_status = customer_data
    assert active_status == is_active
```
This test runs multiple times with different customer data while using parametrized markers for better flexibility. 🚀

### **11. Skipping and Expected Failures in Tests**  

You can use `@pytest.mark.skip` to skip tests that are not needed in certain conditions and `@pytest.mark.xfail` to mark tests expected to fail.  

#### ✅ **Example:**  
```python
import pytest

@pytest.mark.skip(reason="Skipping Eve's test")
def test_eve():
    assert True  

@pytest.mark.xfail(reason="Mallory is under 18, expected test failure")
def test_mallory():
    age = 16
    assert age >= 18  
```
This ensures `test_eve` is skipped, and `test_mallory` is expected to fail due to the age condition. 🚀

### **12. Using `@pytest.mark.usefixtures` in Pytest**

`@pytest.mark.usefixtures` is used to specify which fixtures should be executed before a test runs without passing them as arguments to the test. It allows for running setup code before tests without the need to directly reference the fixture in the test function.

### Example:
```python
import pytest

@pytest.fixture
def setup_data():
    print("Setup data before test")

@pytest.mark.usefixtures("setup_data")
def test_example():
    print("Running test_example")
```

**Output:**
```
Setup data before test
Running test_example
```

### **13. Using `filterwarnings` in Pytest**

The `filterwarnings` marker in Pytest allows you to filter specific warnings during test execution, enabling you to ignore or customize how warnings are handled. It's useful when you want to suppress or modify warning behavior for certain tests.

#### **Example:**
```python
import pytest

@pytest.mark.filterwarnings("ignore:.*DeprecationWarning.*")
def test_example():
    # Ignore DeprecationWarning during this test
    warn("This is a deprecated feature", DeprecationWarning)
    assert True
```
In this example, any `DeprecationWarning` will be ignored during the execution of the test.

### **14. Using `@pytest.mark.skipif` in Pytest**

The `@pytest.mark.skipif` marker allows you to skip a test function based on a specific condition. It's useful for skipping tests when certain environments or conditions are not met.

#### **Example:**
```python
import pytest
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Test is skipped on Windows")
def test_example():
    assert True
```
In this example, the test will be skipped if the platform is Windows (`win32`).


In **pytest**, you can re-run failed tests and maintain state between test runs using the following methods:

---


Here’s the structured content as per your request:  

---

### **15. How to re-run failed tests and maintain state between test runst**  

#### **1. Re-running Failed Tests Automatically**  
- **Use `pytest-rerunfailures` plugin** to automatically re-run failed tests.  

##### **Installation:**  
- Install the plugin using:  
  ```bash
  pip install pytest-rerunfailures
  ```  

##### **Usage:**  
- Run tests with re-run options:  
  ```bash
  pytest --reruns 3 --reruns-delay 2
  ```  
  - **`--reruns 3`** → Re-run failed tests up to **3** times.  
  - **`--reruns-delay 2`** → Wait **2 seconds** before re-running.  

##### **Example:**  
- Use `@pytest.mark.flaky` for specific test functions:  
  ```python
  import pytest

  @pytest.mark.flaky(reruns=3, reruns_delay=2)
  def test_unstable():
      import random
      assert random.choice([True, False])
  ```  
  - If the test fails, it will retry **3** times with a **2-second delay**.  

---

#### **2. Running Only Failed Tests**  
- **Use `pytest --lf`** to run only tests that failed in the last session.  

##### **Command:**  
- Run the last failed tests:  
  ```bash
  pytest --lf
  ```  

- **Use `pytest --ff`** to run failed tests first before other tests.  
  ```bash
  pytest --ff
  ```  

---

#### **3. Persisting Test Results Between Runs**  
- **Pytest stores the state of test results** in a cache directory (`.pytest_cache`).  

##### **Commands:**  
- Show last failed tests:  
  ```bash
  pytest --cache-show
  ```  
- Clear cached test results:  
  ```bash
  pytest --cache-clear
  ```  

---

#### **4. Summary**  

| Method | Description | Command/Code |  
|--------|-------------|-------------|  
| `pytest-rerunfailures` | Auto re-run failed tests | `pytest --reruns 3 --reruns-delay 2` |  
| `pytest --lf` | Run only last failed tests | `pytest --lf` |  
| `pytest --ff` | Run failed tests first | `pytest --ff` |  
| `pytest --cache-show` | Show cached failed tests | `pytest --cache-show` |  
| `pytest --cache-clear` | Clear cache | `pytest --cache-clear` |  

---

### **16. How to handle test failures**  
#### **1. Stopping after the first (or N) failures** 
##### **Commands:**  
- ##### stop after first failure:  
  ```bash
  pytest -x
  ```  
- ##### stop after two failures:  
  ```bash
  pytest --maxfail=2  
  ``` 
- ##### Dropping to pdb on failures
  ```bash
    pytest --pdb
  ``` 
- ##### Dropping to pdb at the start of a test:
  ```bash
  pytest --trace 
  ``` 
   

### **17.Example Explaining the Difference Between `-x` / `--maxfail` and `--pdb` / `--trace`**  

#### **1. Simple Test Code with Some Failures:**  
```python
import pytest

def test_pass():
    assert 1 + 1 == 2  # This test will pass

def test_fail_1():
    assert 1 + 1 == 3  # This test will fail

def test_fail_2():
    assert "hello".upper() == "hello"  # This test will also fail

def test_fail_3():
    assert len([1, 2, 3]) == 5  # This test will fail too
```

---

### **2. Running `pytest -x` (Stop at First Failure Only)**  
```bash
pytest -x test_example.py
```
🔹 **Result:**  
- `test_pass` runs first (✅ Pass).  
- `test_fail_1` runs next (❌ Fails).  
- **Execution stops immediately after the first failure (`-x`).**  
- `test_fail_2` and `test_fail_3` will **not** run.  

---

### **3. Running `pytest --maxfail=2` (Stop After Two Failures)**  
```bash
pytest --maxfail=2 test_example.py
```
🔹 **Result:**  
- `test_pass` runs first (✅ Pass).  
- `test_fail_1` runs next (❌ Fails).  
- `test_fail_2` runs next (❌ Fails).  
- **Execution stops after the second failure (`--maxfail=2`).**  
- `test_fail_3` will **not** run.  

---

### **4. Running `pytest --pdb` (Drop into `pdb` on Every Failure)**  
```bash
pytest --pdb test_example.py
```
🔹 **Result:**  
- `test_pass` runs first (✅ Pass).  
- `test_fail_1` fails and enters `pdb`:  
  ```python
  > assert 1 + 1 == 3
  (Pdb)  # You can inspect variables and debug here
  ```
- After exiting `pdb`, `test_fail_2` runs and enters `pdb` again.  
- This happens for every failed test.  

---

### **5. Running `pytest --trace` (Drop into `pdb` at the Start of Each Test)**  
```bash
pytest --trace test_example.py
```
🔹 **Result:**  
- Before running `test_pass`, pytest enters `pdb`.  
- After executing `test_pass`, pytest enters `pdb` before `test_fail_1`.  
- This happens before every test, allowing you to inspect each step before execution.  

---

### **📌 When to Use Each?**
| Scenario | Use |
|----------|-----|
| Stop running tests after the first failure | `pytest -x` |
| Stop running tests after a specific number of failures | `pytest --maxfail=N` |
| Drop into `pdb` only when a test fails | `pytest --pdb` |
| Stop at the first failure **and** enter `pdb` | `pytest -x --pdb` |
| Debug only the first `N` failures | `pytest --pdb --maxfail=N` |
| Enter `pdb` at the start of every test | `pytest --trace` |

🚀 **Summary:**  
- **`-x` and `--maxfail`**: Stop test execution after a certain number of failures.  
- **`--pdb` and `--trace`**: Debug failures interactively using `pdb`.