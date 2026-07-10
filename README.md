# galaga.edouard.nz

Interactive [marimo](https://marimo.io) notebooks running Python 3.14 in the browser via WebAssembly (Pyodide). No backend server — everything executes client-side.

## Quick Start

```bash
make help             # Show all available commands
make install          # Install dependencies (uv sync)
make edit NB=hello    # Edit a notebook in marimo editor
make deploy           # Build and deploy to galaga.edouard.nz
```

## Documentation

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System architecture
- **[docs/adr/](docs/adr/)** — Architectural Decision Records

## Commands

| Command | Description |
| --- | --- |
| `make install` | Install dependencies |
| `make edit NB=name` | Open notebook in marimo editor |
| `make new NB=name` | Create a new notebook |
| `make build` | Export all notebooks to WASM HTML |
| `make serve` | Build and serve locally |
| `make deploy` | Build and deploy to production |
| `make deploy-only` | Deploy without rebuilding |
| `make infra` | Deploy CloudFormation stack (one-time) |
| `make clean` | Remove build artifacts |

## Adding a Notebook

```bash
make new NB=my_notebook   # Opens marimo editor
# ... develop ...
make deploy               # Push to production
```

Notebooks use `--sandbox` mode — dependencies are declared inline via [PEP 723](https://peps.python.org/pep-0723/) script metadata and automatically installed in the WASM environment.

## Project Structure

```text
├── notebooks/              # Marimo notebook .py files
├── scripts/
│   ├── build.sh            # Export notebooks to WASM HTML
│   ├── deploy.sh           # Build + sync to S3 + invalidate CloudFront
│   ├── infra.sh            # Deploy CloudFormation stack
│   └── generate_index.py   # Generate landing page + patch runtime template
├── infrastructure.yaml     # CloudFormation (S3, CloudFront, Lambda@Edge, DNS)
├── Makefile                # Developer commands
└── pyproject.toml          # Python project metadata
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (dependency management)
- AWS CLI (for deployment)
