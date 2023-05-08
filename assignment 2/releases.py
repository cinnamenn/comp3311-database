#!/usr/bin/python3

# COMP3311 22T3 Assignment 2
# Print a list of countries where a named movie was released

import sys
import psycopg2
import helpers
from helpers import getYear

### Globals

db = None
usage = f"Usage: {sys.argv[0]} 'MovieName' Year"

### Command-line args

if len(sys.argv) < 3:
   print(usage)
   exit(1)

movie = sys.argv[1]
year = sys.argv[2]

qryMovieExist = """
   select m.*
   from Movies m
   where m.title = %s and m.year = %s
   ;
"""

qry = """
   select c.name
   from Movies m
   join ReleasedIn r on m.id =  r.movie
   join countries c on c.code = r.country
   where m.title = %s and m.year = %s
   order by c.name asc
   ;
"""

# process the command-line args ...

### Queries

### Manipulating database

try:
   # your code goes here
   db = psycopg2.connect("dbname = ass2")
   cur = db.cursor()
   if not getYear(year):
      print("Invalid year")
      exit(1)

   cur.execute(qryMovieExist,(movie,year))
   getMovie = cur.fetchone()
   # check the movie in the database
   if not getMovie:
      print("No such movie")
      exit(1)

   cur.execute(qry,(movie,year))
   lists = cur.fetchall()
   # movie exist but no release
   if not lists:
      print("No releases")
      exit(1)

   for m in lists:
      print(f"{m[0]}")  
   
except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()

