"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: Kyle Parks

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(file_path, pipe_parent,SENDER_DONE_SIGNAL): # Parent
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(file_path, "r") as file:
        first_line = True
        for line in file:
            if not first_line:
                pipe_parent.send("\n")
            line = line.split()
            first_word = True
            for i in range(len(line)):
                if not first_word:
                    pipe_parent.send(" ")
                pipe_parent.send(line[i])
                first_word = False
            first_line = False
        pipe_parent.send(SENDER_DONE_SIGNAL)
        pipe_parent.close()


def receiver(new_file_path, pipe_child, items_sent, sender_done_signal): # Child
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(new_file_path, "w") as new_file:
        while True:
            line = pipe_child.recv()
            if line == sender_done_signal:
                return
            else:
                new_file.write(line)
                items_sent.value += 1


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # DONE create a pipe 

    pipe_parent, pipe_child = mp.Pipe()
    
    # DONE create variable to count items sent over the pipe

    items_sent = Value('i',0)

    SENDER_DONE_SIGNAL = "NO_MORE_LINES"

    # DONE create processes
    file_sender = Process(target=sender, args=(filename1, pipe_parent, SENDER_DONE_SIGNAL))
    file_reciever = Process(target=receiver, args=(filename2, pipe_child, items_sent, SENDER_DONE_SIGNAL)) 

    log.start_timer()
    start_time = log.get_time()

    # DONE start processes
    file_sender.start()
    file_reciever.start()
    
    # DONE wait for processes to finish
    file_sender.join()
    file_reciever.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content ({items_sent.value} items) = {stop_time - start_time}: ')
    log.write(f'items / second = {items_sent.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')