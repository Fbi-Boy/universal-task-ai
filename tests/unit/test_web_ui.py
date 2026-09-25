from backend.api.main import web_css, web_js, web_ui


def test_ui_routes_return_files() -> None:
    assert web_ui().path.endswith("backend/web/index.html")
    assert web_js().path.endswith("backend/web/ui.js")
    assert web_css().path.endswith("backend/web/ui.css")


def test_reference_workspace_markup_and_styles_are_present() -> None:
    html = open(web_ui().path, encoding="utf-8").read()
    css = open(web_css().path, encoding="utf-8").read()
    assert 'Projects' in html
    assert 'quick' in html
    assert 'app-shell' in css
    assert '@media' in css
