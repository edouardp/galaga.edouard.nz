# galaga.edouard.nz

Interactive [marimo](https://marimo.io) notebooks running Python 3.14 in the browser via WebAssembly.

## Quick Start

```bash
make install          # Install dependencies (uv sync)
make edit NB=hello    # Edit a notebook in marimo editor
make serve            # Build and serve locally at http://localhost:8000
```

## Workflow

1. Create/edit notebooks in `./notebooks/`
2. `make deploy` to build and push to galaga.edouard.nz

## Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make edit NB=hello` | Open a notebook in marimo editor |
| `make new NB=name` | Create a new notebook |
| `make build` | Export all notebooks to WASM HTML |
| `make serve` | Build and serve locally |
| `make deploy` | Build and deploy to galaga.edouard.nz |
| `make infra` | Deploy AWS infrastructure (one-time) |
| `make clean` | Remove build artifacts |

## Infrastructure

Hosted on AWS (S3 + CloudFront):

- `infrastructure.yaml` — CloudFormation template
- `scripts/infra.sh` — Deploy the infrastructure stack (run once)
- `scripts/deploy.sh` — Build notebooks and sync to S3 + invalidate cache
- `scripts/build.sh` — Export notebooks to WASM HTML

## Adding a Notebook

```bash
make new NB=my_analysis     # Opens marimo editor
# ... develop your notebook ...
make deploy                 # Push to production
```

Notebooks use `--sandbox` mode so dependencies are inlined into the file and automatically installed in the WASM environment.
