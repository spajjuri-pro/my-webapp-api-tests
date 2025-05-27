# my-webapp-api-tests

This project is designed to test the public Hackernews API.

## Dev Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Activate the virtual environment
pip install -r requirements.txt
```

## How to Run Tests

```bash
pytest <test_file>
```

## How to View Results

To generate an HTML report, run:

```bash
pytest -v --html=report.html --self-contained-html
```