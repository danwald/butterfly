.PHONY: test type lint clean build

test: type lint
	uv run pytest tests

type:
	uv run mypy src tests

lint:
	uv run pre-commit run --all-files
	uv run ruff check

build:
	uv build

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf dist/ build/ src/*.egg-info/
