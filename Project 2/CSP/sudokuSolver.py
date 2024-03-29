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

                    # Add only those values which aren't in neither in
                    # row, column or box
                    if not (inRow or inColumn or inBox):
                        order_domain_values[i][j].append(var)

    return

# Returns the total number of unsolved Cells, ie counts for the number of '0's
# in the puzzle array, this is used as our termination condiation in the
# backtrack method. We decrement each time we get a solution and when it
# reaches 0 we reached solution !!
def getNoOfUnsolvedCells(puzzle):
    noOfUnsolvedCells = 0

    for i in range(0,9):
        for j in range (0,9):
            if puzzle[i][j] == 0:
                noOfUnsolvedCells += 1

    return noOfUnsolvedCells

# is the number in given row?
# This method is used for consistency check
def isInRow(puzzle, row, var):
    if var in puzzle[row]:
        return True

    return False

# is the number in given Column?
# This method is used for consistency check
def isInColumn(puzzle, column, var):
    for i in range(0,9):
        if var == puzzle[i][column]:
            return True

    return False

# is the number in given sub-box?
# This method is used for consistency check
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
# The complete order domain for any 3x3 sudoku problem is [1-9]
# this used in bruteforce method always returns lsit of 1-9
def getOrderDomainValues():
    return [1,2,3,4,5,6,7,8,9]

# this is common for all MRV, FC and Arc
# we've already prepared the solution domain so just return the
# list prepared, so need not to calculate anything
def getOrderDomainValuesMRV (orderDomainValues, row, column):
    return orderDomainValues[row][column]

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
            # Don't return the same row, column that the currently
            # operating on, so just continue in this case
            if i == row and j == column:
                continue

            if puzzle[i][j] == 0:
                if len(orderDomainValues[i][j]) < minLen:
                    min = (i, j)
                    minLen = len(orderDomainValues[i][j])

    return min

# Returns the next cell that needs to be solved without any intelligence
def selectUnassignedVariable(puzzle, curRow, curCol):

    # check for remaining cells in the current row
    for j in range(curCol, 9):
        if puzzle[curRow][j] == 0:
            return (curRow, j)

    # check for the remaining rows
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
# If it present in the any of the above it is not consistent (inconsistent)
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
def doInferenceArc(var, odv, row, column):
    global order_domain_values

    # Contraint remove don only if the constraint left with single value
    if len(odv[row][column]) != 1:
        return True

    orderDomainValues = [[[] for x in xrange(9)] for x in xrange(9)]

    for i in range(0,9):
        for j in range(0,9):
            orderDomainValues[i][j] = odv[i][j][:]

    orderDomainValues[row][column].remove(var)

    # Using BFS graph search clear all the constraints from the solution domain
    visitedCells = []
    # Fringe here is a Queue
    fringe = []
    fringe.insert (0, (row, column))

    # Propagate the constraint using the BFS method adds to the queue if any other
    # node with single value is found. The key is (row, column, value) that found
    # so it doesn't drop into infinite loop traversing the same nodes
    while (len (fringe) == 0):
        lrow, lcolumn = fringe.pop ()
        lvar = orderDomainValues[lrow][lcolumn][0]
        visitedCells.append ((lrow, lcolumn, lvar))

        # Remove from the corresponding row
        for j in range(0,9):
            if var in orderDomainValues[lrow][j]:
                if len (orderDomainValues [lrow][j]) == 1:
                    return False

                orderDomainValues[lrow][j].remove (lvar)
                # if len of this node is 1 and already not visited add it to queue
                if len (orderDomainValues[lrow][j]) == 1 and not((lrow, j, lvar) in visitedCells):
                    fringe.insert (0, (lrow, j))

        # Remove from the corresponding column
        for i in range(0,9):
            if var in orderDomainValues[i][lcolumn]:
                if len (orderDomainValues [i][lcolumn]) == 1:
                    return False

                orderDomainValues[i][lcolumn].remove (lvar)
                # if len of this node is 1 and already not visited add it to queue
                if len (orderDomainValues[i][lcolumn]) == 1 and not((lrow, j, lvar) in visitedCells):
                    fringe.insert (0, (i, lcolumn))

        boxStartX = ((lrow/3) * 3)
        boxStartY = ((lcolumn/3) * 3)

        # Remove from the corresponding box
        for i in range(boxStartX,(boxStartX + 3)):
            for j in range(boxStartY,(boxStartY + 3)):
                if var in orderDomainValues[i][j]:
                    if len (orderDomainValues [lrow][lcolumn]) == 1:
                        return False
                    orderDomainValues[i][j].remove (lvar)
                    # if len of this node is 1 and already not visited add it to queue
                    if len (orderDomainValues[i][j]) == 1 and not((lrow, j, lvar) in visitedCells):
                        fringe.insert (0, (i, j))

    for i in range(0,9):
        for j in range(0,9):
            order_domain_values[i][j] = orderDomainValues[i][j][:]

    return True

# Does an inference for Forward Checking
def doInferenceFC(var, odv, row, column):
    global order_domain_values

    # Contraint remove don only if the constraint left with single value
    if len(odv[row][column]) != 1:
        return True

    orderDomainValues = [[[] for x in xrange(9)] for x in xrange(9)]

    for i in range(0,9):
        for j in range(0,9):
            orderDomainValues[i][j] = odv[i][j][:]

    orderDomainValues[row][column].remove(var)

    # Remove from the corresponding row
    for j in range(0,9):
        if var in orderDomainValues[row][j]:
            if len (orderDomainValues [row][j]) == 1:
                return False

            orderDomainValues[row][j].remove (var)

    # Remove from the corresponding column
    for i in range(0,9):
        if var in orderDomainValues[i][column]:
            if len (orderDomainValues [i][column]) == 1:
                return False

            orderDomainValues[i][column].remove (var)

    boxStartX = ((row/3) * 3)
    boxStartY = ((column/3) * 3)

    # Remove from the corresponding box
    for i in range(boxStartX,(boxStartX + 3)):
        for j in range(boxStartY,(boxStartY + 3)):
            if var in orderDomainValues[i][j]:
                if len (orderDomainValues [i][j]) == 1:
                    return False

                orderDomainValues[i][j].remove (var)

    for i in range(0,9):
        for j in range(0,9):
            order_domain_values[i][j] = orderDomainValues[i][j][:]

    return True

###################################################################################################
##################### Main algos that checks responisble for backtracking #########################
###################################################################################################

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
            if doInferenceArc (i, order_domain_values, row, column):
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
            if doInferenceFC (i, order_domain_values, row, column):
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
def bruteforce(puzzle, noOfUnsolvedCells):

    (startX, startY) = selectUnassignedVariable(puzzle, 0, 0)

    bruteForceBacktrackMethod(noOfUnsolvedCells, startX, startY);

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

        print "Solving the puzzle using Forward Checking method"
        forwardcheck (puzzle, noOfUnsolvedCells);
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
        print "Solving the puzzle using Forward Checking method"
        forwardcheck (puzzle, noOfUnsolvedCells);
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

