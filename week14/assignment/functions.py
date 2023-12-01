"""
Course: CSE 251, week 14
File: functions.py
Author: Kyle Parks

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    family = tree.get_family(family_id)
    wife = family.get_wife()
    tree.add_person(wife)
    depth_fs_pedigree(wife.get_familyid(), tree)
    #TODO thread
    husband = family.get_husband()
    depth_fs_pedigree(husband.get_familyid(), tree)


    # TODO recursive: get mother (recur), then thread(get father)
    # TODO add person to tree
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #for each top-level person, get father, mother
    #TODO how to keep track of who's at the top level
        #TODO add to a queue, go one at a time?
        #TODO New thread for the next guy in queue
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    #TODO Semaphore?
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass