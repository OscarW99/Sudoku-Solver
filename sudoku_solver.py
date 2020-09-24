# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:44:11 2020

@author: oscar
"""
import time
import numpy as np
from tkinter import *


    
def checkRow(board, row, num, checkBoard = False):
    """ a function to check row for number and/or check number is valid in row"""
    global error_messages
    valid = False
    if num in board[row]:
        if checkBoard:
            a = board[row].count(num)
            if a > 1:
                error = str(num) + ' appears '+ str(a) + ' times in a row'
                error_messages.append(error)
            else:
                valid = True
    else:
        valid = True
    return valid
 

    
def checkCol(board, col, num, checkBoard = False):
    """ a function to check column for number """
    global error_messages
    temp_col_nums = [row[col] for row in board]
    valid = False
    if num in temp_col_nums:
        if checkBoard:
            a = temp_col_nums.count(num)
            if a > 1:
                error = str(num) + ' appears '+ str(a) + ' times in a column'
                error_messages.append(error)
            else:
                valid = True
    else:
        valid = True
    return valid

    

def checkSquare(board, row, col, num, checkBoard = False):
    """a function to check 3x3 square for number"""
    global error_messages
    valid = False
    #######################
    # numpy array for each square, referenced by coordinates in dictionary
    square1 = np.array(board)[0:3,0:3]
    square2 = np.array(board)[0:3,3:6]
    square3 = np.array(board)[0:3,6:]
    square4 = np.array(board)[3:6,0:3]
    square5 = np.array(board)[3:6,3:6]
    square6 = np.array(board)[3:6,6:]
    square7 = np.array(board)[6:,0:3]
    square8 = np.array(board)[6:,3:6]
    square9 = np.array(board)[6:,6:]
    square_dict = {(0,0): square1, (0,1): square2, (0,2): square3,
                   (1,0): square4, (1,1): square5, (1,2): square6,
                   (2,0): square7, (2,1): square8, (2,2): square9}
    #######################
    #define square coordinates
    coordinate = (row // 3, col // 3)
    square = square_dict[coordinate]
    if num in square:
        # check squares have valid input
        if checkBoard:
            a =  np.count_nonzero(square == num)
            if a > 1:
                error = str(num) + ' appears '+ str(a) + ' times in a square'
                error_messages.append(error)
            else:
                valid = True
    else:
        valid = True
    return valid
    

    
def find_empty(board):
    """ a function to find an empty square in board, starting from top left """
    for lista in board:
        for num in lista:
            if num == 0:
                return (board.index(lista), lista.index(num))
                break
    return False


            
def check_valid(board, row, col, num, check_board = False):
    """Check a number can go in a square, includes row, column and square checking functions"""
    if check_board:
        checkBoard = True
    else:
        checkBoard = False
    if checkRow(board, row, num, checkBoard) and checkCol(board, col, num, checkBoard) and checkSquare(board, row, col, num, checkBoard):
        return True
    else:
        return False


def check_nums(board):
    """ check all inputs are numbers from 0-9 """
    temp_list = []
    for lista in board:
        for num in lista:
            if num not in range(0,10):
                temp_list.append('false')
    if 'false' in temp_list:
        return False
    else:
        return True        


def solve(incomplete_board):
    """ back tracking algoritm that solves sudoku board (recursive function) """
    board = incomplete_board
    pos = find_empty(board)
    if not pos:
        temp_zipper = list(zip(my_entries, board))
        zipped_list = []
        for item in temp_zipper:
            zipper = list(zip(item[0], item[1]))
            zipped_list.append(zipper)
        for lista in zipped_list:
            for tup in lista:
                tup[0].delete(0,END)
                tup[0].insert(0, tup[1])
        return True
    else:
        row, col = pos[0], pos[1]
    for i in range(1, 10):
        if check_valid(board, row, col, i):
            board[row][col] = i
            if solve(board):
                return True
            else:
                board[row][col] = 0     
    return False
        


def clear_board():
    """ clears GUI board """
    for ob_list in my_entries:
        for ob in ob_list:
            ob.delete(0,END)
        


def get_entries():
    """ makes a game-board from gui inputs, checks all input are integers 1-9 """
    """ Checks that inputs are valid, eg. cant have 2 of the same number in a column. Calls solve function
    if board is valid and creates error window if not"""
    #make board from all entries
    game_board = []
    for row_list in my_entries:
        row = []
        for entry in row_list:
            if entry.get():
                try:
                    row.append(int(entry.get()))
                except:
                    messagebox.showerror(title='Invalid board', message='cannot input non-intergers')
                    break
            else:
                row.append(0)
        game_board.append(row)
        
    #check board for invalid inputs
    validate = [check_valid(game_board, game_board.index(lista), lista.index(num), num, check_board = True)
                for lista in game_board for num in lista if num != 0]
    validate2 = [check_nums(game_board)]
    errors = set(error_messages)
    if 0 in validate or 0 in validate2:
        first = ""
        if len(errors) > 0:
            for element in list(errors):
                first = first + element + '\n'
        if 0 in validate2:
            first = first + 'can only enter numbers 1-9' + '\n'
        messagebox.showerror(title='Invalid board', message=first) 
    else:
        solve(game_board)
          
        
        
        
######################## Tkinter GUI ##########################
        
root = Tk()
root.title('Sudoku solver')
root.configure(bg='black')
root.geometry('500x500')


#make main sudoku board frame
main_frame = Frame(root, bg='black', width=1016, height=300)

#global list variables
error_messages = []
my_entries = []

#make a frame for each of the 81 squares and put an entry widget in each of these frames
for r in range(9):
    row = []
    for c in range(9):
        my_frame = Frame(main_frame, bg='black')
        my_entry = Entry(my_frame, font=("Arial 16"), width = 4, justify = 'center')
        my_entry.grid(row=0, column=0, pady=0, ipady = 10)
        row.append(my_entry)
        
        #make every 3rd box have thick border to the side/bottom
        temp_tuple = [[0,1],[0,1]]
        if r % 3 == 2 and r != 8:
            temp_tuple[0] = [0,3]
        if c % 3 == 2 and c != 8:
            temp_tuple[1] = [0,3]
                 
        my_frame.grid(row=r, column=c, pady = tuple(temp_tuple[0]), padx = tuple(temp_tuple[1]))
    my_entries.append(row)
  
#make second frame for 'clear' and 'solve' buttons
second_frame = Frame(root, bg='black', width=1016, height=300)

#make 'clear' and 'solve' buttons
clear = Button(second_frame, text = 'Clear board', font = 'Ariel', command = clear_board)
clear.pack(side = LEFT, padx = 3, ipadx = 75)

solve_button = Button(second_frame, text = 'Solve', font = 'Ariel', command = get_entries)
solve_button.pack(side = LEFT, padx = 3, ipadx = 69)

#pack all frames
main_frame.pack(padx = 1, pady= (5,2))
second_frame.pack(pady = 3)

root.mainloop()