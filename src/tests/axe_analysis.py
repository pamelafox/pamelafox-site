import multiprocessing

import pytest
from axe_playwright_python.sync_playwright import Axe
from flask import url_for
from playwright.sync_api import Page

multiprocessing.set_start_method("fork")


@pytest.mark.parametrize("route", ["home_page", "projects", "talks", "interviews"])
def test_a11y(app, live_server, page: Page, route: str):
    axe = Axe()
    page.goto(url_for(route, _external=True))
    results = axe.run(page)
    assert results.violations_count == 0, results.generate_report()
