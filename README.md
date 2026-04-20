# personal-notes-mcp

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server that lets an MCP-aware client (e.g. Claude Desktop, Claude Code) manage a local folder of Markdown notes.

Notes are stored as `.md` files with YAML frontmatter under `~/claude-notes/`.

## Requirements

- Python >= 3.11
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

## Installation

```bash
uv sync
```

or with pip:

```bash
pip install -e .
```

## Running the server

```bash
uv run python -m personal_notes_mcp.server
```

## Tools

| Tool | Description |
| --- | --- |
| `create_note(title, content, tags=[])` | Create a new note. Filename is derived from a slugified title. Tags and title are written as frontmatter. |
| `search_notes(query)` | Substring search across note content and titles. Returns file, title, and a 200-char preview. |
| `list_notes()` | List all note filenames in the notes directory. |

## Claude Desktop configuration

Add the following to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "personal-notes": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/Repositories/personal-notes-mcp",
        "run",
        "python",
        "-m",
        "personal_notes_mcp.server"
      ]
    }
  }
}
```

## Storage

All notes live in `~/claude-notes/` (created on first run). Each file looks like:

```markdown
---
title: My note
tags:
  - ideas
---
Note body goes here.
```
