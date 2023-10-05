"""
Author: Brother Keers

This is an example of the Producer-Consumer design pattern. The producer-consumer
pattern is a concurrency pattern that allows two or more threads to safely share
a data structure.

Here we have a real life scenario where you bring a bag of cans into a recycling
center to redeem them for money. The operator (producer) must place the can into
the recycling machine (consumer) for safety reasons, and to insure you do not try 
to cheat the system. In this example the machine can only handle 15 cans at a time
and you brought in 333 cans. The operator will do his/her best to keep feeding the
machine with cans but will not overload it beyond its capacity. As long as the
machine detects cans are present it will keep recycling.

You should think about the following questions and discuss them with your team:

- Why did we have to use 2 semaphores? Could we do this with 1?
"""

import threading
import time
import random

# Include cse 251 common Python files
from cse251 import *

# Setup global variables for demo.
CANS_TO_RECYCLE = 333
MACHINE_CAN_HANDLE = 15

class Recycling_Queue():
    """ This is a custom queue object for this demo. """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= MACHINE_CAN_HANDLE
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Recycling_Operator(threading.Thread):
    """
    A threaded class that represents the operator of the recycling machine. This person is in charge
    of loading your cans into the machine for counting and processing (recycling).
    """

    def __init__(self, can_queue, machine_remaining_spots, cans_loaded_into_machine):
        super().__init__()
        self.can_queue = can_queue
        self.machine_remaining_spots = machine_remaining_spots
        self.cans_loaded_into_machine = cans_loaded_into_machine

    def run(self):
        for i in range(CANS_TO_RECYCLE):
            self.machine_remaining_spots.acquire()
            can_num = i+1 # So the can numbers are not 0 based add 1.
            print(f'Process can #{can_num}')
            self.can_queue.put(can_num)
            self.cans_loaded_into_machine.release()

        self.can_queue.put(None)
        self.cans_loaded_into_machine.release()


class Recycling_Machine(threading.Thread):

    def __init__(self, can_queue, machine_remaining_spots, cans_loaded_into_machine, stats):
        super().__init__()
        self.can_queue = can_queue
        self.machine_remaining_spots = machine_remaining_spots
        self.cans_loaded_into_machine = cans_loaded_into_machine
        self.stats = stats

    def run(self):
        while True:
            self.cans_loaded_into_machine.acquire()
            can = self.can_queue.get()

            if can == None:
                return

            print(f'Recycle can #{can}')

            # Update stats. ??? Index out of bounds error ???
            # >>> Hotfix
            index = self.can_queue.size()
            if (index > 0):
                index -= 1
            # <<< End hotfix.
            self.stats[index] += 1

            self.machine_remaining_spots.release()

            # Pretend to be processing (recycling) this can.
            time.sleep(random.choice([0.01, 0.02, 0.015]))


def main():

    print(f'Preparing to recycle {CANS_TO_RECYCLE} cans.')

    # Track the queues stats. This will let you see how many cans are in the queue on average by count.
    queue_stats = [0] * MACHINE_CAN_HANDLE
    
    # Use a semaphore to track how many cans are loaded for recycling and how many spots are available.
    cans_loaded_into_machine = threading.Semaphore(0)
    machine_remaining_spots  = threading.Semaphore(MACHINE_CAN_HANDLE)

    # Make a queue for the cans to be placed on; this is the machines intake queue.
    can_queue = Recycling_Queue()

    # Get an instance of the needed classes (threads).
    operator = Recycling_Operator(can_queue, machine_remaining_spots, cans_loaded_into_machine)
    machine  = Recycling_Machine(can_queue, machine_remaining_spots, cans_loaded_into_machine, queue_stats)

    # Start the demo; operator and machine.
    operator.start()
    machine.start()

    # Wait for the entire recycling process to finish.
    operator.join()
    machine.join()

    # Done. Show the results.
    print(f'Recycled {CANS_TO_RECYCLE} cans.')
    xaxis = [i for i in range(1, MACHINE_CAN_HANDLE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Recycled: Count VS Queue Size', x_label='Queue Size', y_label='Count')


# Protect the call to the main function.
if __name__ == '__main__':
    main()