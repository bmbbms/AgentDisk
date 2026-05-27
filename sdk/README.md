# AgentDisk Python SDK

Python SDK for [AgentDisk](https://github.com/wybug/AgentDisk) — an enterprise-grade cloud disk middleware designed for multi-agent systems.

## Installation

```bash
pip install agentdisk
```

Requires Python 3.9+.

## Quick Start

### Synchronous Client

```python
from agentdisk import AgentDiskClient

client = AgentDiskClient(
    base_url="http://localhost:9100",
    token="<jwt-from-gateway>",
)

# Folder operations
client.create_folder("docs/reports")
folders = client.list_folders("docs")

# File operations
client.upload_file("docs/reports/summary.md", "/local/summary.md")
client.upload_bytes("docs/notes.txt", b"hello world", auto_mkdir=True)
files = client.list_files("docs/reports")

# Share & preview
share = client.create_share("docs/reports", expire_hours=24)
result = client.preview("docs/reports/summary.md")

client.close()
```

### Default Test Authorization

For local verification, the SDK can generate a valid test JWT instead of requiring
you to paste a token manually.

```python
from agentdisk import AgentDiskClient

client = AgentDiskClient.from_test_auth(
    base_url="http://localhost:9100",
    user_id="sdk-test-user",
)

space = client.get_space()
client.close()
```

You can also generate the token yourself:

```python
from agentdisk import create_test_token

token = create_test_token(
    user_id="sdk-test-user",
    agent_id="sdk-test-agent",
    agent_group_id="sdk-test-group",
)
```

By default this uses `AGENTDISK_JWT_SECRET` if present, otherwise it falls back to
the local development secret `dev-jwt-secret-for-testing-only`.

### Asynchronous Client

```python
from agentdisk import AsyncAgentDiskClient

async with AsyncAgentDiskClient(
    base_url="http://localhost:9100",
    token="<jwt-from-gateway>",
) as client:
    await client.create_folder("docs/reports")
    await client.upload_file("docs/reports/summary.md", "/local/summary.md")
    files = await client.list_files("docs/reports")
```

Async clients support the same helper:

```python
from agentdisk import AsyncAgentDiskClient

async with AsyncAgentDiskClient.from_test_auth(
    base_url="http://localhost:9100",
    user_id="sdk-test-user",
) as client:
    await client.get_space()
```

## API Overview

All operations use **path-based** API — no need to manage folder/file IDs manually.

| Category | Methods |
|----------|---------|
| **Folders** | `create_folder`, `list_folders`, `get_folder`, `rename_folder`, `delete_folder` |
| **Files** | `upload_file`, `upload_bytes`, `list_files`, `get_file`, `update_file`, `update_file_bytes`, `delete_file` |
| **Shares** | `create_share`, `list_shares`, `revoke_share`, `get_share_by_code`, `access_share` |
| **Permissions** | `grant_permission`, `list_permissions`, `check_permission`, `revoke_permission` |
| **Tags** | `bind_tag`, `unbind_tag`, `search_files` |
| **Versions** | `list_versions`, `rollback_version` |
| **Recycle Bin** | `list_recycle`, `restore`, `delete_permanent` |
| **Preview** | `preview` |
| **Space** | `get_space` |
| **Cache** | `invalidate_cache`, `clear_cache` |

## License

Apache-2.0
