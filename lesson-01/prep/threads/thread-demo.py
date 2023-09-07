"""
Author: Brother Keers
Copyright 2023 Brigham Young University Idaho.

This script demonstrates the basics of threading in python. You should think
about the following questions and discuss them with their team:

- What can you infer from the output?
- Why do the results differ when the system is under load?
- How could we improve this code? *hint* Loop(s).
"""

import random
import threading
import time

def append_letter(ltr_list, ltr, times):
    """ Add a letter to a list of letters `times` amount of times. """

    for _ in range(0,times):
        ltr_list.append(ltr)

def append_letter_simulate_load(ltr_list, ltr, times):
    """ Add a letter to a list of letters `times` amount of times. """

    for _ in range(0,times):
        ltr_list.append(ltr)
        # Sleep this script for a random amount of time to simulate computer load.
        time.sleep(random.random() * 0.3 + 0.1)

def append_letter_with_lock(ltr_list, ltr, times, lock):
    """ Add a letter to a list of letters `times` amount of times. """

    lock.acquire()
    for _ in range(0,times):
        ltr_list.append(ltr)
    lock.release()

def print_section_title(title):
    """ Print text with horizontal rule below it that matches its length """
    print(f'{title}\n{"-" * len(title)}')

# [ EXAMPLE 1 ]
# Print the letters using threads.
letters = []

t1 = threading.Thread(target=append_letter, args=(letters, 'A', 10))
t2 = threading.Thread(target=append_letter, args=(letters, 'B', 10))
t3 = threading.Thread(target=append_letter, args=(letters, 'C', 10))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print_section_title('No lock and no load:')
for i, ltr in enumerate(letters):
    print(f'{ltr} ', end='')
    if ((i + 1) % 10 == 0):
        print()

print()

# [ EXAMPLE 2 ]
# Print the letters using threads under "heavy" computer load.

letters = []

t1 = threading.Thread(target=append_letter_simulate_load, args=(letters, 'A', 10))
t2 = threading.Thread(target=append_letter_simulate_load, args=(letters, 'B', 10))
t3 = threading.Thread(target=append_letter_simulate_load, args=(letters, 'C', 10))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print_section_title('No lock and simulated load:')
for i, ltr in enumerate(letters):
    print(f'{ltr} ', end='')
    if ((i + 1) % 10 == 0):
        print()

print()

# [ EXAMPLE 3 ]
# Print the letters using threads with locks.

letters = []

lock = threading.Lock()

t1 = threading.Thread(target=append_letter_with_lock, args=(letters, 'A', 10, lock))
t2 = threading.Thread(target=append_letter_with_lock, args=(letters, 'B', 10, lock))
t3 = threading.Thread(target=append_letter_with_lock, args=(letters, 'C', 10, lock))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print_section_title('Lock in the correct spot:')
for i, ltr in enumerate(letters):
    print(f'{ltr} ', end='')
    if ((i + 1) % 10 == 0):
        print()