"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Kyle Parks

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 3
WRITERS = 3


WRITE_POSITION_INDEX = BUFFER_SIZE #Stores a value 0-BUFFER, stored at BUFFER+1 (out of the buffer)
NEXT_VALUE_INDEX = BUFFER_SIZE + 1 #LAST IN, LAST OUT
READ_POSITION_INDEX = BUFFER_SIZE + 2 #Stores a value 0-BUFFER, stored at BUFFER+3 (out of the buffer)
RESULT_INDEX = BUFFER_SIZE + 3
STOP_VAL = -1

def writer_process(end_value, buffer_lock, reading_sem, writing_sem, shared_list):
    stop = False
    while not stop:
    # While there is data to write, write it:
      # HINT: You will need to acquire() the writer semaphore and the buffer lock.
      writing_sem.acquire()
      buffer_lock.acquire()

      #print(f'Sending: {shared_list[NEXT_VALUE_INDEX]}')

      # Write the next value to the shared list (circular buffer) or stop if there are no more values.
      if shared_list[NEXT_VALUE_INDEX] > end_value:
        next_value = STOP_VAL
      else:
        next_value = shared_list[NEXT_VALUE_INDEX] #The Value to write, which is stored outside the buffer at NVI
      next_index = shared_list[WRITE_POSITION_INDEX]
      shared_list[next_index] = next_value #Writing next_value at next_index

      if next_value == STOP_VAL: #If we just wrote STOP, then stop
        stop = True
      else:
        shared_list[NEXT_VALUE_INDEX] += 1 #Increment the value stored at NVI
        shared_list[WRITE_POSITION_INDEX] = (shared_list[WRITE_POSITION_INDEX] + 1) % BUFFER_SIZE
        #write to shared list
      # HINT: Uses modulus (%) to always call the correct index number. (cycles 0-9, 10=0)

      # HINT: You will need to release() the buffer lock and reading semaphore.
      buffer_lock.release()
      reading_sem.release()    
      
def reader_process(buffer_lock, reading_sem, writing_sem, shared_list):
  stop = False
  while not stop:
  #While there is data to read, read it:
    #HINT: You will need to acquire() the reading semaphore and the buffer lock.
    reading_sem.acquire()
    buffer_lock.acquire()
    #Read (print) the next value from the shared list (circular buffer) or stop if stop flag was received.
    next_index = shared_list[READ_POSITION_INDEX]
    next_value = shared_list[next_index]
    if next_value == STOP_VAL:
      stop = True
    else:
      shared_list[RESULT_INDEX] = next_value
      print(next_value, end=', ', flush=True)
      shared_list[READ_POSITION_INDEX] = (shared_list[READ_POSITION_INDEX] + 1) % BUFFER_SIZE
    #HINT: Uses modulus (%) to always call the correct index number.

    # HINT: You will need to release() the buffer lock and writing semaphore.
    buffer_lock.release()
    writing_sem.release()

def main():
    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # DONE - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))

    #         A flat list treated like a circle

    shared_list = smm.ShareableList([0] * (BUFFER_SIZE + 4))

    # DONE - Create any lock(s) or semaphore(s) that you feel you need
    buffer_lock = mp.Lock()
    writing_sem = mp.Semaphore(BUFFER_SIZE)
    reading_sem = mp.Semaphore(0)

    end_value = items_to_send

    # DONE - create reader and writer processes
    readers = [mp.Process(target=reader_process, args=(buffer_lock, reading_sem, writing_sem, shared_list,)) for _ in range(READERS)]
      
    writers = [mp.Process(target = writer_process, args = (end_value, buffer_lock, reading_sem, writing_sem, shared_list,)) for _ in range(WRITERS)]

    # DONE - Start the processes and wait for them to finish
    for reader in readers:
      reader.start()

    for writer in writers:
      writer.start()

    for reader in readers:
      reader.join()

    for writer in writers:
      writer.join()

    print(f'{items_to_send} values sent')

    # DONE - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f'{shared_list[RESULT_INDEX]} values received')

    smm.shutdown()

if __name__ == '__main__':
    main()