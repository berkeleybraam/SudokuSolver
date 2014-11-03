SudokuSolver
============
Note: Must have NumPy installed to run sudoku.py.

The file sudoku.py solves valid 9x9 Sudoku puzzles. To run solver, the command:
"python sudoku.py p1.csv" can be entered at the command prompt. The program applies
the sudoku problem solving techniques: rule of one, scanning columns, scanning rows, 
hidden pairs, and finding naked pairs. The program will list the methods used to fill
out the Sudoku puzzle. If the above techniques do not produce a solution, a recursive 
backtracking algorithm is applied to the Sudoku puzzle to find the solution. Inputting 
a non-valid sudoku puzzle will result in an error. The solution will be saved as a 
CSV file with the title sudokuOutput.csv.  

