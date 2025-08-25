run:
	uv run eogtouch

setup-dev:
	uv pip install -e .[dev]

sync:
	rm uv.lock
	uv sync

lab:
	jupyter lab
