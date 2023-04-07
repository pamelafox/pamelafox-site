import multiprocessing

from axe_core_python.sync_playwright import Axe
from flask import url_for
from playwright.sync_api import Page

multiprocessing.set_start_method("fork")


def test_a11y(app, live_server, page: Page):
    axe = Axe()
    violations_count = 0
    violations_reports = ""
    for route in ["home_page", "projects"]:
        page.goto(url_for(route, _external=True))
        results = axe.run(page, {"resultTypes": ["violations"]})
        # Track violations for report at the end
        violations_count += len(results["violations"])
        violations_reports += Axe.report_violations(results)
    assert violations_count == 0, violations_reports
