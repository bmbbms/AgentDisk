"""Pytest fixtures for SDK tests."""

import os

import pytest

from agentdisk import AgentDiskClient, AsyncAgentDiskClient
from agentdisk.auth import create_test_token

BASE_URL = os.environ.get("AGENTDISK_URL", "http://localhost:9100")
JWT_SECRET = os.environ.get("AGENTDISK_JWT_SECRET", "dev-jwt-secret-for-testing-only")
DL_SECRET = os.environ.get("AGENTDISK_DL_SECRET", "dev-dl-token-secret-for-testing")


def _generate_jwt(user_id: str, agent_id: str = "", agent_group_id: str = "") -> str:
    return create_test_token(
        secret=JWT_SECRET,
        user_id=user_id,
        agent_id=agent_id,
        agent_group_id=agent_group_id,
    )


@pytest.fixture(scope="session")
def user_token():
    return _generate_jwt("sdk-test-user")


@pytest.fixture(scope="session")
def agent_token():
    return _generate_jwt("sdk-test-user", "sdk-test-agent", "sdk-test-group")


@pytest.fixture(scope="session")
def client(user_token):
    with AgentDiskClient.from_test_auth(
        base_url=BASE_URL,
        secret=JWT_SECRET,
        user_id="sdk-test-user",
    ) as c:
        yield c


@pytest.fixture(scope="session")
def agent_client(agent_token):
    with AgentDiskClient.from_test_auth(
        base_url=BASE_URL,
        secret=JWT_SECRET,
        user_id="sdk-test-user",
        agent_id="sdk-test-agent",
        agent_group_id="sdk-test-group",
    ) as c:
        yield c


@pytest.fixture
def async_client(user_token):
    c = AsyncAgentDiskClient.from_test_auth(
        base_url=BASE_URL,
        secret=JWT_SECRET,
        user_id="sdk-test-user",
    )
    yield c
    import asyncio

    asyncio.get_event_loop().run_until_complete(c.close())
