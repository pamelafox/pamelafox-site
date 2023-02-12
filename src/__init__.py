import os
import json
import urllib.request

from flask import Flask, make_response, render_template, request

from .datasources import get_worksheet_data, get_blogger_data

app = Flask(__name__)

def render_html_template(filename, **context):
    resp = make_response(render_template(filename, **context))
    resp.headers['Content-type'] = 'text/html; charset=utf-8'
    return resp


@app.route("/")
def home_page():
    values = {"title": "pamela fox"}
    return render_html_template("index.html", **values)


@app.route("/readinglist.html")
def readinginglist():
    values = {"title": "pamela fox's reading list"}
    return render_html_template("readinglist.html", **values)


@app.route("/talks.html")
def talks():
    fields = [
        "title",
        "date",
        "description",
        "thumbnail",
        "slides",
        "video",
        "tags",
        "location",
    ]
    talks = get_worksheet_data("Talks")
    title = "pamela fox's talks"
    values = {"talks": talks, "title": title}
    return render_html_template("talks.html", **values)


@app.route("/projects.html")
def projects():
    projects = get_worksheet_data("Projects")
    title = "pamela fox's projects"
    values = {"projects": projects, "title": title}
    return render_html_template("projects.html", **values)


@app.route("/interviews.html")
def interviews():
    interviews = get_worksheet_data("Interviews")
    title = "pamela fox's interviews"
    values = {"interviews": interviews, "title": title}
    return render_html_template("interviews.html", **values)


@app.route("/blogposts.html")
def blogposts():
    tag = request.args.get("tag", None)
    posts, tags, tag = get_blogger_data(tag)
    title = "pamela fox's blog posts"
    values = {"tags": tags, "posts": posts, "title": title}
    return render_html_template("blogposts.html", **values)
