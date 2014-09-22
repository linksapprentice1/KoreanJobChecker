import sqlite3
import urllib2 
import re
from threading import Thread

class Koreanlist:

   def __init__(self, list_type, cursor):
      self.list_type = list_type
      self.webpage = ""
      self.cursor = cursor
      self.filename = list_type + ".txt"

   def update(self):
      self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.list_type + " (company)")
      self.checkWebpage()
      if self._webpageUpdated():
         self._saveWebpage()
         self._updateTable()

   def checkWebpage(self):
      if self.webpage == "":
         self.webpage = self._html("http://" + self.list_type + ".tokyojon.com/")

   def _html(self, url):
      return urllib2.urlopen(url).read()

   def _webpageUpdated(self):
      return self.webpage is not self._savedPage()

   def _saveWebpage(self):
      with open(self.filename, 'w') as f:
         f.write(self.webpage)

   def _savedPage(self):
      try:
         with open(self.filename, 'r') as f:
            return f.read()
      except:
         return ""

   def _updateTable(self):
      subjects = re.findall("ubject:[</span>]*([\w| |\-|\,]{6,})", self.webpage)
      subject_tuples = [(self._prettyPrint(subject), ) for subject in subjects]
      self.cursor.executemany("INSERT INTO " + self.list_type + "(company) VALUES (?)", subject_tuples)

   def _prettyPrint(self, string):
      return string.strip().lower()

class Greenlist(Koreanlist):

   def __init__(self, cursor):
      Koreanlist.__init__(self, "greenlist", cursor)

class Blacklist(Koreanlist):

   def __init__(self, cursor):
      Koreanlist.__init__(self, "blacklist", cursor)


def updateDatabase():
   conn = sqlite3.connect("schools.db", check_same_thread=False)
   cursor = conn.cursor()
   lists = [Greenlist(cursor), Blacklist(cursor)]
   _checkWebpages(lists)
   _updateLists(lists)
   conn.commit()

def _checkWebpages(lists):
   threads = [_makeThread(l.checkWebpage(), ()) for l in lists]
   _joinThreads(threads)

def _makeThread(function, arguments):
   thread = Thread(target=function, args=arguments)
   thread.start()
   return thread

def _joinThreads(threads):
   for thread in threads:
       thread.join()

def _updateLists(lists):
   for l in lists:
       l.update()
