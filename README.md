# sudoku-solver
## A Sudoku solver using backtracking search with constraint propagation and minimum remaining value heuristic.

The sudoku is represented as a string of 81 (9x9) numbers

## Usage
### Initial Puzzle

2 5 0 0 0 7 0 0 1 

0 0 0 0 0 4 0 5 0 

0 1 0 0 2 0 3 6 7 

0 0 0 6 0 0 0 0 0 

0 0 0 0 8 1 0 3 0 

0 8 0 0 4 0 7 0 6 

6 2 0 1 0 0 0 7 0 

0 0 9 4 0 0 0 0 8 

8 0 0 0 0 6 0 0 3 

### Input
```
$python3 sudoku.py 250007001000004050010020367000600000000081030080040706620100070009400008800006003
```
### Output
```
output.txt
258367941367914852914825367432679185796581234185243796623158479579432618841796523

