"""
 Licensed under the Apache License, Version 2.0: 
 http://www.apache.org/licenses/LICENSE-2.0 
"""
 
import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from django.utils import simplejson
  
    
class BaseRequestHandler(webapp.RequestHandler):

  def get(self):
    page = memcache.get(self.get_cachename())
    if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
	  page = None
    if not page:
      path = os.path.join(os.path.dirname(__file__), self.get_filename())
      page = template.render(path, self.get_values())
      memcache.set(self.get_cachename(), page, 60*30)
    self.response.out.write(page)
    
  def get_worksheet_data(self, worksheet_id, fields, extra_query=None):
    url = 'https://spreadsheets.google.com/feeds/list/0Ah0xU81penP1dFNLWk5YMW41dkcwa1JNQXk3YUJoOXc/' + worksheet_id + '/public/values?sq=include%3Dyes&alt=json'
    if extra_query:
      url += extra_query
    filter = None
    if self.request.get('q'):
      filter = self.request.get('q')
      url += '&q=' + filter
    result = urlfetch.fetch(url)
    rows = []
    tags = []
    if result.status_code == 200:
      json = simplejson.loads(result.content)
      feed = json['feed']
      entries = []
      if 'entry' in feed:
        entries = feed['entry']
      for entry in entries:
        row_info = {}
        matches = True
        for field in fields:
          logging.info(field)
          if not entry['gsx$' + field]:
            continue
          row_info[field] = entry['gsx$' + field]['$t']
          if field == 'tags':
            # Check this row matches filtered tag
            # and row_info[field].find(filter) == -1
            if filter is not None and row_info['tags'].find(filter) == -1:
              matches = False
            # Add to our current tags list
            row_tags = row_info['tags'].split(',')
            for tag in row_tags:
              tag = tag.strip()
              if tag not in tags and len(tag) > 0:
                tags.append(tag)
        if matches:
          logging.info('appending')
          rows.append(row_info)
    logging.info(rows)
    return rows, tags, filter


class HomePage(BaseRequestHandler):

  def get_filename(self):
    return 'index.html'

  def get_cachename(self):
    return 'index'

  def get_values(self):
    return {'title': 'pamela fox'}

    
class ReadingList(BaseRequestHandler):

  def get_filename(self):
    return 'readinglist.html'

  def get_cachename(self):
     return 'readinglist' + self.request.get('q', '')

  def get_values(self):
    fields = ['title', 'author', 'asin', 'review', 'rating', 'thumbnail', 'tags']
    books, tags, filter = self.get_worksheet_data('od6', fields)
    title = 'pamela fox\'s reading list'
    if filter:
      title += ' :: ' + filter
    return {'books': books, 'tags': tags, 'filter': filter, 'title': title}
    
class Talks(BaseRequestHandler):

  def get_filename(self):
    return 'talks.html'
    
  def get_cachename(self):
    return 'talks' + self.request.get('q', '')

  def get_values(self):
    fields = ['title', 'date', 'description', 'thumbnail', 'slides', 'video', 'tags', 'location']
    talks, tags, filter = self.get_worksheet_data('od7', fields, '&orderby=column:date&reverse=true')
    title = 'pamela fox\'s talks'
    if filter:
      title += ' :: ' + filter
    return {'talks': talks, 'tags': tags, 'filter': filter, 'title': title}


class Projects(BaseRequestHandler):

  def get_filename(self):
    return 'projects.html'
    
  def get_cachename(self):
    return 'projects'
    
  def get_values(self):
    fields = ['title', 'date', 'description', 'homepage', 'source', 'thumbnail']
    projects, tags, filter = self.get_worksheet_data('od5', fields, '&orderby=column:date&reverse=true')
    title = 'pamela fox\'s projects'
    return {'projects': projects, 'tags': tags, 'filter': filter, 'title': title}


class BlogPosts(BaseRequestHandler):

  def get_filename(self):
    return 'blogposts.html'

  def get_cachename(self):
    return 'blogposts'

  def get_values(self):
	import datetime as dt
	
	url = 'http://www.blogger.com/feeds/8501278254137514883/posts/default?max-results=150&alt=json'
	result = urlfetch.fetch(url)
	posts = []
	if result.status_code == 200:
	  json = simplejson.loads(result.content)
	  feed = json['feed']
	  entries = feed['entry']
	  for entry in entries:
	    post_info = {}
	    post_info['title'] = entry['title']['$t']
	    #post_info['date'] = dt.datetime.strptime(entry['published']['$t'], '%Y-%m-%dT%H:%M:%S.%f-%Z')
	    links = entry['link']
	    for link in links:
		  if link['rel'] == 'alternate':
			post_info['link'] = link['href']
	    posts.append(post_info)
	title = 'pamela fox\'s blog posts'
	return {'posts': posts, 'title': title}


    
application = webapp.WSGIApplication(
                                     [('/', HomePage),
                                      ('/readinglist', ReadingList),
                                      ('/projects', Projects),
                                      ('/blogposts', BlogPosts),
                                      ('/talks', Talks)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
