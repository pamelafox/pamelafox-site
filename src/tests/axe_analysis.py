import multiprocessing
import os

from axe_core_python.sync_playwright import Axe
from flask import url_for
from playwright.sync_api import Page

multiprocessing.set_start_method("fork")


def test_a11y(app, live_server, page: Page):
    axe = Axe()
    # for route in app.url_map():
    page.goto(url_for("home_page", _external=True))
    results = axe.run(page, {"resultTypes": ["violations"]})
    Axe.save_results(results, os.path.join(os.path.dirname(__file__), "axe_results.json"), violations_only=True)
    assert len(results["violations"]) == 0, Axe.report_violations(results)
