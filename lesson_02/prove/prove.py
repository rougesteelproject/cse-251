"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

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

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
lock = threading.Lock()


# TODO Add your threaded class definition here
class ThreadedClass(threading.Thread):
  def __init__(self, url):
    super().__init__()
    self.url = url
    self.response = {}

# TODO Add any functions you need here
  def run(self):
    global call_count
    self.response = requests.get(self.url).json()
    lock.acquire()
    call_count += 1
    lock.release()


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

  #Characters

  characters = film_getter.response["characters"]

  print(f'Characters: {len(characters)}')
  
  threads = []

  character_names = []

  for character in characters:
    thread = ThreadedClass(character)
    threads.append(thread)
    thread.start()
    
  for thread in threads:
    thread.join()
    character_names.append(thread.response["name"])

  character_names.sort()
  
  print(character_names)

  #Planets

  planets = film_getter.response["planets"]

  print(f'Planets: {len(planets)}')
  
  threads = [None] * len(planets)

  planet_names = []

  for i in range(len(planets)):
    threads[i] = ThreadedClass(planets[i])
    threads[i].start()
    
  for i in range(len(threads)):
    threads[i].join()
    planet_names.append(threads[i].response["name"])
  
  planet_names.sort()

  print(planet_names)

  #Starships

  starships = film_getter.response["starships"]

  print(f'Starships: {len(starships)}')
  
  threads = [None] * len(starships)

  starship_names = []

  for i in range(len(starships)):
    threads[i] = ThreadedClass(starships[i])
    threads[i].start()
    
  for i in range(len(threads)):
    threads[i].join()
    starship_names.append(threads[i].response["name"])
  
  starship_names.sort()
  
  print(starship_names)

  #Species

  species = film_getter.response["species"]

  print(f'Species: {len(species)}')
  
  threads = [None] * len(species)

  species_names = []

  for i in range(len(species)):
    threads[i] = ThreadedClass(species[i])
    threads[i].start()
    
  for i in range(len(threads)):
    threads[i].join()
    species_names.append(threads[i].response["name"])
  
  species_names.sort()
  
  print(species_names)

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()