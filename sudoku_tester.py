#!/usr/bin/env python
#coding:utf-8

"""
Sudoku tester file.

Usage: python3 sudoku_tester.py

Notes:
    * This file expects a file named 'sudokus_start.txt' to be in the same directory, which
    contains one Sudoku puzzle per line
    * There should also be a corresponding 'sudokus_finish.txt' with solutions to the puzzles
    * Do NOT submit this file, only submit sudoku.py and README.txt

TO-DO: Time your run of the sudoku boards
"""

import sys
import time
import statistics
from sudoku import *

def main():
    if len(sys.argv) > 1:
        print("Usage: python3 sudoku_tester.py")
        sys.exit(1)
    
    try:
        #  Read boards from test and solution files
        test_filename = "sudokus_start.txt"
        sol_filename = "sudokus_finish.txt"
        testfile = open(test_filename, "r")
        solfile = open(sol_filename, "r")

        try:
            test_list = testfile.read()
        except:
            print("Error reading the sudoku file %s" % test_list)
            exit()
        
        try:
            sol_list = solfile.read()
        except:
            print("Error reading the sudoku file %s" % sol_list)
            exit()

        # Setup puzzles and solutions
        puzzles = test_list.split("\n")
        solutions = sol_list.split("\n")

        # Solve each board using backtracking
        test_no = 1
        successes = []
        failures = []
        skips = []
        times = []
        
        for puzzle_no in range(len(puzzles)):
            puzzle = puzzles[puzzle_no]

            if len(puzzle) < 9:
                skips.append(test_no)
                test_no += 1
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(puzzle[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Uncomment this for debugging.
            # print_board(board)

            # Solve with backtracking
            start = time.time()
            solved_board = backtracking(board)
            end = time.time()
            times.append(end - start)

            # Print solved board. TODO: Uncomment this for debugging.
            # print_board(solved_board)

            if board_to_string(solved_board) == solutions[puzzle_no]:
                successes.append(test_no)
            else:
                failures.append((test_no, solved_board))
            test_no += 1

        # Print results
        print("=== Sudoku Test Results ===")

        print("Test case count: %d" % (test_no - 1))

        print("Successes:\t %d" % len(successes))

        if len(failures) == 0:
            print("Failures:\t 0")
        else:
            print("Failures:")
            for failure in failures:
                print("    - Board #%d\t- got %s" % (failure[0], board_to_string(failure[1])))

        if len(skips) == 0:
            print("Skipped:\t 0")
        if len(skips) > 0:
            print("Skipped:")
            for skip in skips:
                print("    - %d" % skip)
                
        if times:
            min_t = min(times)
            max_t = max(times)
            mean_t = statistics.mean(times)
            stdev_t = statistics.stdev(times) if len(times) > 1 else 0.0

#            print(f"Minimum: {min_t:.4f}")
#            print(f"Maximum: {max_t:.4f}")
#            print(f"Mean:    {mean_t:.4f}")
#            print(f"StdDev:  {stdev_t:.4f}")

            with open("README.txt", "w") as f:
                f.write(f"Boards solved successfully: {len(successes)}\n")
                f.write("Runtime Statistics (in seconds):\n")
                f.write(f"  Minimum: {min_t:.4f}\n")
                f.write(f"  Maximum: {max_t:.4f}\n")
                f.write(f"  Mean:    {mean_t:.4f}\n")
                f.write(f"  Standard Deviation: {stdev_t:.4f}\n\n")
                
    except FileNotFoundError:
        print("Error: 'sudokus_start.txt' file not found.")
        exit()

if __name__ == '__main__':
    main()
