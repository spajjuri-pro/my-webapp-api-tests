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
API tests will be saved in `report.html`.

## API Tests Implemented
- Test for fetching top stories
- Test for fetching a specific story by ID
- Test for fetching first comment of a top story

## Edge Cases covered
- Test for fetching a non-existent item
- Test for fetching null item
- Test for fetching invalid parameters
- Test for sql injection attempts
- Test for http security headers
- Test for rate limiting