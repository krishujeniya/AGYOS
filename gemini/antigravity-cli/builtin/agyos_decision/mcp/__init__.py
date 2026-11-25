"""MCP (Model Context Protocol) stdio server for Roxx (optional extra).

Install the extra to use it:

    pip install "roxx[mcp]"

Then run the server:

    roxx-mcp-server            # console script
    python -m roxx.mcp.server  # equivalent module form

The submodules ``device`` and ``tools`` are importable without the ``mcp``
dependency; ``server`` requires the extra.
"""

__all__ = ["device", "server", "tools"]
