"""Unit tests for SDK test-auth helpers."""

from __future__ import annotations

import base64
import json
import time

import pytest

from agentdisk import AgentDiskClient, AsyncAgentDiskClient, create_test_token


def _decode_payload(token: str) -> dict[str, object]:
    _header, payload, _signature = token.split(".")
    padding = "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload + padding).decode("utf-8"))


def test_create_test_token_user_claims():
    before = int(time.time())
    token = create_test_token(secret="unit-test-secret", user_id="tester")
    payload = _decode_payload(token)

    assert payload["userId"] == "tester"
    assert "agentId" not in payload
    assert payload["iat"] >= before
    assert payload["exp"] > payload["iat"]


def test_create_test_token_agent_claims():
    token = create_test_token(
        secret="unit-test-secret",
        user_id="tester",
        agent_id="agent-01",
        agent_group_id="team-a",
    )
    payload = _decode_payload(token)

    assert payload["userId"] == "tester"
    assert payload["agentId"] == "agent-01"
    assert payload["agentGroupId"] == "team-a"


def test_create_test_token_requires_user_id():
    with pytest.raises(ValueError, match="user_id is required"):
        create_test_token(secret="unit-test-secret", user_id="")


def test_create_test_token_requires_positive_expiry():
    with pytest.raises(ValueError, match="expire_hours must be greater than 0"):
        create_test_token(secret="unit-test-secret", user_id="tester", expire_hours=0)


def test_sync_client_from_test_auth_sets_token():
    client = AgentDiskClient.from_test_auth(
        base_url="http://localhost:9100",
        secret="unit-test-secret",
        user_id="tester",
        agent_id="agent-01",
        agent_group_id="team-a",
    )
    try:
        payload = _decode_payload(client._token)
        assert payload["userId"] == "tester"
        assert payload["agentId"] == "agent-01"
        assert payload["agentGroupId"] == "team-a"
    finally:
        client.close()


def test_async_client_from_test_auth_sets_token():
    client = AsyncAgentDiskClient.from_test_auth(
        base_url="http://localhost:9100",
        secret="unit-test-secret",
        user_id="tester",
    )
    try:
        payload = _decode_payload(client._token)
        assert payload["userId"] == "tester"
    finally:
        import asyncio

        asyncio.get_event_loop().run_until_complete(client.close())
