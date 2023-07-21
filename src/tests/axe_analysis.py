import multiprocessing

from axe_playwright_python.sync_playwright import Axe
from flask import url_for
from playwright.sync_api import Page

multiprocessing.set_start_method("fork")


def test_a11y(app, live_server, page: Page):
    axe = Axe()
    violations_count = 0
    violations_reports = ""
    for route in ["home_page", "projects", "talks", "interviews"]:
        page.goto(url_for(route, _external=True))
        results = axe.run(page)
        violations_count += results.violations_count
        violations_reports += results.generate_report()
    assert violations_count == 0, violations_reports
