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

nodesExpanded = 0
global_puzzle = []
order_domain_values = [[[] for x in xrange(9)] for x in xrange(9)]

#########################################################################
##################### General methods used by all algos #################
#########################################################################

# Established the solution domain by traversing through the sudoku
# Creates a list for each empty cell by the order domain values
# and removes the values which are inconsistent
def establishSolutionDomain(puzzle):
    global order_domain_values

    for i in range(0,9):
        for j in range (0,9):
            if puzzle[i][j] == 0:
                for var in range(1,10):
                    # not (inRow or inColumn or inBox)
                    inRow = isInRow(puzzle, i, var)
                    inColumn = isInColumn (puzzle, j, var)
                    inBox = isInBox (puzzle, i, j, var)

                    if not (inRow or inColumn or inBox):
                        order_domain_values[i][j].append(var)

    return

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

#########################################################################
##################### different methods to serve domain values ##########
#########################################################################
def getOrderDomainValues():
    return [1,2,3,4,5,6,7,8,9]

# this is common for all MRV, FC and Arc
def getOrderDomainValuesMRV (orderDomainValues, row, column):
    return orderDomainValues[row][column]

# A list generated for a cell in the 9x9 sudoku which says what are the
# numbers can be filled in the cell (takes those number which are not in any
# of current row, current column or current sub 3x3 box) for Team's solution
def getCanBeFilledList(puzzle, row, column):
    canBeFilledList = []

    for i in range(1,10):
        # not (inRow or inColumn or inBox)
        inRow = isInRow(puzzle, row, i)
        inColumn = isInColumn (puzzle, column, i)
        inBox = isInBox (puzzle, row, column, i)

        if not (inRow or inColumn or inBox):
            canBeFilledList.append(i)

    return canBeFilledList


#########################################################################
##################### Selects the next cell that needs to be solved #####
#########################################################################

# This is the main logic of MRV which returns the cell with least
# possible order domain values by minimizing the no of wrong tree path
# expansion, we can also use this in the FC and Arc consistency algos
def selectUnassignedVariableMRV(puzzle, orderDomainValues, row, column):
    min = (-1, -1)
    minLen = 10

    for i in range(0,9):
        for j in range(0,9):
            if i == row and j == column:
                continue

            if puzzle[i][j] == 0:
                if len(orderDomainValues[i][j]) < minLen:
                    min = (i, j)
                    minLen = len(orderDomainValues[i][j])

    return min

# Returns the next cell that needs to be solved without any intelligence
def selectUnassignedVariable(puzzle, curRow, curCol):

    for j in range(curCol, 9):
        if puzzle[curRow][j] == 0:
            return (curRow, j)

    for i in range(curRow+1,9):
        for j in range (0,9):
            if puzzle [i][j] == 0:
                return (i,j)

    return (-1,-1)


#########################################################################
##################### consistency check methods #########################
#########################################################################

#Consistency check
# This checks whtether a value can be assigned at the current row and column
# based on the puzzle inputs
# How does it do?
# Checks whether the given value already present in the given row/column/box
def isConsistent (var, puzzle, row, column):
    inRow = isInRow(puzzle, row, var)
    inColumn = isInColumn (puzzle, column, var)
    inBox = isInBox (puzzle, row, column, var)

    if (inRow or inColumn or inBox):
        return False

    return True

###################################################################################################
##################### Inference Algos for FC and Arc #############################################
###################################################################################################

