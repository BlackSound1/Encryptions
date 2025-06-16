SHELL := bash
.ONESHELL:
.DEFAULT_GOAL := help

FORMAT := .
LINT := .

EXCLUDE_PATTERNS := .git,__pycache__,.venv,*.egg-info,build,dist

.PHONY: format
format:  ## Format a specified file/ directory. [Default is .]
	@echo Formatting using Black
	@uv run black --extend-exclude="($(EXCLUDE_PATTERNS))" --line-length=120 "${FORMAT}"
	@echo ""

.PHONY: lint
lint:  ## Lint a specified file/ directory. [Default is .]
	@echo Linting using Flake8
	@uv run flake8 --exclude="$(EXCLUDE_PATTERNS)" --max-line-length=120 "${LINT}"
	@echo ""

.PHONY: help
help:   ## Show this help
	@echo -e "\nCommands:\n"
	@egrep '^[a-zA-Z_-]+:.*?## .*' Makefile | sort |
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""
