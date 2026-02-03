.PHONY: venv test format clean

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && PYTHONPATH=. python3 -m unittest discover tests

format:
	. .venv/bin/activate && black .

clean:
	rm -rf .venv build dist *.egg-info __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
