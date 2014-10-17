#!/bin/sh

## DONT SUBMIT THIS ON BLACKBOARD
mv puzzle.txt puzzle.txt.backup
mv given_solution.txt given_solution.txt.backup
mv solution.txt solution.txt.backup

for i in `seq 1 10`; do
        echo "Team's solution round: $i"
        python sudokuGenerator.py > /dev/null 2>&1

        echo "Bruteforce round: $i"
        python sudokuSolver.py bruteforce
        python sudokuChecker.py > /tmp/testing 2>&1
        grep Error /tmp/testing

        if [ $? -eq 0 ]; then
                echo ""
                echo ""
                echo " Error"
                echo ""
                echo ""
        fi

        echo "MRV round: $i"
        python sudokuSolver.py mrv
        python sudokuChecker.py > /tmp/testing 2>&1
        grep Error /tmp/testing

        if [ $? -eq 0 ]; then
                echo ""
                echo ""
                echo " Error"
                echo ""
                echo ""
        fi

        echo "Forward check round: $i"
        python sudokuSolver.py forwardcheck
        python sudokuChecker.py > /tmp/testing 2>&1
        grep Error /tmp/testing

        if [ $? -eq 0 ]; then
                echo ""
                echo ""
                echo " Error"
                echo ""
                echo ""
        fi

        echo "Arc Consistency round: $i"
        python sudokuSolver.py arcconsistency
        python sudokuChecker.py > /tmp/testing 2>&1
        grep Error /tmp/testing

        if [ $? -eq 0 ]; then
                echo ""
                echo ""
                echo " Error"
                echo ""
                echo ""
        fi
done

mv puzzle.txt.backup puzzle.txt
mv given_solution.txt.backup given_solution.txt
mv solution.txt.backup solution.txt
