import os
import json
from playwright.sync_api import expect

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')


def test_root(page):
    response = page.goto(BASE_URL)
    assert response.ok
    expect(page.locator('body')).to_contain_text('Hello from Task Manager!')

def test_view(page):
    response = page.request.get(f'{BASE_URL}/view')
    
    # Debug output
    print(f"Status: {response.status}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    # Check if response is actually JSON
    if response.status != 200:
        print(f"Error response: {response.text()}")
    
    assert response.status == 200, f"Expected 200, got {response.status}: {response.text()}"
    
    # Only parse JSON if status is OK
    data = response.json()
    assert isinstance(data, list)

def test_add(page):
    response = page.request.post(
        f'{BASE_URL}/add',
        data = json.dumps({'task': 'test task'}),
        headers = {'Content-Type': 'application/json'}
    )
    assert response.status == 201
    assert response.json() == {'OK': True}

def test_update_status(page):
    page.request.post(
        f'{BASE_URL}/add',
        data = json.dumps({'task': 'test task'}),
        headers = {'Content-Type': 'application/json'}
    )
    view = page.request.get(f"{BASE_URL}/view")
    tasks = view.json()
    task_id = tasks[-1]["task_id"]
    response = page.request.post(
        f"{BASE_URL}/update_status",
        data=json.dumps({"task_id": task_id, "task_status": "DONE"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.ok
    assert response.json() == {"OK": True}

def test_delete(page): 
    page.request.post(
        f'{BASE_URL}/add',
        data = json.dumps({'task': 'test task'}),
        headers = {'Content-Type': 'application/json'}
    )
    view = page.request.get(f'{BASE_URL}/view')
    matches = [t for t in view.json() if t.get('task') == 'test task']
    task_id = matches[-1]['task_id']
    response = page.request.post(
        f'{BASE_URL}/delete',
        data = json.dumps({'task_id': task_id}),
        headers = {'Content-Type': 'application/json'}
    )
    assert response.ok
    assert response.json() == {'OK': True}