# Does an inference for Arc consistency
# Constraint propagation
def doInferenceArc(var, orderDomainValues, row, column):
    # Contraint remove don only if the constraint left with single value
    if len(orderDomainValues[row][column]) != 1:
        return

    orderDomainValues[row][column].remove(var)

    # Using DFS graph search clear all the constraints from the solution domain
    visitedCells = []
    fringe = []
    fringe.append ((row, column))

    while (len (fringe) == 0):
        lrow, lcolumn = fringe.pop ()
        lvar = orderDomainValues[lrow][lcolumn][0]
        visitedCells.append ((lrow, lcolumn, lvar))

        # Remove from the corresponding row
        for j in range(0,9):
            orderDomainValues[lrow][j].remove (lvar)
            if len (orderDomainValues[lrow][j]) == 1 and not((lrow, j, lvar) in visitedCells):
                fringe.append (( row, j))

        # Remove from the corresponding column
        for i in range(0,9):
            orderDomainValues[i][lcolumn].remove (lvar)
            if len (orderDomainValues[i][lcolumn]) == 1 and not((lrow, j, lvar) in visitedCells):
                fringe.append ((i, lcolumn))

        boxStartX = ((lrow/3) * 3)
        boxStartY = ((lcolumn/3) * 3)

        # Remove from the corresponding box
        for i in range(boxStartX,(boxStartX + 3)):
            for j in range(boxStartY,(boxStartY + 3)):
                orderDomainValues[i][j].remove (lvar)
                if len (orderDomainValues[i][j]) == 1 and not((lrow, j, lvar) in visitedCells):
                    fringe.append ((i, j))

# Does an inference for Forward Checking
def doInferenceFC(var, orderDomainValues, row, column):
    # Contraint remove don only if the constraint left with single value
    if len(orderDomainValues[row][column]) != 1:
        return

    orderDomainValues[row][column].remove(var)

    # Remove from the corresponding row
    for j in range(0,9):
        if var in orderDomainValues[row][j]:
            orderDomainValues[row][j].remove (var)

    # Remove from the corresponding column
    for i in range(0,9):
        if var in orderDomainValues[i][column]:
            orderDomainValues[i][column].remove (var)

    boxStartX = ((row/3) * 3)
    boxStartY = ((column/3) * 3)

    # Remove from the corresponding box
    for i in range(boxStartX,(boxStartX + 3)):
        for j in range(boxStartY,(boxStartY + 3)):
            if var in orderDomainValues[i][j]:
                orderDomainValues[i][j].remove (var)

    return

