# Interpretation of specs

## Cache is entirely in memory

With the current implementation, the value can be modified outside of the cache, because it's a pointer to an object in memory, and others have access to the same pointer to the object in memory. The value could be serialized with something like `pickle.dumps`, should we need to add a new requirement like, "make a deep copy of the value at time of cache write" or if we choose to use a different cache persistence.

## Design the interface as a library

pip install is acceptable

## Provide a way for any alternative replacement algorithm to be used

If the alternative replacement algorithm needs radically different data, a major version change and refactor is acceptable. Ex 1: if the whole history of cache reads is required. Ex 2: if the keys are required for the replacement algorithm.

# Build/Test

1. Have a version of python3 installed.
2. Install pytest.
3. Change directory to the set-associative-cache folder and run: `py.test`.

Example:

```
> py.test
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-3.1.2
rootdir: /home/douglas/workspace/set-associative-cache, inifile:
collected 13 items 

app_test.py .............

========================== 13 passed in 0.08 seconds ===========================
```