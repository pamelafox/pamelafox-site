import json
import urllib.request


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
