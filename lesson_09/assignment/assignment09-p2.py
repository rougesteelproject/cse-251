"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Kyle Parks

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different colour by calling get_colour().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

Right now, it's setting the final path as a global after each maze, but that's just
a proof of concept. It could return it or something.

Why would it work?

If a thread finds the exit, it'll have the whole path up to that point.
There's probably a way to do this that's easier on memory.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
colour = (0, 0, 255)
colourS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_colour_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED
path = []

def get_colour():
    """ Returns a different colour when called """
    global current_colour_index
    if current_colour_index >= len(colourS):
        current_colour_index = 0
    colour = colourS[current_colour_index]
    current_colour_index += 1
    return colour

def branch(maze, position, temp_path, colour):
    global stop

    temp_path.append(position)
    row, col = position

    maze.move(row, col, colour)
    
    if maze.at_end(row, col):
        global path
        path = temp_path
        
        stop = True

    valid_moves = [move for move in maze.get_possible_moves(row,col) if maze.can_move_here(move[0], move[1])]
    
    for move in valid_moves:
        new_colour = colour
        if valid_moves.index(move) != 0:
            branch_thread = threading.Thread(target= branch, args = (maze, move, temp_path, get_colour()))
            branch_thread.start()
        else:
            branch(maze, move, temp_path, colour)
    stop = True

    
            

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    global colour
    stop = False

    branch(maze, maze.get_start_pos(), [], colour)


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()