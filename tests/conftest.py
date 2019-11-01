import pytest
import random
import string
import json
from unittest import mock
from urllib.parse import urljoin
from requests.models import Response

from bulk_api_client import Client, AppAPI, ModelAPI


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


@pytest.fixture
def client():
    token = random_string()
    url = "http://test"
    Client.app_api_urls = None
    Client.model_api_urls = {}
    client = Client(token, api_url=url)
    client.clear_cache()
    return client


@pytest.fixture
def app_api(client):
    app_label = random_string()
    data = {
        app_label: urljoin(client.api_url, app_label),
    }
    response = Response()
    response._content = json.dumps(data)
    response.status_code = 200
    with mock.patch.object(Client, 'request', return_value=response):
        app_api = AppAPI(client, app_label)
    return app_api


@pytest.fixture
def model_api(app_api):
    model_name = random_string().lower()
    data = {
        model_name: urljoin(app_api.client.api_url, model_name),
    }
    response = Response()
    response._content = json.dumps(data)
    response.status_code = 200
    with mock.patch.object(Client, 'request') as fn:
        fn.return_value = response
        model_api = ModelAPI(app_api, model_name)
    return model_api