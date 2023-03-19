import io
import json
import unittest.mock
import urllib.request

from flaskapp.datasources import get_blogger_data

fake_blogger_data = {
    "feed": {
        "category": [{"term": "khanacademy"}, {"term": "eatdifferent"}, {"term": "musicvideo"}],
        "entry": [
            {
                "id": {"$t": "tag:blogger.com,1999:blog-8501278254137514883.post-7028526666522021237"},
                "published": {"$t": "2022-06-07T15:26:00.005-07:00"},
                "updated": {"$t": "2022-06-07T15:30:18.333-07:00"},
                "title": {"type": "text", "$t": "How accessibility helps a nursing mother"},
                "category": [{"scheme": "http://www.blogger.com/atom/ns#", "term": "a11y"}],
                "link": [
                    {
                        "rel": "self",
                        "type": "application/atom+xml",
                        "href": "https://www.blogger.com/feeds/8501278254137514883/posts/default/7028526666522021237",
                    },
                    {
                        "rel": "alternate",
                        "type": "text/html",
                        "href": "http://blog.pamelafox.org/2022/06/how-accessibility-helps-nursing-mother.html",
                        "title": "How accessibility helps a nursing mother",
                    },
                ],
            }
        ],
    }
}


def test_get_blogger_data():
    data = io.StringIO(json.dumps(fake_blogger_data))
    data.status = 200
    with unittest.mock.patch.object(urllib.request, "urlopen", return_value=data):
        rows, tags, tag = get_blogger_data()
        assert rows == [
            {
                "link": "http://blog.pamelafox.org/2022/06/how-accessibility-helps-nursing-mother.html",
                "title": "How accessibility helps a nursing mother",
            }
        ]
        assert tags == ["khanacademy", "eatdifferent", "musicvideo"]
        assert tag is None


def test_get_blogger_data_with_tag():
    data = io.StringIO(json.dumps(fake_blogger_data))
    data.status = 200
    with unittest.mock.patch.object(urllib.request, "urlopen", return_value=data) as mocked:
        rows, tags, tag = get_blogger_data("a11y")
        assert (
            mocked.call_args.args[0]
            == "http://www.blogger.com/feeds/8501278254137514883/posts/default?max-results=150&alt=json&category=a11y"
        )
        assert tag == "a11y"
