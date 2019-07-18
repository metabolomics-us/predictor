import pytest

from predictor.app import app


@pytest.fixture
def client(request):

    client = app.test_client()

    def teardown():
        pass  # databases and resourses have to be freed at the end. But so far we don't have anything

    return client
