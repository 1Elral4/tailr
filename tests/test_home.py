from django.test import Client


def test_home_renders_base_layout_and_assets() -> None:
    response = Client().get("/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "<title>tailr</title>" in content
    assert "tailr</a>" in content
    assert "Data Bank" in content
    assert "Applications" in content
    assert 'href="/static/css/tailwind.css"' in content
    assert "htmx.org@2." in content
    assert "alpinejs@3." in content
