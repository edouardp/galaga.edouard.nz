# Makefile for galaga.edouard.nz
#
# Usage:
#   make              Show all available targets
#   make <target>     Run a specific target

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# Setup and Installation
# ============================================================================

.PHONY: install
install: ## Install dependencies with uv
	uv sync

# ============================================================================
# Development
# ============================================================================

.PHONY: edit
edit: ## Open marimo editor for a notebook (usage: make edit NB=hello)
	@if [ -z "$(NB)" ]; then echo "Usage: make edit NB=<notebook_name>"; exit 1; fi
	uv run marimo edit --sandbox notebooks/$(NB).py

.PHONY: new
new: ## Create a new notebook (usage: make new NB=my_notebook)
	@if [ -z "$(NB)" ]; then echo "Usage: make new NB=<notebook_name>"; exit 1; fi
	uv run marimo edit --sandbox notebooks/$(NB).py

# ============================================================================
# Build
# ============================================================================

.PHONY: build
build: ## Build all notebooks to WASM HTML in dist/
	./scripts/build.sh

.PHONY: build-run
build-run: ## Build notebooks in read-only mode
	MARIMO_MODE=run ./scripts/build.sh

# ============================================================================
# Local Testing
# ============================================================================

.PHONY: serve
serve: build ## Build and serve locally on http://localhost:9191
	@echo "Serving at http://localhost:9191"
	@(sleep 2 && open http://localhost:9191) &
	uv run python -m http.server 9191 -d dist

.PHONY: serve-only
serve-only: ## Serve dist/ without rebuilding
	@echo "Serving at http://localhost:9191"
	@(sleep 2 && open http://localhost:9191) &
	uv run python -m http.server 9191 -d dist

# ============================================================================
# Deployment
# ============================================================================

.PHONY: deploy
deploy: ## Build and deploy to galaga.edouard.nz
	./scripts/deploy.sh

.PHONY: deploy-only
deploy-only: ## Deploy without rebuilding (uses existing dist/)
	./scripts/deploy.sh --skip-build

.PHONY: infra
infra: ## Deploy CloudFormation infrastructure stack
	./scripts/infra.sh

# ============================================================================
# Cleanup
# ============================================================================

.PHONY: clean
clean: ## Remove build artifacts
	rm -rf dist/

# ============================================================================
# Default Target
# ============================================================================

.DEFAULT_GOAL := help
