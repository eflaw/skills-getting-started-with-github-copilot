import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app
import src.app as app_module

ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield

@pytest.fixture
def client():
    return TestClient(app)
