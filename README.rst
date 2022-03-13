\:pineapple: pyncat :cat2:
==========================

A simple, stateful code execution server for Python, inspired by ncat.

Warning
-------
pyncat will execute whatever you throw at it!

Be sure to sandbox your execution environment if it will
be exposed to untrusted input.

Installation
------------
Install from PyPI::

    pip install pyncat

Usage
-----
Start the pyncat listener::

    pyncat

Send your Python code for execution::

    echo 'import this' | nc 127.0.0.1 31337
