"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: Kyle Parks

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 1        # Number of retrieve_threads
#TODO set to 4
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(log, q, sem):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue

        sem.acquire()

        value_from_queue = q.get()

        # TODO process the value retrieved from the queue

        if value_from_queue != NO_MORE_VALUES:

        # TODO make Internet call to get characters name and log it
            log.write(requests.get(value_from_queue).json())
        #pass
        sem.release()



def file_reader(log, q, sem): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    sem.acquire()
    with open("urls.txt", "r") as file:


        for thign in file:
            q.put(thign.strip())
            sem.release()

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"

    sem.acquire()
    q.put(NO_MORE_VALUES)
    sem.release()



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue

    q = queue.Queue()

    # TODO create semaphore (if needed)

    sem = threading.Semaphore(0)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    filereader = threading.Thread(target=file_reader, args=(log, q, sem))

    rt_threads = []

    for i in range(RETRIEVE_THREADS):
        rt_threads.append(threading.Thread(target= retrieve_thread, args=(log, q, sem)))

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader

    filereader.start()

    for thread in rt_threads:
        thread.start()

    # TODO Wait for them to finish - The order doesn't matter

    filereader.join()

    for thread in rt_threads:
        thread.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()



