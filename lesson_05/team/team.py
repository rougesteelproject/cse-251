"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: Kyle Parks

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

import queue

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def read_thread(file, q):
    with open(file, 'r') as f:
        for thign in f:
            q.put(thign.strip())

# TODO create prime_process function
def prime_process(q, primes):
    while True:
        try :
            value = q.get(False)
            if is_prime(int(value)):
                primes.append(value)
        except queue.Empty:
            return



def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    # Create the data file for this demo if it does not already exist.
    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures

    q = mp.Queue()

    primes = mp.Manager().list()

    #barrier = mp.Barrier(PRIME_PROCESS_COUNT)

    # TODO create reading thread

    reading_thread = threading.Thread(target=read_thread, args=(filename, q))

    # TODO create prime processes

    prime_processes = [mp.Process(target=prime_process, args=(q, primes)) for i in range(PRIME_PROCESS_COUNT)]

    # TODO Start them all

    reading_thread.start()

    for process in prime_processes:
        process.start()

    # TODO wait for them to complete

    reading_thread.join()

    for process in prime_processes:
        process.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
