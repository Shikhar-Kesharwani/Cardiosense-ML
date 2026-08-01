.PHONY: install run train test setup-r2 clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python app.py

train:
	python -m src.Heart.pipeline.Training_pipeline

test:
	python tests/check_accuracy_fixed.py

setup-r2:
	python scripts/setup_r2.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
