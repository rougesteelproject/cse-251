"""
Course: CSE 251 
Lesson: L02 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
import threading
from typing import Any
import requests
from requests.exceptions import HTTPError, ReadTimeout
import json

# Include cse 251 common Python files
from cse251 import *

# Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}

    def run(self):
        try: 
            self.response = requests.get(self.url).json()
        
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ReadTimeout as read_timeout:
            print(f'Connection Error: {read_timeout}')

    #make api call to deckofcardsapi.com

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        #add call to reshuffle
        thread_shuffle = Request_thread(f'https://www.deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        thread_shuffle.start()
        thread_shuffle.join()
        #if (thread_shuffle.response['shuffled']):
        #    print("Deck Shuffled")


    def draw_card(self):
        thread_draw = Request_thread(f'https://www.deckofcardsapi.com/api/deck/{self.id}/draw/?count=1')
        thread_draw.start()
        thread_draw.join()
        self.remaining -= 1
        return f'{thread_draw.response["cards"][0]["value"]} of {thread_draw.response["cards"][0]["suit"]}'
        #add call to get a card

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '0wakjt3d1n0k'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<
