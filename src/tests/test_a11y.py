import multiprocessing
import os
from string import Template

from axe_core_python.sync_playwright import Axe
from flask import url_for
from playwright.sync_api import Page

multiprocessing.set_start_method("fork")


def test_a11y(live_server, page: Page):
    axe = Axe()
    page.goto(url_for("home_page", _external=True))
    result = axe.run(page)
    violations = result["violations"]
    print(f"{len(violations)} violations found.")
    assert len(violations) == 0, report(violations)


def report(violations: list) -> str:
    """
    Return readable report of accessibility violations found.
    """
    report_str = "Found " + str(len(violations)) + " accessibility violations:"
    template_f = open(os.path.join(os.path.dirname(__file__), "violation.txt"))
    template = Template(template_f.read())
    template_f.close()
    for violation in violations:
        nodes_str = ""
        i = 1
        for node in violation["nodes"]:
            for target in node["target"]:
                nodes_str += f"\n\t{i}) Target: {target}"
                i += 1
            for item in node["all"] + node["any"] + node["none"]:
                nodes_str += "\n\t\t" + item["message"]
        report_str += template.substitute(violation, elements=nodes_str)
    return report_str
