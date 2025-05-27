import requests
import pytest

BASE_URL = "https://hacker-news.firebaseio.com/v0/"
TOP_STORIES_URL= f"{BASE_URL}/topstories.json"
ITEM_URL= f"{BASE_URL}/item/"

#--- Helper functions ---
def get_response_json(url):
    try:
        response= requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request failed : {e}")

def get_items(item_id):
    return get_response_json(f"{ITEM_URL}{item_id}.json")

def test_retrieve_top_stories_success():
    """
    Testcase: Retrieve the top stories using topstories API
    Description
        - Verifies the Topstories returns list of story IDs
        - Verifies that length of the Topstories list is not null
        - Verifies that topstory ID is an integer by checking few items in the Topstories list

    """

    top_story_ids = get_response_json(TOP_STORIES_URL)

    assert isinstance(top_story_ids, list)
    assert len(top_story_ids) > 0
    print(f"{len(top_story_ids)} Top stories retrieved")

    for i in range(min(5, len(top_story_ids))):
        assert isinstance(top_story_ids[i], int), f"Element at {i} is not an integer"
    print("Top stories contains integers IDs")

def test_get_top_stories_details():
    """
    Testcase: Using Top stories API to retrieve the current top story from the Items API
        - Verifies top stories not null and gets ID of the current top story
        - Verifies Top story details from Items API is a Dictionary
        - Verifies "id" value of item details is current top story ID
        - Verifies 'type' and 'title' fields are part of item details
    :return:
    """
    top_story_ids = get_response_json(TOP_STORIES_URL)
    assert len(top_story_ids) > 0, "Top Stories item list is empty"
    first_top_story_id = top_story_ids[0]

    items_details = get_items(first_top_story_id)

    assert isinstance(items_details,dict) , "Item details response is not a dict"
    assert items_details.get('id')==first_top_story_id , "Item ID mismatch"
    assert 'type' in items_details, "Item details is missing 'type' field"
    assert 'title' in items_details, "Item details is missing 'title' field"
    print(f"Item details are successfully retrieved for story {items_details.get('title')}")









