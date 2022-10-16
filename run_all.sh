#!/bin/zsh

python3 sudoku.py 
bat output.txt
diff -q output.txt sudokus_finish.txt
