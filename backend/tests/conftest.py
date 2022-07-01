from unittest import mock

import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.http_client import http_client


@pytest.fixture
def settings():
    return Settings.from_yaml("config.sample.yml")


@pytest.fixture
@mock.patch("app.core.config.settings", Settings.from_yaml("config.sample.yml"))
def client():
    from app.main import app

    return TestClient(app)


@pytest.fixture
def mock_server():
    with aioresponses() as m:
        yield m


@pytest.fixture
async def mock_http_client():
    await http_client.start_session()
    yield http_client
