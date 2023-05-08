#!/usr/bin/python3

# COMP3311 22T3 Assignment 2
# Print a list of countries where a named movie was released

import sys
import psycopg2
import helpers
from helpers import getYear

### Globals

db = None
usage = f"Usage: {sys.argv[0]} Year"

### Command-line args

if len(sys.argv) < 2:
   print(usage)
   exit(1)

# process the command-line args ...
year = sys.argv[1]
### Queries
qry = """
   select count(*) as total, mg.genre
   from MovieGenres mg
   join Movies m on m.id = mg.movie
   where m.year = %s
   group by mg.genre
   order by total desc, mg.genre 
   fetch first 10 rows with ties
   ;
"""
### Manipulating database

try:
   # your code goes here
   db = psycopg2.connect("dbname=ass2")
   cur = db.cursor()
   if not getYear(year):
      print("Invalid year")
      exit(1)

   cur.execute(qry, [year])
   getGenre = cur.fetchone()
   if not getGenre:
      print("No movies")
      exit(1)
   cur.execute(qry, [year])
   getMovie = cur.fetchall()
   for m in getMovie:
      if m[0] < 100:
         print(f" {m[0]} {m[1]}")
      else: 
         print(f"{m[0]} {m[1]}")


except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()

