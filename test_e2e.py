import os
from playwright.sync_api import expect

BASE_URL = os.getenv("BASE_URL", "http://web:8000")

def test_homepage(page):
    response = page.goto(BASE_URL)
    assert response is not None
    assert response.ok
    expect(page.locator("body")).to_be_visible()