#!/usr/bin/python3

# COMP3311 22T3 Assignment 2
# Print a list of movies directed by a given person

import sys
import psycopg2

### Globals

db = None
usage = f"Usage: {sys.argv[0]} FullName"

### Command-line args

if len(sys.argv) < 2:
   print(usage)
   exit(1)

# process the command-line args ...
name = sys.argv[1]

### Queries
qry1 = """
    select p.id
    from Principals pr
    join People p on pr.person = p.id
    where pr.job = 'director' and p.name = %s
    order by p.id
    ;
"""

qry2 = """
   select m.title, m.year
   from Movies m
   join Principals pr on m.id = pr.movie
   where pr.job = 'director' and pr.person = %s
   order by m.year
   ;
"""

qryPersonExist = """
    select *
    from People p
    where p.name = %s
    ;
"""
### Manipulating database

try:
    # your code goes here
    db = psycopg2.connect("dbname = ass2")
    cur = db.cursor()

    # check if the person exist
    cur.execute(qryPersonExist, [name])
    exist = cur.fetchall()
    personExist = 0
    if not exist:
        print("No such person")
        exit(0)
    else:
        personExist = len(exist)

    cur.execute(qry1,[name])
    id = cur.fetchall()
    if not id and (personExist > 1):
        print(f"None of the people called {name} has directed any films")
        exit(0)
    if not id and (personExist == 1):
        print(f"{name} has not directed any movies")
        exit(0)

    cur.execute(qry2,[id[0][0]])
    movies = cur.fetchall()
    for movie in movies:
        print(f"{movie[0]} ({movie[1]})")


except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()


