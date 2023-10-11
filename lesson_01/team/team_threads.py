"""
Course: CSE 251 
Lesson: L01 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review and follow the team activity instructions (INSTRUCTIONS.md)
"""

from datetime import datetime, timedelta
import threading

# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0
lock = threading.Lock()

def is_prime(n):
    global numbers_processed
    lock.acquire()
    numbers_processed += 1
    lock.release()

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

def find_primes(start, range_count):
    global prime_count
    for i in range(start, range_count):
        
        if is_prime(i):
            lock.acquire()
            prime_count += 1
            lock.release()
            #print(i, end=', ', flush=True)
        


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads

    start = 10000000000
    range_count = 100000
    number_of_threads = 10
    interval = int(range_count / number_of_threads)

    threads = [None] * number_of_threads

    for i in range(number_of_threads):
        threads[i] = threading.Thread(target=find_primes, args=(start + (interval * i), start + (interval * (i+ 1)),))
        threads[i].start()
    
    for i in range(len(threads)):
        threads[i].join()

    #print(flush=True)

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')

