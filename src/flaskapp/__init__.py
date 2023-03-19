import json
import os

from flask import Flask, render_template

from .datasources import get_blogger_data

app = Flask(__name__)


def load_json_file(filename):
    file = open(os.path.join(app.root_path, "data", filename))
    return json.load(file)


@app.route("/")
def home_page():
    values = {"title": "pamela fox"}
    return render_template("index.html", **values)


@app.route("/readinglist/")
def readinglist():
    values = {"title": "pamela fox's reading list"}
    return render_template("readinglist.html", **values)


@app.route("/talks/")
def talks():
    talks = load_json_file("talks.json")
    title = "pamela fox's talks"
    values = {"talks": talks, "title": title}
    return render_template("talks.html", **values)


@app.route("/projects/")
def projects():
    projects = load_json_file("projects.json")
    title = "pamela fox's projects"
    values = {"projects": projects, "title": title}
    return render_template("projects.html", **values)


@app.route("/interviews/")
def interviews():
    interviews = load_json_file("interviews.json")
    title = "pamela fox's interviews"
    values = {"interviews": interviews, "title": title}
    return render_template("interviews.html", **values)


@app.route("/blogposts/")
@app.route("/blogposts/<tag>.html")
def blogposts(tag=None):
    posts, tags, tag = get_blogger_data(tag)
    title = "pamela fox's blog posts"
    values = {"tags": tags, "posts": posts, "title": title}
    return render_template("blogposts.html", **values)
