"""
 Licensed under the Apache License, Version 2.0: 
 http://www.apache.org/licenses/LICENSE-2.0 
"""
 
import os
import logging
import json

import jinja2
import webapp2

from google.appengine.api import memcache
from google.appengine.api import urlfetch

import secrets


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
  
    
class BaseRequestHandler(webapp2.RequestHandler):

  def get(self):
    page = memcache.get(self.get_cachename())
    if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
	  page = None
    if not page:
      template = JINJA_ENVIRONMENT.get_template(self.get_filename())
      page = template.render(self.get_values())
      memcache.set(self.get_cachename(), page, 60*1)
    self.response.out.write(page)
    
  def get_worksheet_data(self, worksheet_id, fields=[]):
    url = 'https://sheets.googleapis.com/v4/spreadsheets/1ppywkX1g_0ynTIs6qQvCMzsandxLqMUHFDR0SQyjvtA/values/' + worksheet_id + '?key=' + secrets.GOOGLE_API_KEY
    filter = None
    if self.request.get('q'):
      filter = self.request.get('q')
      url += '&q=' + filter
    result = urlfetch.fetch(url)
    rows = []
    tags = []
    if result.status_code == 200:
      entries = json.loads(result.content)['values']
      headers = entries[0] 
      for entry in entries[1:]:
        row_info = {}
        for ind, header in enumerate(headers):
          row_info[header] = entry[ind]
        rows.append(row_info)
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
     return 'readinglist'

  def get_values(self):
    return {'title': 'pamela fox\'s reading list'}
    
class Talks(BaseRequestHandler):

  def get_filename(self):
    return 'talks.html'
    
  def get_cachename(self):
    return 'talks' + self.request.get('q', '')

  def get_values(self):
    fields = ['title', 'date', 'description', 'thumbnail', 'slides', 'video', 'tags', 'location']
    talks, tags, filter = self.get_worksheet_data('Talks')
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
    projects, tags, filter = self.get_worksheet_data('Projects', fields)
    title = 'pamela fox\'s projects'
    return {'projects': projects, 'tags': tags, 'filter': filter, 'title': title}


class Interviews(BaseRequestHandler):

  def get_filename(self):
    return 'interviews.html'
    
  def get_cachename(self):
    return 'interviews'
    
  def get_values(self):
    fields = ['title', 'url']
    interviews, tags, filter = self.get_worksheet_data('Interviews', fields)
    title = 'pamela fox\'s interviews'
    return {'interviews': interviews, 'title': title}

class BlogPosts(BaseRequestHandler):

  def get_filename(self):
    return 'blogposts.html'

  def get_cachename(self):
    return 'blogposts' + self.request.get('tag', '')

  def get_values(self):
	import datetime as dt
        tag = self.request.get('tag')
	url = 'http://www.blogger.com/feeds/8501278254137514883/posts/default?max-results=150&alt=json'
        if tag:
          url += '&category=%s' % (tag)
	result = urlfetch.fetch(url)
	posts = []
	if result.status_code == 200:
	  feed = json.loads(result.content)['feed']
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
        tags = ['socialanxiety', 'developerexperience', 'apis', 'javascript', 'python', 'appengine', 'css', 'jquery', 'bootstrap', 'backbone', 'performance', 'phonegap', 'girldevelopit', 'coursera', 'khanacademy', 'google','eatdifferent'] 
	return {'tags': tags, 'posts': posts, 'title': title}


    
app = webapp2.WSGIApplication([('/', HomePage),
                               ('/readinglist', ReadingList),
                               ('/projects', Projects),
                               ('/interviews', Interviews),
                               ('/blogposts', BlogPosts),
                               ('/talks', Talks)],
                               debug=True)

