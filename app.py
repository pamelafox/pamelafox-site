import os
import json
import urllib.request
from functools import wraps

from flask import Flask, render_template, request, make_response

app = Flask(__name__)
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

def get_worksheet_data(worksheet_id, fields=[], filter=None):
  url = f'https://sheets.googleapis.com/v4/spreadsheets/1ppywkX1g_0ynTIs6qQvCMzsandxLqMUHFDR0SQyjvtA/values/{worksheet_id}?key={GOOGLE_API_KEY}'
  rows = []
  tags = []
  if filter:
    url += f'&q={filter}'
  with urllib.request.urlopen(url) as result:
    if result.status == 200:
      entries = json.loads(result.read())['values']
    headers = entries[0] 
    for entry in entries[1:]:
      row_info = {}
      for ind, header in enumerate(headers):
        row_info[header] = entry[ind]
      rows.append(row_info)
  return rows, tags, filter

def cache_control(minutes=10):
    """Returns a Flask decorator that sets Cache-Control header. """
    def decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            r = func(*args, **kwargs)
            rsp = make_response(r, 200)
            rsp.headers.add('Cache-Control', 'public,max-age=%d' % int(3600 * 60 * minutes))
            return rsp
        return decorated_func
    return decorator


@app.route('/')
@cache_control(20)
def home_page():
  values = {'title': 'pamela fox'}
  return render_template('index.html', **values)
    
@app.route('/readinglist')
@cache_control(60)
def readinginglist():
  values = {'title': 'pamela fox\'s reading list'}
  return render_template('readinglist.html', **values)

@app.route('/talks')
@cache_control(10)
def talks():
  fields = ['title', 'date', 'description', 'thumbnail', 'slides', 'video', 'tags', 'location']
  talks, tags, filter = get_worksheet_data('Talks')
  title = 'pamela fox\'s talks'
  if filter:
    title += ' :: ' + filter
  values = {'talks': talks, 'tags': tags, 'filter': filter, 'title': title}
  return render_template('talks.html', **values) 

@app.route('/projects') 
@cache_control(10)
def projects():
    fields = ['title', 'date', 'description', 'homepage', 'source', 'thumbnail']
    projects, tags, filter = get_worksheet_data('Projects', fields)
    title = 'pamela fox\'s projects'
    values = {'projects': projects, 'tags': tags, 'filter': filter, 'title': title}
    return render_template('projects.html', **values)

@app.route('/interviews')
@cache_control(10)
def interviews():
  fields = ['title', 'url']
  interviews, tags, filter = get_worksheet_data('Interviews', fields)
  title = 'pamela fox\'s interviews'
  values = {'interviews': interviews, 'title': title}
  return render_template('interviews.html', **values)

@app.route('/blogposts')
@cache_control(15)
def blogposts():
  import datetime as dt
  tag = request.args.get('tag', None)
  url = 'http://www.blogger.com/feeds/8501278254137514883/posts/default?max-results=150&alt=json'
  if tag:
    url += f'&category={tag}'
  posts = []
  with urllib.request.urlopen(url) as result:
    if result.status == 200:
      feed = json.loads(result.read())['feed']
      entries = feed['entry']
      for entry in entries:
        post_info = {}
        post_info['title'] = entry['title']['$t']
        links = entry['link']
        for link in links:
          if link['rel'] == 'alternate':
            post_info['link'] = link['href']
        posts.append(post_info)
    title = 'pamela fox\'s blog posts'
    tags = ['socialanxiety', 'developerexperience', 'apis', 'javascript', 'python', 'appengine', 'css', 'jquery', 'bootstrap', 'backbone', 'performance', 'phonegap', 'girldevelopit', 'coursera', 'khanacademy', 'google','eatdifferent'] 
    values = {'tags': tags, 'posts': posts, 'title': title}
    return render_template('blogposts.html', **values)


if __name__ == '__main__':
   app.run()
