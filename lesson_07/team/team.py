"""
Course: CSE 251 
Lesson: L07 Team
File:   team.py
Author: Kyle Parks

Purpose: Retrieve Star Wars details from a server.

Instructions:

1) Make a copy of your lesson 2 prove assignment. Since you are  working in a team for this
   assignment, you can decide which assignment 2 program that you will use for the team activity.

2) Convert the program to use a process pool and use apply_async() with a callback function to
   retrieve data from the Star Wars website. Each request for data must be a apply_async() call.

3) You can continue to use the Request_Thread() class that makes the call to the server.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

chars = []
planets = []
ships = []
vech = []
species = []


# TODO Add your threaded class definition here
class ThreadedClass(threading.Thread):
  def __init__(self, url: str, data: list):
    super().__init__()
    self.url = url
    self.data = data

# TODO Add any functions you need here
  def run(self):
    global call_count
    self.response = requests.get(self.url).json()
    call_count += 1

def get_url(url, flush = True):
  results = []

  getter = ThreadedClass(url, results)

  getter.start()
  getter.join()

  return getter.data[0]


def main():
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')

  # TODO Retrieve Top API urls
  urls = requests.get(TOP_API_URL).json()
  # TODO Retrieve Details on film 6
  film_getter = ThreadedClass(urls['films'] + '6')

  film_getter.start()
  film_getter.join()

  #print(film_getter.response)

  print(f'Title : {film_getter.response["title"]}')
  print(f'Director: {film_getter.response["director"]}')
  print(f'Producer: {film_getter.response["producer"]}')
  print(f'Released: {film_getter.response["release_date"]}')

  pool = mp.Pool()

  for character in film_getter.response["characters"]:
    pool.apply_async(get_url, args=(character,), callback=cb_char)
  for planet in film_getter.response["planets"]:
    pool.apply_async(get_url, args=(planet,), callback=cb_planet)
  for starship in film_getter.response["starships"]:
    pool.apply_async(get_url, args=(starship,), callback=cb_starship)
  for specie in film_getter.response["species"]:
    pool.apply_async(get_url, args=(specie,), callback=cb_species)
  
  pool.close()
  pool.join()

  print_film_details()

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()