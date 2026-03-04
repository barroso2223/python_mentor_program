# src/article_processor.py

from datetime import datetime, timezone
from src.config import SITE_CONFIGS, TARGET_ARTICLE_COUNT, OUTPUT_DIR_NAME
import os  # Needed for creating output directory later


# This function converts a raw timestamp string into a Python datetime object.
# It's crucial for validating the time-based order of articles.
def parse_iso_timestamp(iso_string: str | None) -> datetime | None:
    if not iso_string:  # If the input string is empty or None, we just return None.
        return None

    # Remove any extra spaces from the start/end of the string.
    cleaned_iso_string = iso_string.strip()
    # If the string contains a space (like "2026-02-20T... 12345"), we only take the first part.
    if " " in cleaned_iso_string:
        cleaned_iso_string = cleaned_iso_string.split(" ")[0]

    try:  # We use a try-except block to safely handle potential errors during date conversion.
        # Convert the cleaned string into a datetime object.
        # '.replace('Z', '+00:00')' helps handle UTC timezone format correctly.
        # '.astimezone(timezone.utc)' ensures it's always in UTC, which is best for comparisons.
        date_obj = datetime.fromisoformat(
            cleaned_iso_string.replace("Z", "+00:00")
        ).astimezone(timezone.utc)
        return date_obj  # If successful, return the datetime object.
    except (
        ValueError
    ):  # If 'fromisoformat' fails because the string isn't a valid date format...
        print(
            f'  ⚠️  Warning: Could not parse timestamp string: "{iso_string}". Returning None.'
        )
        return None  # ...print a warning and return None.
    except Exception as e:  # Catch any other unexpected errors during parsing.
        print(f'  ❌ Error parsing timestamp "{iso_string}": {e}')
        return None


# This function processes a list of raw article data (dictionaries).
# It applies any necessary transformations (like cleaning the timestamp string)
# and converts the raw timestamp into a proper datetime object.
def process_raw_articles(raw_articles: list[dict], site_key: str) -> list[dict]:
    # Get the specific configuration for the chosen site.
    config = SITE_CONFIGS.get(site_key)
    if (
        not config
    ):  # If the site config isn't found, print an error and return an empty list.
        print(f"Error: Config not found for {site_key}")
        return []

    processed_articles = []  # This list will hold our final, processed article data.
    transform_func = config["timestamp"][
        "transform"
    ]  # Get the 'transform' lambda function from our config.

    # We loop through each raw article dictionary in the 'raw_articles' list.
    for article_data in raw_articles:
        raw_ts = article_data.get(
            "rawTimestamp"
        )  # Get the raw timestamp string, or None if it's missing.

        # If we have a raw timestamp AND a transform function in our config...
        if raw_ts and transform_func:
            cleaned_ts = transform_func(
                raw_ts
            )  # ...apply the transform function to clean the timestamp string.
        else:  # Otherwise (no raw timestamp or no transform function)...
            cleaned_ts = raw_ts  # ...just keep the raw timestamp as is.

        parsed_ts = parse_iso_timestamp(
            cleaned_ts
        )  # Convert the (potentially cleaned) timestamp string into a datetime object.

        # Only add the article to our processed list if the timestamp was parsed successfully.
        if parsed_ts:
            # We create a new dictionary for the article, copying all its original data
            # and adding the new 'parsedTimestamp' datetime object.
            processed_articles.append(
                {
                    **article_data,  # This 'unpacks' all key-value pairs from 'article_data' into the new dictionary.
                    "parsedTimestamp": parsed_ts,
                }
            )
        else:  # If the timestamp couldn't be parsed...
            print(
                f"  ⚠️  Skipping article '{article_data.get('title', 'No Title')}' due to unreadable timestamp."
            )

    return processed_articles  # Return the list of articles with parsed timestamps.


