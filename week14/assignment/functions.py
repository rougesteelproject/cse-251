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

Checking if a child existed before trying to request and then add them to the tree
reduced the amount of server calls.
I went from ~60 seconds to ~7 by having the "grandparent" threads start and end at the same time,
instead of joining one before starting the other, and by making the "wife side" a thread, also.


Describe how to speed up part 2

The program ran much faster as a pool of workers eating from the queue, rather than a
"while queue" loop.


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it

    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()

    family = Family(request.get_response())
    tree.add_family(family)

    child_requests = []
    for child in family.get_children():
        if not tree.does_person_exist(child):
            child_request = Request_thread(f'{TOP_API_URL}/person/{child}')
            child_requests.append(child_request)
            child_request.start()

    for child_request in child_requests:
        child_request.join()

    for child_request in child_requests:
        tree.add_person(Person(child_request.get_response()))

    wife_request = Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')
    wife_request.start()
    wife_request.join()

    wife = Person(wife_request.get_response())

    tree.add_person(wife)
    
    #recursive: get mother (recur), then thread(get father)

    husband_request = Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')
    husband_request.start()
    husband_request.join()

    husband = Person(husband_request.get_response())
    tree.add_person(husband)

    grandparents = husband.get_parentid()

    inlaws = wife.get_parentid()

    if inlaws != None:
        wife_dfs = threading.Thread(target = depth_fs_pedigree, args=(inlaws, tree,))
        wife_dfs.start()

    if grandparents != None:
        husband_dfs = threading.Thread(target = depth_fs_pedigree, args = (grandparents, tree,))
        husband_dfs.start()
        
    if grandparents != None:
        husband_dfs.join()
    if inlaws != None:
        wife_dfs.join()

def worker(q, tree):
    while True:
        next_family = q.get()

        request = Request_thread(f'{TOP_API_URL}/family/{next_family}')
        request.start()
        request.join()

        family = Family(request.get_response())
        tree.add_family(family)

        child_requests = []
        for child in family.get_children():
            if not tree.does_person_exist(child):
                child_request = Request_thread(f'{TOP_API_URL}/person/{child}')
                child_requests.append(child_request)
                child_request.start()

        for child_request in child_requests:
            child_request.join()

        for child_request in child_requests:
            tree.add_person(Person(child_request.get_response()))

        husband_request = Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')
        husband_request.start()
        husband_request.join()

        husband = Person(husband_request.get_response())
        #print(husband)
        tree.add_person(husband)

        wife_request = Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')
        wife_request.start()
        wife_request.join()

        wife = Person(wife_request.get_response())
        #print(wife)
        tree.add_person(wife)

        grandparents = husband.get_parentid()
        if grandparents != None:
            q.put(grandparents)

        inlaws = wife.get_parentid()
        if inlaws != None:
            q.put(inlaws)

        q.task_done()


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval

    breadth_queue = queue.Queue()
    breadth_queue.put(family_id)

    for i in range(8):
        threading.Thread(target=worker, args=(breadth_queue,tree), daemon=True).start()

    breadth_queue.join()
    # TODO - Printing out people and families that are retrieved from the server will help debugging

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    #TODO Semaphore?
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass