# SUDOKU SOLVER

import sys
from time import time
from sudokuUtil import *

# Please implement function solve_puzzle
# input puzzle: 2D list, for example:
# [ [0,9,5,0,3,2,0,6,4]
#   [0,0,0,0,6,0,1,0,0]
#   [6,0,0,0,0,0,0,0,0]
#   [2,0,0,9,0,3,0,0,6]
#   [0,7,6,0,0,0,0,0,3]
#   [3,0,0,0,0,0,0,0,0]
#   [9,0,0,5,0,4,7,0,1]
#   [0,5,0,0,2,1,0,9,0]
#   [0,0,8,0,0,6,3,0,5] ]
# Return a 2D list with all 0s replaced by 1 to 9.
# You can utilize argv to distinguish between algorithms
# (basic backtracking or with MRV and forward checking).
# For example: python sudokuSolver.py backtracking

global_puzzle = []

# Returns the total number of unsolved Cells, ie counts for the number of '0's
# in the puzzle array
def getNoOfUnsolvedCells(puzzle):
    noOfUnsolvedCells = 0

    for i in range(0,9):
        for j in range (0,9):
            if puzzle[i][j] == 0:
                noOfUnsolvedCells += 1

    return noOfUnsolvedCells

# is the number in given row?
def isInRow(puzzle, row, var):
    if var in puzzle[row]:
        return True

    return False

# is the number in given Column?
def isInColumn(puzzle, column, var):
    for i in range(0,9):
        if var == puzzle[i][column]:
            return True

    return False

# is the number in given sub-box?
def isInBox(puzzle, row, column, var):
    boxStartX = ((row/3) * 3)
    boxStartY = ((column/3) * 3)

    for i in range(boxStartX,(boxStartX + 3)):
        for j in range(boxStartY,(boxStartY + 3)):
            if var == puzzle[i][j]:
                return True

    return False

# A list generated for a cell in the 9x9 sudoku which says what are the
# numbers can be filled in the cell (takes those number which are not in any
# of current row, current column or current sub 3x3 box)
def getCanBeFilledList(puzzle, row, column):
    canBeFilledList = []

    for i in range(0,10):
        # not (inRow or inColumn or inBox)
        inRow = isInRow(puzzle, row, i)
        inColumn = isInColumn (puzzle, column, i)
        inBox = isInBox (puzzle, row, column, i)

        if not (inRow or inColumn or inBox):
            canBeFilledList.append(i)

    return canBeFilledList

# Returns the next cell that needs to be solved
def getNextEmptyCell(puzzle, curRow, curCol):

    for j in range(curCol, 9):
        if puzzle[curRow][j] == 0:
            return (curRow, j)

    for i in range(curRow+1,9):
        for j in range (0,9):
            if puzzle [i][j] == 0:
                return (i,j)

    return (-1,-1)

# Recursive backtrack algorithm
def basicBacktrackSudokuSolver(noOfUnsolvedCells, row, column):

    # Terminating condition
    if noOfUnsolvedCells == 0:
        return True

    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    (nextEmptyX, nextEmptyY) = getNextEmptyCell(global_puzzle, row, column+1)

    for i in getCanBeFilledList(global_puzzle, row, column):

        global_puzzle[row][column] = i
        noOfUnsolvedCells -= 1

        ret = basicBacktrackSudokuSolver(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
        if ret:
            # If successful say it to caller
            return True

        global_puzzle[row][column] = 0
        noOfUnsolvedCells += 1

    return False


def solve_puzzle(puzzle, argv):
    """Solve the sudoku puzzle."""
    global global_puzzle
    global_puzzle = puzzle[:]

    noOfUnsolvedCells = getNoOfUnsolvedCells(global_puzzle)

    (startX, startY) = getNextEmptyCell(puzzle, 0, 0)

    ret = basicBacktrackSudokuSolver(noOfUnsolvedCells, startX, startY)

    return global_puzzle
    #return load_sudoku('given_solution.txt')

#===================================================#
puzzle = load_sudoku('puzzle.txt')

print "solving ..."
t0 = time()
solution = solve_puzzle(puzzle, sys.argv)
t1 = time()
print "completed. time usage: %f" %(t1 - t0), "secs."

save_sudoku('solution.txt', solution)

