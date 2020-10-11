from app import app


client = app.test_client()


def test_post_task():
    response = client.post('/')
    assert response.status_code == 200


def test_get_task():
    response = client.post('/')
    assert response.status_code == 200
