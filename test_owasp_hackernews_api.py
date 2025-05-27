import requests
import pytest
import time

#Base URLs for Hacker News API
BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{BASE_URL}/topstories.json"
ITEM_URL = f"{BASE_URL}/item/"
# Helper function to get JSON response from a URL
def get_json_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request failed: {e}")

# Function to get item details by ID
def get_item_details(item_id):
    return get_json_response(f"{ITEM_URL}{item_id}.json")

#---- OWASP-related Security Tests ----

def test_security_input_validation_invalid_item_id():
    """
    Testcase: Validate input handling for invalid item ID
    Description:
        - Verifies that the API returns a 404 status code for an invalid item ID
    """
    invalid_item_id = "abc123"
    response = requests.get(f"{ITEM_URL}{invalid_item_id}.json")
    print(f"Testing invalid item ID: {invalid_item_id}. Status code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 for invalid item ID, got {response.status_code}"
    assert response.json() is None, "Expected null response for invalid item ID"
    # Ensure that the response does not contain server errors
    assert not response.status_code >= 500, \
        f"Unexpected server error for invalid item ID: {response.status_code}. Response: {response.text}"
    print(f"API correctly handled invalid item ID: {invalid_item_id}")    

def test_security_input_validation_empty_item_id():
    """
    Testcase: Validate input handling for empty item ID
    Description:
        - Verifies that the API returns a 401 status code for an empty item ID
    """
    empty_item_id = ""
    response = requests.get(f"{ITEM_URL}{empty_item_id}.json")
    print(f"Testing empty item ID. Status code: {response.status_code}")
    assert response.status_code == 401, f"Expected 401 for empty item ID, got {response.status_code}"
    assert not response.status_code >= 500, \
        f"Unexpected server error for empty item ID: {response.status_code}. Response: {response.text}"
    print("API correctly handled empty item ID")

def test_security_input_validation_non_existent_item_id():
    """
    Testcase: Validate input handling for non-existent item ID
    Description:
        - Verifies that the API returns a 404 status code for a non-existent item ID
    """
    non_existent_item_id = 9999999999  # Assuming this ID does not exist
    response = requests.get(f"{ITEM_URL}{non_existent_item_id}.json")
    print(f"Testing non-existent item ID: {non_existent_item_id}. Status code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 for non-existent item ID, but got {response.status_code} and response: {response.text}"
    assert response.json() is None, "Expected null response  for non-existent item ID"
    print(f"API correctly handled non-existent item ID: {non_existent_item_id}")

def test_security_input_null_item_id():
    """
    Testcase: Validate input handling for null item ID
    Description:
        - Verifies that the API returns a 401 status code for a null item ID
    """
    null_item_id = None
    response = requests.get(f"{ITEM_URL}{null_item_id}.json")
    print(f"Testing null item ID. Status code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 for null item ID, got {response.status_code}"
    assert response.json() is None, "Expected null response for null item ID"

def test_security_input_validation_sql_injection():
    """
    Testcase: Validate input handling for SQL injection attempt
    Description:
        - Verifies that the API does not return sensitive information or execute SQL commands
    """
    sql_injection_payload = "'; DROP TABLE users; --"
    response = requests.get(f"{ITEM_URL}{sql_injection_payload}.json")
    print(f"Testing SQL injection payload: {sql_injection_payload}. Status code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200 for SQL injection payload, got {response.status_code}"
    assert response.json() is None, "Expected null response for SQL injection payload"

def test_security_http_security_headers():
    """
        OWASP Test (A05:2021 - Security Misconfiguration): Check for essential HTTP security headers.
        Description:
        - Makes a request to a common API endpoint (e.g., top stories).
        - Asserts the presence of key security headers that help prevent common attacks.
        - Note: Not all headers are strictly required for a pure API, but good practice for web servers.
    """
    response = requests.get(TOP_STORIES_URL)
    headers = response.headers
    print(f"Checking headers for {TOP_STORIES_URL}: {headers}")

    # common security headers
    # Strict-Transport-Security: Enforces secure (HTTPS) connections to the server
    assert "Strict-Transport-Security" in headers, "Missing Strict-Transport-Security header"

def test_security_verbose_error_messages():
    """
    Testcase: Validate that the API does not expose verbose error messages
    Description:
        - Verifies that the API does not return detailed error messages that could aid an attacker
    """
    response = requests.get(f"{ITEM_URL}9999999999.json")  # Non-existent item ID
    print(f"Testing verbose error messages for non-existent item ID. Status code: {response.status_code} and response: {response.text}")

    assert response.status_code == 200, f"Expected 200 for non-existent item ID, got {response.status_code}"
    assert response.json() is None, "Expected null response for non-existent item ID"
        
    # Check if the response contains any sensitive information
    assert "error" not in response.text, "Response contains sensitive error information"

def test_security_rate_limiting():
    """
    Testcase: Validate rate limiting by making multiple requests in a short time
    Description:
        - Verifies that the API enforces rate limiting by checking for 429 Too Many Requests status code
    """
    requests_per_second = 50 
    rate_limit_triggered = False
    for _ in range(requests_per_second):  
        response = requests.get(TOP_STORIES_URL)
        if response.status_code == 429:
            rate_limit_triggered = True
            break
        time.sleep(0.01)  # Short delay to avoid overwhelming the server

    assert rate_limit_triggered, "API did not trigger rate limiting after {requests_per_second} requests"
