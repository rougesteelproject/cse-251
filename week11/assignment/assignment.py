"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}\n')
    time.sleep(random.uniform(0, 1))

def cleaner_function(id, start_time, room_occupied, cleaned_count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while start_time + TIME > time.time():
        cleaner_waiting()
        with room_occupied:
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id)
            cleaned_count.value += 1
            print(STOPPING_CLEANING_MESSAGE)
        
    print(f'Cleaner {id}: Time\'s up!')

def guest_function(id, start_time, room_occupied, partying, occupancy, party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() < start_time + TIME:
        guest_waiting()
        
        with partying:
            occupancy.value += 1
            if occupancy.value == 1:
                room_occupied.acquire()
                print(STARTING_PARTY_MESSAGE)

        guest_partying(id, occupancy.value)
            
        with partying:          

            if occupancy.value == 1:
                print(STOPPING_PARTY_MESSAGE)
                party_count.value += 1
                room_occupied.release()
                
            occupancy.value -= 1


    print(f'Guest {id}: Time\'s up!')

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    room_occupied = mp.Lock()
    partying = mp.Lock()
    occupancy = mp.Value('i')

    cleaned_count = mp.Value('i')
    party_count = mp.Value('i')
    # TODO - add any arguments to cleaner() and guest() that you need

    cleaners = [mp.Process(target = cleaner_function, args = (id_number, start_time, room_occupied, cleaned_count)) for id_number in range(CLEANING_STAFF)]
    guests = [mp.Process(target=guest_function, args=(id_number, start_time, room_occupied, partying ,occupancy, party_count)) for id_number in range(HOTEL_GUESTS)]

    for cleaner in cleaners:
        cleaner.start()

    for guest in guests:
        guest.start()

    for cleaner in cleaners:
        cleaner.join()

    for guest in guests:
        guest.join()


    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

