from time import sleep
from uuid import uuid4 as generate_uuid

import pytest
from fastapi.testclient import TestClient

from fastapi_simple_mutex_server.main import app
from fastapi_simple_mutex_server.config import service_config
from fastapi_simple_mutex_server.models import (
    ObtainMutexResponse,
    ReleaseMutexResponse
)


client = TestClient(app)

TEST_RESOURCE_NAME = 'test123'


@pytest.fixture
def random_test_data() -> str:
    return str(generate_uuid()) + str(generate_uuid())


def test_get_mutex_noauth():
    response = client.get("/api/v1/mutex")
    assert response.status_code == 403


def test_delete_mutex_noauth():
    response = client.delete("/api/v1/mutex")
    assert response.status_code == 403


def test_get_mutex_badauth(random_test_data: str):
    response = client.get("/api/v1/mutex", params={'api_key': random_test_data})
    assert response.status_code == 403


def test_delete_mutex_badauth():
    response = client.delete("/api/v1/mutex", params={'api_key': random_test_data})
    assert response.status_code == 403


class MutexAPITester:
    def get(ttl=None) -> ObtainMutexResponse:
        ttl_param = dict()
        if ttl:
            ttl_param = {
                'ttl': ttl
            }

        response = client.get("/api/v1/mutex", params={
            'resource_name': TEST_RESOURCE_NAME,
            'api_key': service_config.api_key
        } | ttl_param)

        assert response.status_code == 200
        return ObtainMutexResponse(**response.json())

    def delete(uuid) -> ReleaseMutexResponse:
        response = client.delete("/api/v1/mutex", params={
            'resource_name': TEST_RESOURCE_NAME,
            'uuid': uuid,
            'api_key': service_config.api_key
        })

        assert response.status_code == 200
        return ReleaseMutexResponse(**response.json())

@pytest.fixture
def mutex_api_tester() -> MutexAPITester:
    return MutexAPITester


def test_mutex_api(mutex_api_tester: MutexAPITester, random_test_data: str):
    # try and delete the mutex
    # since it doesn't exist, delete will return True
    r = mutex_api_tester.delete(uuid=random_test_data)
    assert r.released == True

    # try and get the mutex
    r = mutex_api_tester.get()
    assert r.obtained == True
    uuid1 = r.uuid

    # try and get the mutex
    # since it already exists, get will return False
    r = mutex_api_tester.get()
    assert r.obtained == False

    # try and delete the mutex with an incorrect uuid
    r = mutex_api_tester.delete(uuid=random_test_data)
    assert r.released == False

    # try and delete the mutex with the correct uuid
    r = mutex_api_tester.delete(uuid=uuid1)
    assert r.released == True

    # try and get the mutex again after it has been deleted
    r = mutex_api_tester.get()
    assert r.obtained == True
    uuid2 = r.uuid

    # try and delete the mutex using the old uuid
    r = mutex_api_tester.delete(uuid=uuid1)
    assert r.released == False

    # try and delete the mutex with the new uuid
    r = mutex_api_tester.delete(uuid=uuid2)
    assert r.released == True

    # try and get a mutex with a ttl
    r = mutex_api_tester.get(ttl=2)
    assert r.obtained == True
    uuid3 = r.uuid

    # try and get the mutex again
    r = mutex_api_tester.get(ttl=2)
    assert r.obtained == False

    # wait three seconds and then
    # try and get the mutex again
    sleep(3)
    r = mutex_api_tester.get(ttl=5)
    assert r.obtained == True
    uuid4 = r.uuid

    # try and delete the mutex using the old uuid
    r = mutex_api_tester.delete(uuid=uuid3)
    assert r.released == False

    # try and delete the mutex with the new uuid
    r = mutex_api_tester.delete(uuid=uuid4)
    assert r.released == True
