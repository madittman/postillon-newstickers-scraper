all: uv_sync remove_build_folder run_pip run_code_checkers

uv_sync:
	uv sync

remove_build_folder:
	rm -rf build/

run_pip:
	pip install --upgrade pip
	uv run pip install -e .

run_code_checkers:
	uv run isort .
	uv run black .
	uv run ruff check --fix .
	uv run mypy .