###################################################################################################
##################### Main algos that checks responisble for backtracking #########################
###################################################################################################
# Recursive backtrack algorithm
def oursolutionSudokuSolver(noOfUnsolvedCells, row, column):
    # To display the statistics
    global nodesExpanded
    nodesExpanded += 1

    # Terminating condition
    if noOfUnsolvedCells == 0:
        return True

    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    (nextEmptyX, nextEmptyY) = selectUnassignedVariable(global_puzzle, row, column+1)

    for i in getCanBeFilledList(global_puzzle, row, column):

        global_puzzle[row][column] = i
        noOfUnsolvedCells -= 1

        ret = oursolutionSudokuSolver(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
        if ret:
            # If successful say it to caller
            return True

        global_puzzle[row][column] = 0
        noOfUnsolvedCells += 1

    return False

# Arc consistency added to the naive backtrack method
def arcconsistencyBacktrackMethod(noOfUnsolvedCells, row, column):

    # To display the statistics
    global nodesExpanded
    nodesExpanded += 1

    # Terminating condition - ie Is the assignment complete?
    # If so terminate the control by returning 'assignment'.
    if noOfUnsolvedCells == 0:
        return True

    # Check for error condition
    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    orderDomainValues = getOrderDomainValuesMRV (order_domain_values, row, column);

    for i in orderDomainValues:
        # Check for consistency - Look at the function definition for consistency detail
        if isConsistent (i, global_puzzle, row, column):
            # If consistent assign the variable
            global_puzzle[row][column] = i
            noOfUnsolvedCells -= 1

            # Plese check the what does this function do above the function definition
            doInferenceArc (i, order_domain_values, row, column)

            # Select-Unassigned-Variable - returns the next empty cell with minimum remaining values (MRV)
            (nextEmptyX, nextEmptyY) = selectUnassignedVariableMRV (global_puzzle, order_domain_values, row, column)

            ret = arcconsistencyBacktrackMethod(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
            if ret:
                # If successful say it to caller
                return True

            global_puzzle[row][column] = 0
            noOfUnsolvedCells += 1

    return False

# Forward checking added to the naive backtrack method
def forwardcheckBacktrackMethod(noOfUnsolvedCells, row, column):

    # To display the statistics
    global nodesExpanded
    nodesExpanded += 1

    # Terminating condition - ie Is the assignment complete?
    # If so terminate the control by returning 'assignment'.
    if noOfUnsolvedCells == 0:
        return True

    # Check for error condition
    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    orderDomainValues = getOrderDomainValuesMRV (order_domain_values, row, column);

    for i in orderDomainValues:
        # Check for consistency - Look at the function definition for consistency detail
        if isConsistent (i, global_puzzle, row, column):
            # If consistent assign the variable
            global_puzzle[row][column] = i
            noOfUnsolvedCells -= 1

            # Plese check the what does this function do above the function definition
            doInferenceFC (i, order_domain_values, row, column)

            # Select-Unassigned-Variable - returns the next empty cell with minimum remaining values (MRV)
            (nextEmptyX, nextEmptyY) = selectUnassignedVariableMRV (global_puzzle, order_domain_values, row, column)

            ret = forwardcheckBacktrackMethod(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
            if ret:
                # If successful say it to caller
                return True

            global_puzzle[row][column] = 0
            noOfUnsolvedCells += 1

    return False


# Question 5 part A
def mrvBacktrackMethod(noOfUnsolvedCells, row, column):

    # To display the statistics
    global nodesExpanded
    nodesExpanded += 1

    # Terminating condition - ie Is the assignment complete?
    # If so terminate the control by returning 'assignment'.
    if noOfUnsolvedCells == 0:
        return True

    # Check for error condition
    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    # Select-Unassigned-Variable - returns the next empty cell
    (nextEmptyX, nextEmptyY) = selectUnassignedVariableMRV (global_puzzle, order_domain_values, row, column)

    # For the brute-force method the Order domain is always 1-9
    orderDomainValues = getOrderDomainValuesMRV (order_domain_values, row, column);

    for i in orderDomainValues:
        # Check for consistency - Look at the function definition for consistency detail
        if isConsistent (i, global_puzzle, row, column):
            # If consistent assign the variable
            global_puzzle[row][column] = i
            noOfUnsolvedCells -= 1

            ret = mrvBacktrackMethod(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
            if ret:
                # If successful say it to caller
                return True

            # If failure UN-assign the variable and decrement the noOfUnsolvedCells var
            global_puzzle[row][column] = 0
            noOfUnsolvedCells += 1

    # Couldn't find the solution so backtrack and say False to caller
    return False

# Naive Brute-force backtrack
# Question 4
def bruteForceBacktrackMethod(noOfUnsolvedCells, row, column):

    # To display the statistics
    global nodesExpanded
    nodesExpanded += 1

    # Terminating condition - ie Is the assignment complete?
    # If so terminate the control by returning 'assignment'.
    if noOfUnsolvedCells == 0:
        return True

    # Check for error condition
    if row == -1 or column == -1:
        print "Received Unexpected Logic Error or Unsolvable input puzzle"
        sys.exit()

    # Select-Unassigned-Variable - returns the next empty cell
    (nextEmptyX, nextEmptyY) = selectUnassignedVariable (global_puzzle, row, column+1)

    # For the brute-force method the Order domain is always 1-9
    orderDomainValues = getOrderDomainValues ();

    for i in orderDomainValues:
        # Check for consistency - Look at the function definition for consistency detail
        if isConsistent (i, global_puzzle, row, column):
            # If consistent assign the variable
            global_puzzle[row][column] = i
            noOfUnsolvedCells -= 1

            ret = bruteForceBacktrackMethod(noOfUnsolvedCells, nextEmptyX, nextEmptyY)
            if ret:
                # If successful say it to caller
                return True

            # If failure UN-assign the variable and decrement the noOfUnsolvedCells var
            global_puzzle[row][column] = 0
            noOfUnsolvedCells += 1

    # Couldn't find the solution so backtrack and say False to caller
    return False



# Arc Consistency triggering method
def arcconsistency(puzzle, noOfUnsolvedCells):
    establishSolutionDomain (puzzle)

    # Get the minimum remaining value
    (startX, startY) = selectUnassignedVariableMRV(puzzle, order_domain_values, 0, 0)

    arcconsistencyBacktrackMethod (noOfUnsolvedCells, startX, startY)

    return

# Trigger the forward check algorithm
def forwardcheck(puzzle, noOfUnsolvedCells):
    establishSolutionDomain (puzzle)

    (startX, startY) = selectUnassignedVariableMRV(puzzle, order_domain_values, 0, 0)

    forwardcheckBacktrackMethod (noOfUnsolvedCells, startX, startY)

    return

# Triggering the MRV consistency function algorithm
def mrv(puzzle, noOfUnsolvedCells):
    establishSolutionDomain (puzzle)

    (startX, startY) = selectUnassignedVariableMRV(puzzle, order_domain_values, 0, 0)

    mrvBacktrackMethod (noOfUnsolvedCells, startX, startY)

    return

# Triggering function for bruteforce algorith
def oursolution(puzzle, noOfUnsolvedCells):

    (startX, startY) = selectUnassignedVariable(puzzle, 0, 0)

    oursolutionSudokuSolver (noOfUnsolvedCells, startX, startY);

    return

# Triggering function for bruteforce algorith
def bruteforce(puzzle, noOfUnsolvedCells):

    (startX, startY) = selectUnassignedVariable(puzzle, 0, 0)

    oursolutionSudokuSolver(noOfUnsolvedCells, startX, startY);

    return

def solve_puzzle(puzzle, argv):
    """Solve the sudoku puzzle."""
    global global_puzzle
    global_puzzle = puzzle[:]

    noOfUnsolvedCells = getNoOfUnsolvedCells(puzzle)
    if len (argv) == 1:
        print "Wrong argument please specify: either of the below"
        print "1. bruteforce"
        print "2. mrv"
        print "3. forwardcheck"
        print "4. arconsistency"
        print "Defaulting to Team's method"
        print "Solving the puzzle using own method"
        ret = oursolution(puzzle, noOfUnsolvedCells)
        print "Nodes Expanded: ", nodesExpanded

        return global_puzzle


    if argv[1] == "bruteforce":
        print "Solving the puzzle using Bruteforce Backtrack method"
        bruteforce(puzzle, noOfUnsolvedCells);
        print "Nodes Expanded: ", nodesExpanded

    elif argv[1] == "mrv":
        print "Solving the puzzle using MRV heuristic method"
        mrv (puzzle, noOfUnsolvedCells);
        print "Nodes Expanded: ", nodesExpanded

    elif argv[1] == "forwardcheck":
        print "Solving the puzzle using Forward Checking method"
        forwardcheck (puzzle, noOfUnsolvedCells);
        print "Nodes Expanded: ", nodesExpanded

    elif argv[1] == "arcconsistency":
        print "Solving the puzzle using Arc consistency method"
        arcconsistency (puzzle, noOfUnsolvedCells);
        print "Nodes Expanded: ", nodesExpanded

    else:
        print "Wrong argument please specify: either of the below"
        print "1. bruteforce"
        print "2. mrv"
        print "3. forwardcheck"
        print "4. arconsistency"
        print "Defaulting to Team's method"
        print "Solving the puzzle using own method"
        ret = oursolution(puzzle, noOfUnsolvedCells)
        print "Nodes Expanded: ", nodesExpanded

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

