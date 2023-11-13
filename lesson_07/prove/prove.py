"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: Kyle Parks

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

TODO:

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.

I HAVE 12 CORES, so I want to use between 12 and 24. Evenly split, that's 5 per pool, with 4 to play with. ~40s with 2 each, ~30 with 5 each.
Finding the word is IO bound because it needs to open and close the file, so it won't benefit with a bigger pool.
I dropped it down to 1, leaving a total of 7 to allocate,
but after experimentation, the "words" pool on 1 process was 20s slower than on 4. 
If I want to fine-tune it, I'd take more from the "upper" pool, since it seems like a simple function.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment

PRIME_POOL_SIZE = 1
WORD_POOL_SIZE  = 1
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 1
NAME_POOL_SIZE  = 1

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return is_prime(value)


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        datafile = f.readlines()
    for line in datafile:
        if word in line:
            return True
    return False


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return text.upper()


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    return sum(range(start_value, end_value + 1))


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response =  requests.get(url)
    if response.status_code == 200:
        return response.json()['name']
    else:
        return response.status_code

def prime_callback(prime):
    result_primes.append(prime)

def word_callback(result):
    result_words.append(result)

def upper_callback(result):
    result_upper.append(result)

def sum_callback(result):
    result_sums.append(result)

def name_callback(name):
    result_names.append(name)


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools

    pool_primes = mp.Pool(5)
    pool_words = mp.Pool(5)
    pool_upper = mp.Pool(4)
    pool_sums = mp.Pool(5)
    pool_names = mp.Pool(5)

    # TODO you can change the following
    # TODO start and wait pools
    
    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_primes.apply_async(task_prime, args=(task['value'],),callback=prime_callback)
        elif task_type == TYPE_WORD:
            pool_words.apply_async(task_word, args=(task['word'],), callback=word_callback)
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_word, args=(task['text'],), callback=upper_callback)
        elif task_type == TYPE_SUM:
            pool_sums.apply_async(task_sum, args=(task['start'], task['end'],), callback=sum_callback)
        elif task_type == TYPE_NAME:
            pool_names.apply_async(task_name, args=(task['url'],), callback=name_callback)
        else:
            log.write(f'Error: unknown task type {task_type}')

    pool_primes.close()
    pool_words.close()
    pool_upper.close()
    pool_sums.close()
    pool_names.close()

    pool_primes.join()
    pool_words.join()
    pool_upper.join()
    pool_sums.join()
    pool_names.join()

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')

    print(os.cpu_count())

if __name__ == '__main__':
    main()