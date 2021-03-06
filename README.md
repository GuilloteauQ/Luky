# Luky
Luky - Script for easy (Rust/Cargo like) tests in Python

## Installation

You can add this line to your ```.bashrc``` file to execute ```luky``` from everywhere:

```bash
alias luky="python3 path/to/luky.py"
```

## How does it work ?

You have a test file for your Python project, with your test functions (no parameter)
If you write ``#[test]`` before your function, and then run ``luky your_test_file.py``,
it will run your test function and print if it passed the test (complete its run) or if it failed.

Luky can take several Python files as input and can show the time of each test if you put the ``--time`` or the ``-t`` tags.

It also displays colors in the terminal by default. But if your terminal does not support colors, you can disable this with the
``--no-color`` tag.

There is an help that you can see with the ``--help`` or ``-h`` tags.

## Example

``my_tests.py``:

```python

#[test]
def stupid_test():
    assert 10 < 1

def untested_test():
     assert 1 == 1

#[test]
def test_add():
    assert 1 + 1 == 2
```
Then we run ``luky my_tests.py``

And we get :

```python
---------- my_tests.py ----------
[failed] : stupid_test
[passed] : test_add
Tests passed : 1 / 2
```
(The ``passed`` and ``failed`` are in green and red, but i couldn't figure out how to put color ...)

## Limits

Works only in Python3 (Python2 incoming..) and on Linux (maybe MacOS).

## Motivation

I've played a bit with [Rust](http://www.rust-lang.org) and with Cargo. A cool feature of the compiler is the test run. You can write tests functions within your program with the test macro, and they will not be executed during a standart run (``cargo run``), but only with a 'test run'(``cargo test``).
I found this pretty cool, and then tried to do kind of the same in Python.
