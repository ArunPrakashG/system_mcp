# system-mcp-wrapper

A tiny PyPI package that exposes the `system-mcp` CLI.

This package depends on the GitHub repo `ArunPrakashG/system_mcp` at a tagged version and simply re-exports the console script entrypoint, so you can `pip install system-mcp-wrapper` from PyPI and call `system-mcp`.

## Installation (PyPI)

```bash
pip install system-mcp-wrapper
```

## Usage

```bash
system-mcp --transport stdio
```

For advanced usage, refer to the upstream repository README.
