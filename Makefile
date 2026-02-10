all: remove_build_folder install_libs run_code_checkers

remove_build_folder:
	rm -rf build/

install_libs:
	uv run pip install -e .

run_code_checkers:
	uv run isort .
	uv run ruff check --fix .
	uv run mypy .