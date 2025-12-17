#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("------------------------")
    rownum = 0
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
            if int(j) % 3 == 0:
                row += " | "
        print(row)
        if rownum % 3 == 2:
            print("------------------------")
        rownum += 1


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solved_board = backtracking_internal(board)
    # write to output.txt if solved_board is not None
    return solved_board

def backtracking_internal(board):
    # if assignment complete then return the board
    if assignmentComplete(board):
#        print(f"Done!!!!!!! {board_to_string(board)}")
        # print_board (board)
        return board
    
    next_cell, possible_val = findMinRemainingValues(board)
    for val in possible_val:
        board[next_cell] = int(val)
        result = backtracking_internal(board)
        if result != None:
            # this value worked all the way down, so return this board
            return result
        board[next_cell] = 0
    return None # if possible_val is "" or no value worked then this cannot proceed

def assignmentComplete (board):
    if 0 in board.values():
        return False
    else:
        return True
    
def findMinRemainingValues(board):
    # this uses minimum remaining value heuristic.
    # It chooses the cell which can have min legal values.
    # If there is a cell that has 0 legal values then it just returns empty value which is then used to backtrack
    possible_vals = {}
    next_cell = None
    for index_r, r in enumerate(ROW):
        for  index_c, c in enumerate(COL):
            val = board[r+c]
            if val != 0:
                continue
            vals = "123456789"
            # go through all columns of the same row
            for c1 in COL:
                if board[r+c1] != 0:
                    vals = vals.replace(str(board[r+c1]), "")
            # go through all row of the same column
            for r1 in ROW:
                if board[r1+c] != 0:
                    vals = vals.replace(str(board[r1+c]), "")
            # go through the 3X3 metrics
            start_r = index_r - (index_r % 3)
            start_c = index_c - (index_c % 3)
            for r1 in range(start_r, start_r + 3):
                for c1 in range(start_c, start_c + 3):
                    if board[ROW[r1]+COL[c1]] != 0:
                        vals = vals.replace(str(board[ROW[r1]+COL[c1]]), "")
            # if there is no possible value for a given cell then you can't proceed with this any more
            if (len(vals)) == 0:
                return r+c, ""
            if (next_cell is None) or (len(possible_vals[next_cell]) > len(vals)):
                next_cell = r+c
            possible_vals[r+c] = vals
    # print(possible_vals)
    return next_cell, possible_vals[next_cell]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) < 9:
            print("Input string too short")
            exit()

        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")
    
    print("Finishing all boards in file.")
