#!/usr/bin/python3

# COMP3311 22T3 Assignment 2
# Print a list of character roles played by an actor/actress

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
name  = sys.argv[1]

### Queries
qry1 = """
   select p.id
   from People p
   where p.name = %s
   order by p.id
   ;
"""

qry2 = """
   select pl.role, m.title, m.year
   from People p
   join Principals pr on pr.person = p.id
   join Movies m on m.id = pr.movie
   join Playsrole pl on pl.inMovie = pr.id
   where (p.id = %s) and (pr.job = 'self' or pr.job = 'actor' or pr.job = 'actress')
   order by m.year, m.title, pl.role
   ;
"""

### Manipulating database
db = psycopg2.connect("dbname=ass2")
cur = db.cursor()

try:
   # your code goes here
   cur.execute(qry1, [name])
   person = cur.fetchall()

   countPerson = 0
   if not person:
      print("No such person")
      exit(0)
   else:
      countPerson = len(person)

   for p in person:
      cur.execute(qry2,person[0])

   roles = cur.fetchall()
   numRoles = len(roles)

   if countPerson == 1 :
      if numRoles == 0:
         print("No acting roles")
      else:
         for r in roles:
            print(f"{r[0]} in {r[1]} ({r[2]})")

   else : 
      counter = 1
      for p in person:
         cur.execute(qry2,[p[0]])
         roles = cur.fetchall()
         numRoles = len(roles)
         print(f"{name} #{counter}")
         counter +=1
         if numRoles == 0: 
            print(f"No acting roles")
         else:
            for r in roles:
               print(f"{r[0]} in {r[1]} ({(r[2])})")
               
     
except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()

