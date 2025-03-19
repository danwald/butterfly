.PHONY: test type lint clean

test:
	uv run pytest tests

type:
	uv run mypy */*.py *.py

lint:
	uv run ruff check

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
