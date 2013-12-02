Super Word Search

===========


Run Environment:
Python 2.7.3
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

Used Python standard library: multiprocessig, sys, datetime



Two approaches to solving the super word search:
1. Single processing with Object Oriented (OO) design => main.py
2. Multiple processing with somewhat OO design => main_parallel.py

In tests run locally, on input_file_for_parallel.txt (i created this file and am providing it), multi-processing has proven to be more efficient in solving the puzzle. On average, the multi-processing approach solves puzzle in half the time, compared to the single processing approach.


