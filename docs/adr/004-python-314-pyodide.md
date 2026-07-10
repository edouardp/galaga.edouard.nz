# ADR-004: Python 3.14 and Pyodide

## Status

Accepted

## Context

The galaga library uses Python 3.14's [t-strings (PEP 750)](https://peps.python.org/pep-0750/) for its marimo integration (`galaga-marimo`). T-strings provide template strings with deferred evaluation, enabling the library to render mathematical expressions inline in marimo markdown cells with proper escaping and formatting.

Pyodide (the CPython-to-WebAssembly port) added Python 3.14 support, making it possible to run t-string-dependent code in the browser.

## Decision

Target Python 3.14+ as the minimum version. This is declared in:
- `pyproject.toml` (`requires-python = ">=3.14"`)
- `.python-version` (`3.14`)
- Notebook script metadata (`requires-python = ">=3.14"`)

The marimo WASM export uses Pyodide's Python 3.14 build, which is selected automatically when exporting notebooks that declare `>=3.14`.

## Consequences

- The galaga-marimo library can use t-strings for ergonomic template rendering
- Notebooks can use any Python 3.14 feature (including t-strings, `@` operator improvements, etc.)
- Developers need Python 3.14 installed locally (via `uv python install 3.14`)
- Some packages may not yet have wheels for 3.14 — Pyodide builds them from source or uses pure-Python fallbacks
- Ties the project to the bleeding edge; will need to track Pyodide's 3.14 support for any regressions
