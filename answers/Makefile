format:
	poetry run black .
	poetry run isort .
	poetry run ruff .

test:
	poetry run pytest

dev-api:
	uvicorn answers.entrypoints.api:app --reload