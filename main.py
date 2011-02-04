"""
 Licensed under the Apache License, Version 2.0: 
 http://www.apache.org/licenses/LICENSE-2.0 
"""
 
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from django.utils import simplejson
  
    
class BaseRequestHandler(webapp.RequestHandler):

  def get(self):
    page = memcache.get(self.get_cachename())
    if not page:
      path = os.path.join(os.path.dirname(__file__), self.get_filename())
      page = template.render(path, self.get_values())
      memcache.set(self.get_cachename(), page, 60*30)
    self.response.out.write(page)
    

class HomePage(BaseRequestHandler):

  def get_filename(self):
    return 'index.html'

  def get_cachename(self):
    return 'index'

  def get_values(self):
    pic = {}
    url = 'https://api.dailybooth.com/v1/users/254325/pictures.json?limit=1'
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      json = simplejson.loads(result.content)
      pic = json[0]
    return {'pic': pic}

    
class ReadingList(BaseRequestHandler):

  def get_filename(self):
    return 'readinglist.html'

  def get_cachename(self):
     return 'readinglist' + self.request.get('q', '')

  def get_values(self):
    books = []
    url = 'https://spreadsheets.google.com/feeds/list/0Ah0xU81penP1dFNLWk5YMW41dkcwa1JNQXk3YUJoOXc/od6/public/values?sq=include%3Dyes&alt=json'
    if self.request.get('q'):
      url += '&q=' + self.request.get('q')
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      json = simplejson.loads(result.content)
      feed = json['feed']
      if 'entry' in feed:
        entries = feed['entry']
      else:
        entries = []
      for entry in entries:
        fields = ['title', 'author', 'asin', 'review', 'rating', 'thumbnail']
        book_info = {}
        for field in fields:
          if entry['gsx$' + field]:
            book_info[field] = entry['gsx$' + field]['$t']
        books.append(book_info)
    return {'books': books}
    
    
application = webapp.WSGIApplication(
                                     [('/', HomePage),
                                      ('/readinglist', ReadingList)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
