import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from django.utils import simplejson
    
def getpage(filename, values={}):
  page = memcache.get(filename)
  if page:
    return page
  else:
    path = os.path.join(os.path.dirname(__file__), filename)
    page = template.render(path, values)
    memcache.set(filename, page, 60*30)
    return page
    
    
class HomePage(webapp.RequestHandler):
  def get(self):
    pic = {}
    url = 'https://api.dailybooth.com/v1/users/254325/pictures.json?limit=1'
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      json = simplejson.loads(result.content)
      pic = json[0]
    self.response.out.write(getpage('index.html', {'pic': pic}))
    
class ReadingList(webapp.RequestHandler):
  def get(self):
    books = []
    url = 'https://spreadsheets.google.com/feeds/list/0Ah0xU81penP1dFNLWk5YMW41dkcwa1JNQXk3YUJoOXc/od6/public/values?sq=include%3Dyes&alt=json'
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      json = simplejson.loads(result.content)
      entries = json["feed"]["entry"]
      for entry in entries:
        fields = ['title', 'author', 'asin', 'review', 'rating']
        book_info = {}
        for field in fields:
          if entry['gsx$' + field]:
            book_info[field] = entry['gsx$' + field]['$t']
        books.append(book_info)
      
    self.response.out.write(getpage('readinglist.html', {'books': books}))
    
    
application = webapp.WSGIApplication(
                                     [('/', HomePage),
                                      ('/readinglist', ReadingList)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
