#!/usr/bin/python3

# COMP3311 22T3 Assignment 2
# Print info about one movie; may need to choose

import sys
import psycopg2
import helpers

### Globals

db = None
usage = f"Usage: {sys.argv[0]} 'PartialMovieName'"

### Command-line args

if len(sys.argv) < 2:
   print(usage)
   exit(1)

# process the command-line args ...
movie = sys.argv[1].lower()
pattern = f"%{movie}%"
### Queries

qryMovieExist = """
   select m.title, m.year, m.id
   from Movies m
   where lower(title) like %s
   order by m.title, m.year
   ;
"""

#qry only with actor and actress
qryAct = """
   select p.name, pr.job, pr.id
   from Principals pr 
   join People p on p.id = pr.person
   where pr.movie = %s 
   order by pr.ord
   ;
"""

#qry except actor and actress
qryRole = """
   select role
   from Playsrole
   where inMovie = %s
   ;
"""

### Manipulating database
db = psycopg2.connect("dbname=ass2")
cur = db.cursor()

try:
   cur.execute(qryMovieExist, [pattern])
   movies = cur.fetchall()

   numMovie = 0
   if not movies:
      print(f"No movie matching: '{sys.argv[1]}'")
      exit(0)
   else:
      numMovie = len(movies)

   # only 1 movie match
   if numMovie == 1: 
      for m in movies:
         print(f"{m[0]} ({m[1]})")
         cur.execute(qryAct, [m[2]])
         actPri = cur.fetchall()
         numRoles = len(actPri)
         for a in actPri:
            if(a[1] == "self" or a[1] == "actor" or a[1] == "actress"):
               cur.execute(qryRole, [a[2]])
               roles = cur.fetchone()
               if not roles:
                  print(f"{a[0]} plays ???")
               else:
                  print(f"{a[0]} plays {roles[0]}")
            else:
               print(f"{a[0]}: {a[1]}")
   else :
      counter = 0
      for m in movies:
         counter += 1
         print(f"{counter}. {m[0]} ({m[1]})")
         cur.execute(qryAct, [m[2]])
         actPri = cur.fetchall()
         numRoles = len(actPri)

      chooseMovie = input("Which movie? ")
      counter = 0
      for m in movies:
         counter += 1
         if (counter == int(chooseMovie)):
            print(f"{m[0]} ({m[1]})")
            cur.execute(qryAct, [m[2]])
            actPri = cur.fetchall()
            numRoles = len(actPri)
            for a in actPri:
               if(a[1] == "self" or a[1] == "actor" or a[1] == "actress"):
                  cur.execute(qryRole, [a[2]])
                  roles = cur.fetchone()
                  if not roles:
                     print(f"{a[0]} plays ???")
                  else:
                     print(f"{a[0]} plays {roles[0]}")
               else:
                  print(f"{a[0]}: {a[1]}") 
         #else:
               #print("No such movie")

except Exception as err:
   print("DB error: ", err)

finally:
   if db:
      db.close()

