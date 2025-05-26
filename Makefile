.PHONY: test type lint clean

test: type lint
	uv run pytest tests

type:
	uv run mypy */*.py *.py

lint:
	uv run pre-commit run --all-files
	uv run ruff check

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