# This function checks if a list of articles is sorted correctly from newest to oldest.
# It returns 'True' or 'False' for 'passed', and a list of detailed 'failures'.
def validate_sorting(articles: list[dict]) -> tuple[bool, list[str]]:
    passed = True  # We start by assuming the list is sorted correctly.
    failures = (
        []
    )  # This list will collect any error messages for out-of-order articles.

    # We loop through the list of articles from the first one up to the second-to-last one.
    for i in range(len(articles) - 1):
        curr = articles[i]  # The current article in the loop.
        next_item = articles[
            i + 1
        ]  # The article immediately following the current one.

        # This is the CORE VALIDATION LOGIC.
        # We compare the 'parsedTimestamp' (datetime objects) of the current and next articles.
        # If the current article's timestamp is OLDER than the next article's timestamp, they are out of order.
        if curr["parsedTimestamp"] < next_item["parsedTimestamp"]:
            passed = False  # Set 'passed' to False because we found an error.
            # Add a very detailed message to our 'failures' list, explaining exactly what went wrong.
            failures.append(
                f"  Position {i + 1} -> {i + 2}:\n"
                f"    \"{curr['title']}\"\n"
                f"    timestamp: {curr['rawTimestamp']}\n"
                f"    url:       {curr['url']}\n"
                f"    ...is OLDER than...\n"
                f"    \"{next_item['title']}\"\n"
                f"    timestamp: {next_item['rawTimestamp']}\n"
                f"    url:       {next_item['url']}"
            )
    return passed, failures  # Return whether the test passed and the list of failures.


# --- Main execution block for this script (runs when you execute this file directly) ---
if (
    __name__ == "__main__"
):  # This ensures the code inside only runs when this file is executed directly, not when imported.
    print("--- Simulating Python Data Processing ---")

    # Here we create some example 'raw' article data. Each article is a dictionary.
    # This simulates the kind of data we'd scrape from a website.
    raw_data_batch_1 = [
        {
            "id": 1,
            "title": "Old Article",
            "rawTimestamp": "2024-01-01T10:00:00Z 123",
            "url": "http://example.com/old",
        },
        {
            "id": 2,
            "title": "Newer Article",
            "rawTimestamp": "2024-01-01T10:10:00Z 456",
            "url": "http://example.com/newer",
        },
    ]
    raw_data_batch_2 = [
        {
            "id": 3,
            "title": "Even Newer",
            "rawTimestamp": "2024-01-01T10:20:00Z 789",
            "url": "http://example.com/even-newer",
        },
        {
            "id": 4,
            "title": "Invalid Time",
            "rawTimestamp": "NOT_A_DATE",
            "url": "http://example.com/bad-time",
        },  # This will cause a warning when parsed.
        {
            "id": 5,
            "title": "Latest",
            "rawTimestamp": "2024-01-01T10:30:00Z 101",
            "url": "http://example.com/latest",
        },
    ]

    # We combine our two batches of raw data into one long list.
    all_raw_articles = raw_data_batch_1 + raw_data_batch_2

    print(f"\nProcessing {len(all_raw_articles)} raw articles...")
    # We call our 'process_raw_articles' function to clean and parse the timestamps.
    processed_articles = process_raw_articles(all_raw_articles, "hackernews")
    print(f"Processed {len(processed_articles)} valid articles.")

    print("\nValidating sorting...")
    # We call our 'validate_sorting' function to check the order.
    # It returns two values: 'passed' (True/False) and 'failures' (a list of messages).
    passed, failures = validate_sorting(processed_articles)

    if passed:  # If 'passed' is True...
        print("✅ Simulation PASSED: Articles are correctly sorted.")
    else:  # Otherwise...
        print("❌ Simulation FAILED: Articles are NOT correctly sorted.")
        for f in failures:  # Loop through and print each failure message.
            print(f)

    print("\n--- Python Data Structures Examples ---")
    # --- Examples of Python Data Structures ---

    # Lists: Ordered collections of items.
    my_list = ["apple", "banana", "cherry"]
    print(f"List: {my_list}")
    for item in my_list:  # Loop through each item in the list.
        print(f"  - {item}")

    # Dictionaries: Collections of key-value pairs.
    my_dict = {"name": "Daniel", "role": "Engineer", "skill": "Python"}
    print(f"Dictionary: {my_dict}")
    for (
        key,
        value,
    ) in my_dict.items():  # Loop through both keys and values in the dictionary.
        print(f"  {key}: {value}")

    # Sets: Collections of UNIQUE items (duplicates are automatically removed).
    fruits_set = {"apple", "banana", "apple", "orange"}
    print(f"Set (removes duplicates): {fruits_set}")
    if "banana" in fruits_set:  # Check if an item is quickly present in the set.
        print("  'banana' is in the set.")
    else:
        print("  'banana' is NOT in the set.")
