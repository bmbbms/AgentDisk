"""Helpers for generating test JWTs for local SDK verification."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time

DEFAULT_TEST_JWT_SECRET = "dev-jwt-secret-for-testing-only"
DEFAULT_TEST_USER_ID = "sdk-test-user"
DEFAULT_TEST_AGENT_ID = "sdk-test-agent"
DEFAULT_TEST_AGENT_GROUP_ID = "sdk-test-group"
DEFAULT_TEST_EXPIRE_HOURS = 72


def create_test_token(
    *,
    secret: str | None = None,
    user_id: str = DEFAULT_TEST_USER_ID,
    agent_id: str = "",
    agent_group_id: str = "",
    expire_hours: int = DEFAULT_TEST_EXPIRE_HOURS,
) -> str:
    """Create a valid HS256 JWT for local SDK verification.

    This helper is intended for development and integration testing only.
    It generates the same claim shape as the backend JWT helper:
    `userId`, optional `agentId`, optional `agentGroupId`, `iat`, and `exp`.
    """

    if not user_id:
        raise ValueError("user_id is required")
    if expire_hours <= 0:
        raise ValueError("expire_hours must be greater than 0")

    now = int(time.time())
    payload: dict[str, int | str] = {
        "userId": user_id,
        "iat": now,
        "exp": now + expire_hours * 3600,
    }
    if agent_id:
        payload["agentId"] = agent_id
    if agent_group_id:
        payload["agentGroupId"] = agent_group_id

    secret_value = secret or os.environ.get("AGENTDISK_JWT_SECRET") or DEFAULT_TEST_JWT_SECRET
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _encode_segment(header)
    payload_segment = _encode_segment(payload)
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = hmac.new(secret_value.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_segment = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")
    return f"{header_segment}.{payload_segment}.{signature_segment}"


def _encode_segment(value: dict[str, int | str]) -> str:
    encoded = json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return base64.urlsafe_b64encode(encoded).rstrip(b"=").decode("ascii")


__all__ = [
    "DEFAULT_TEST_AGENT_GROUP_ID",
    "DEFAULT_TEST_AGENT_ID",
    "DEFAULT_TEST_EXPIRE_HOURS",
    "DEFAULT_TEST_JWT_SECRET",
    "DEFAULT_TEST_USER_ID",
    "create_test_token",
]
