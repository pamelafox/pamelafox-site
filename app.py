import os
import logging
import json
import urllib.request

import jinja2
from flask import Flask, render_template, request

import app_secrets

app = Flask(__name__)
 
def get_worksheet_data(worksheet_id, fields=[], filter=None):
  url = f'https://sheets.googleapis.com/v4/spreadsheets/1ppywkX1g_0ynTIs6qQvCMzsandxLqMUHFDR0SQyjvtA/values/{worksheet_id}?key={app_secrets.GOOGLE_API_KEY}'
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

@app.route('/')
def home_page():
  values = {'title': 'pamela fox'}
  return render_template('index.html', **values)
    
@app.route('/readinglist')
def readinginglist():
  values = {'title': 'pamela fox\'s reading list'}
  return render_template('readinglist.html', **values)

@app.route('/talks')
def talks():
  fields = ['title', 'date', 'description', 'thumbnail', 'slides', 'video', 'tags', 'location']
  talks, tags, filter = get_worksheet_data('Talks')
  title = 'pamela fox\'s talks'
  if filter:
    title += ' :: ' + filter
  values = {'talks': talks, 'tags': tags, 'filter': filter, 'title': title}
  return render_template('talks.html', **values) 

@app.route('/projects') 
def projects():
    fields = ['title', 'date', 'description', 'homepage', 'source', 'thumbnail']
    projects, tags, filter = get_worksheet_data('Projects', fields)
    title = 'pamela fox\'s projects'
    values = {'projects': projects, 'tags': tags, 'filter': filter, 'title': title}
    return render_template('projects.html', **values)

@app.route('/interviews')
def interviews():
  fields = ['title', 'url']
  interviews, tags, filter = get_worksheet_data('Interviews', fields)
  title = 'pamela fox\'s interviews'
  values = {'interviews': interviews, 'title': title}
  return render_template('interviews.html', **values)

@app.route('/blogposts')
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
