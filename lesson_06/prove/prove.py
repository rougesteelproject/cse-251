"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: Kyle Parks

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'logs/boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'
PIPE_EMPTY = 'pipe-empty'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, sender, marble_count, delay, pipe_empty):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sender = sender
        self.marble_count = marble_count
        self.delay = delay
        self.pipe_empty = pipe_empty

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for marble in range(self.marble_count):
            self.sender.send(random.choice(self.colors))
            time.sleep(self.delay)
        self.sender.send(self.pipe_empty)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, reciever, sender, marbles_per_bag, delay, pipe_empty):
        mp.Process.__init__(self)
        self.reciever = reciever
        self.sender = sender
        self.marbles_per_bag = marbles_per_bag
        self.delay = delay
        self.pipe_empty = pipe_empty

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = Bag()
        while True:
            marble = self.reciever.recv()
            if marble != self.pipe_empty:
                bag.add(marble)
                if bag.get_size() == self.marbles_per_bag:
                    self.sender.send(bag)
                    bag = Bag()
                    time.sleep(self.delay)
            else:
                self.sender.send(self.pipe_empty)
                return

        #while True:
            #while bag.get_size < self.marbles_per_bag:
                #marble = self.reciever.recv()
                #if marble != self.pipe_empty:
                    #bag.add(marble)
                #else:
                    #self.sender.send(self.pipe_empty)
                    #return
            #self.sender.send(bag)
            #bag = Bag()
            #time.sleep(self.delay)

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, reciever, sender, delay,  pipe_empty, gifts_created):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.reviever = reciever
        self.sender = sender
        self.delay = delay
        self.pipe_empty = pipe_empty
        self.gifts_created = gifts_created


    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.reviever.recv()
            if bag != self.pipe_empty:
                self.sender.send(Gift(random.choice(self.marble_names), bag))
                self.gifts_created.value += 1 #TODO value()?
                time.sleep(self.delay)
            else:
                self.sender.send(self.pipe_empty)
                return


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, reciever, pipe_empty, delay, box_filename):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.reciever = reciever
        self.delay = delay
        self.pipe_empty = pipe_empty
        self.box_filename = box_filename

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.box_filename, "w") as box_file:
            
            while True:
                gift = self.reciever.recv()
                if gift != self.pipe_empty:
                    box_file.write(f'Created - {datetime.now().time()}: {gift.__str__()} \n')
                    time.sleep(self.delay)
                else:
                    return


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')


def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    parent_creator, child_bagger = mp.Pipe()
    parent_bagger, child_assembler = mp.Pipe()
    parent_assembler, child_wrapper = mp.Pipe()
    # TODO create variable to be used to count the number of gifts

    number_of_gifts = mp.Value("i",0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator = Marble_Creator(parent_creator, settings[MARBLE_COUNT], settings[CREATOR_DELAY], settings[PIPE_EMPTY])
    bagger = Bagger(child_bagger, parent_bagger, settings[NUMBER_OF_MARBLES_IN_A_BAG], settings[BAGGER_DELAY], settings[PIPE_EMPTY])
    assembler = Assembler(child_assembler, parent_assembler, settings[ASSEMBLER_DELAY], settings[PIPE_EMPTY], number_of_gifts)
    wrapper = Wrapper(child_wrapper, settings[PIPE_EMPTY], settings[WRAPPER_DELAY], BOXES_FILENAME)

    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()
    # TODO add code here

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(number_of_gifts.value)

if __name__ == '__main__':
    main()
