from fuzzywuzzy import process
import sqlite3

def isBlacklisted(school):
   return _matches(school, "blacklist")

def isGreenlisted(school):
   return _matches(school, "greenlist")

def closestBlacklistSchool(school):
   return _closestMatchSchool(school, "blacklist")

def closestGreenlistSchool(school):
   return _closestMatchSchool(school, "greenlist")

def _matches(school, list_type):
   return _closestMatchRating(school, list_type) > 80

def _closestMatchSchool(school, list_type):
   return _closestMatch(school, list_type)[0]

def _closestMatchRating(school, list_type):
   return _closestMatch(school, list_type)[1]

def _closestMatch(school, list_type):
   return process.extractOne(school, _subjects(list_type))

def _subjects(list_type):
   cursor = sqlite3.connect("schools.db").cursor()
   cursor.execute("SELECT * FROM " + list_type)
   return  _tuples_tuple_to_list(cursor.fetchall())

def _tuples_tuple_to_list(tuple):
   return map(list, zip(*tuple))[0]
