import os
import json
import urllib.request


def get_worksheet_data(worksheet_id):
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", 'NoKeyFound')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/1ppywkX1g_0ynTIs6qQvCMzsandxLqMUHFDR0SQyjvtA/values/{worksheet_id}?key={GOOGLE_API_KEY}"
    rows = []
    with urllib.request.urlopen(url) as result:
        if result.status == 200:
            entries = json.loads(result.read())["values"]
        headers = entries[0]
        for entry in entries[1:]:
            row_info = {}
            for ind, header in enumerate(headers):
                row_info[header] = entry[ind]
            rows.append(row_info)
    return rows


def get_blogger_data(tag=None):
    url = "http://www.blogger.com/feeds/8501278254137514883/posts/default?max-results=150&alt=json"
    if tag:
        url += f"&category={tag}"
    posts = []
    tags = []
    with urllib.request.urlopen(url) as result:
        if result.status == 200:
            feed = json.loads(result.read())["feed"]
            tags = [category["term"] for category in feed["category"]]
            entries = feed["entry"]
            for entry in entries:
                post_info = {}
                post_info["title"] = entry["title"]["$t"]
                links = entry["link"]
                for link in links:
                    if link["rel"] == "alternate":
                        post_info["link"] = link["href"]
                posts.append(post_info)
    return posts, tags, tag
