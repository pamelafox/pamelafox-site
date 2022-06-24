import os
import json
import urllib.request

from flask import Flask, render_template, request

from .decorators import cache_control
from .datasources import get_worksheet_data, get_blogger_data

app = Flask(__name__)


@app.route("/")
@cache_control(20)
def home_page():
    values = {"title": "pamela fox"}
    return render_template("index.html", **values)


@app.route("/readinglist")
@cache_control(60)
def readinginglist():
    values = {"title": "pamela fox's reading list"}
    return render_template("readinglist.html", **values)


@app.route("/talks")
@cache_control(10)
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
    return render_template("talks.html", **values)


@app.route("/projects")
@cache_control(10)
def projects():
    projects = get_worksheet_data("Projects")
    title = "pamela fox's projects"
    values = {"projects": projects, "title": title}
    return render_template("projects.html", **values)


@app.route("/interviews")
@cache_control(10)
def interviews():
    interviews = get_worksheet_data("Interviews")
    title = "pamela fox's interviews"
    values = {"interviews": interviews, "title": title}
    return render_template("interviews.html", **values)


@app.route("/blogposts")
@cache_control(15)
def blogposts():
    tag = request.args.get("tag", None)
    posts, tags, tag = get_blogger_data(tag)
    title = "pamela fox's blog posts"
    values = {"tags": tags, "posts": posts, "title": title}
    return render_template("blogposts.html", **values)
