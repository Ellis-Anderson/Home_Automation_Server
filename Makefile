MAX_LINE_LENGTH=120

.PHONY: help
help: ## Show this help
	@echo "Some useful developer shortcuts (Try tab autocomplete for make!)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' --no-filename $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; { printf "\033[36m%-15s\033[0m %s\n", $$1, $$2 }'

.PHONY: tidy
tidy: ## Restyle with 'black' and sort imports with 'isort'
	black . --line-length ${MAX_LINE_LENGTH}
	isort . --profile black --force-alphabetical-sort-within-sections

.PHONY: lint
lint: tidy ## Run linters
	flake8 --max-line-length ${MAX_LINE_LENGTH}
	mypy . --disallow-untyped-defs --ignore-missing-imports
