# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:48:12 2021

@author: Tajwar
"""

from RelaxationLabeling import *


SodukoBoard = [
    [3, 7, 0, 5, 0, 0, 0, 0, 6],
    [0, 0, 0, 3, 6, 0, 0, 1, 2],
    [0, 0, 0, 0, 9, 1, 7, 5, 0],
    [0, 0, 0, 1, 5, 4, 0, 7, 0],
    [0, 0, 3, 0, 7, 0, 6, 0, 0],
    [0, 5, 0, 6, 3, 8, 0, 0, 0],
    [0, 6, 4, 9, 8, 0, 0, 0, 0],
    [5, 9, 0, 0, 2, 6, 0, 0, 0],
    [2, 0, 0, 0, 0, 5, 0, 6, 4]
]


def soduko(Sboard):
   #print(Sboard) #This shows how the backtracking works
    find = find_empty(Sboard) #finding the first empty cell
    if not find:
        return True #this means we find the solution and we are done
    else: #
        row, column = find

    # above code is actually the base case of recursion

    for i in range(1, 10): #Looping thru the board
        if check_validation(Sboard, i, (row, column)): #checking the validation of the number
            Sboard[row][column] = i  #if find a valid number insert into cell

            if soduko(Sboard):   # this is basic recursive step that actually backtracks we keep on trying trying trying to add
                # values untill the solution is find
                return True

            Sboard[row][column] = 0 # if the number is invalid that we fit we set the previous value to 0 and again try diff value

    return False

# This function checks the validity of the board
def check_validation(Sboard, number, position):
    #It takes three parameters the Board, the number which we fit in the cells, and the position where the number would be fit

    #we are basically checking three things
    #Rows
    #Columns
    #3x3 Boxes


    for i in range(len(Sboard[0])):  # Looping thru the every single column of a given row
        if Sboard[position[0]][i] == number and position[1] != i:  #We check each element in the row we just added in
            #the position[1] != i is that number we just inserted in we ignored that
            return False

    for i in range(len(Sboard)): #Now we are checking the column vertical
        if Sboard[i][position[1]] == number and position[0] != i:  # Nothing special its just opposite of row operation
            return False


    # Now we are checking the 3x3 Boxes in the Board
    # we make sure that No number coincides in the box 0 to 9

    #this 2 codes divides the whole board in 3x3 boxes and assign positions like [0,0] [0,1] [0,2] so on and so forth
    x = position[1] // 3
    y = position[0] // 3



    # looping through the 9 elements
    # Now we making sure that in the boxes now value is appearing twice
    #multiplying by 3 beacuse all the positions are either 0 or 1 2
    for i in range(y * 3, y * 3 + 3): # +3 is for going to the 3rd column and row
        for j in range(x * 3, x * 3 + 3):
            if Sboard[i][j] == number and (i, j) != position:
                return False

    return True

#Printing the board for better visualization
def print_board(SBoard):
    for i in range(len(SBoard)):
        if i % 3 == 0 and i != 0:
            print("-----------------------")

        for j in range(len(SBoard[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(SBoard[i][j])
            else:
                print(str(SBoard[i][j]) + " ", end="")
print("\n")
print("Initial Soduko Board")
print("\n")
print_board(SodukoBoard)
print("\n")

#Finding empty cell
def find_empty(SBoard):
    for i in range(len(SBoard)):
        for j in range(len(SBoard[0])):
            if SBoard[i][j] == 0:
                return (i, j)

    return None


soduko(SodukoBoard)

print("After using the Backtrack Algorithm we have the soduko ")
print("\n")

print_board(SodukoBoard)

print("\n")

print("Sudoku with Relaxation Labeling")
print("\n")

solve_relaxationLabeling(SodukoBoard)


