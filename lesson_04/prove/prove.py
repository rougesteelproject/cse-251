"""
Course: CSE 251 
Lesson: L04 Prove
File:   prove.py
Author: <Add name here>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Complete the assignments TODO sections and DO NOT edit parts you were told to leave alone.
- Review the full instructions in Canvas; there are a lot of DO NOTS in this lesson.
"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, q, factory_spaces, available_cars):
        super().__init__()
        self.q = q
        self.factory_spaces = factory_spaces
        self.available_cars = available_cars

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            
            self.factory_spaces.acquire()
            self.q.put(Car())
            
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """
            self.available_cars.release()
            

        # signal the dealer that there there are not more cars
        self.q.put("NO_MORE_CARS")
        self.available_cars.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, q, factory_spaces, available_cars, queue_stats):
        super().__init__()
        
        self.q = q
        self.factory_spaces = factory_spaces
        self.available_cars = available_cars
        self.cars = []
        self.queue_stats = queue_stats

    def run(self):
        while True:
            
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.available_cars.acquire()

            car = self.q.get()

            
            if car != "NO_MORE_CARS":
                #car.display()
                self.cars.append(car)
                self.queue_stats[self.q.size()] += 1
            else:
                return
            
            self.factory_spaces.release()

            #decrease dealer semaphore, increase factory semaphore

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    factory_spaces = threading.Semaphore(MAX_QUEUE_SIZE)
    #THERE's space in the queue, you can produce a car
    available_cars = threading.Semaphore(0)
    #THere's a car in the queueue, you can pull a car

    #Create queue251

    q = Queue251()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    #right after you take the car off the queue, check the queue size, and add one to it

    #create your one factory

    fact_1 = Factory(q, factory_spaces,available_cars)

    #create your one dealership

    dealer_1 = Dealer(q,factory_spaces, available_cars, queue_stats)

    log.start_timer()

    #Start factory and dealership

    fact_1.start()
    dealer_1.start()

    #Wait for factory and dealership to complete

    fact_1.join()
    dealer_1.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()