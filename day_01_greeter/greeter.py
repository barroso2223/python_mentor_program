import sys  # WHAT: Imports the 'sys' module. WHY: To access system-specific parameters and functions, specifically sys.exit() for clean program termination. HOW: The 'import' keyword makes module functions available.

# === Global Constants ===
# WHAT: A list data structure to store the names of months.
# WHY: Provides a mapping from month numbers (1-12) to their string names. Defined globally as its value is constant and needed by a function.
# HOW: Defined using square brackets `[]`. Index 0 is intentionally left empty so month numbers (1-12) can directly map to their list index.
# SECURITY: Read-only access ensures consistency.
# MISTAKES: Forgetting 0-indexing can lead to IndexError or incorrect month names.
MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# === Functions ===


def display_greeting(name, city):
    """
    WHAT: Defines a function named `display_greeting`.
    WHY: Encapsulates the logic for printing a personalized welcome message based on user-provided data.
         Promotes modularity and reusability.
    HOW: Takes `name` and `city` as parameters. Uses an f-string to format and print the message to the console.
    WHERE: Any interactive CLI application to greet users.
    SECURITY: Low direct risk, but be cautious if `name` or `city` contained sensitive data and was logged without care in a real system.
    MISTAKES: Forgetting to pass arguments, indentation errors.
    """
    print(f"Hello, {name}! I heard you're from {city}. That's cool!")


def process_birth_month_and_sign(month_number):
    """
    WHAT: Defines a function named `process_birth_month_and_sign`.
    WHY: Separates the logic for determining the month's name and a fun 'sign info' message based on a month number.
         It takes a *validated* month number and returns the derived string data.
    HOW: Takes `month_number` as a parameter. Initializes `sign_info_text` with a safe default.
         Accesses `MONTH_NAMES` globally. Uses `if/elif` statements for conditional logic.
         Returns two strings (packed into a tuple) representing the month name and sign info.
    WHERE: Used in applications where a numerical month needs to be translated into human-readable text and associated information.
           Called *after* the month number has been validated.
    SECURITY: Operates on `month_number` which is assumed to be already validated (1-12) by `get_valid_month_input()`.
              This is a good design: validation at input boundary, processing inside.
    MISTAKES: Incorrect conditional logic, forgetting to initialize local variables before use, forgetting to return values.
    """
    # WHAT: Local variable, initialized with a safe, user-friendly default string.
    # WHY: Ensures it always has a value before being returned, even if a logic path is missed.
    # HOW: Standard string assignment.
    sign_info_text = "No special sign info available."

    # WHAT: Assigns the correct month name.
    # WHY: Given that `month_number` is already validated (1-12), we can directly access the list.
    # HOW: Accesses the global `MONTH_NAMES` list using `month_number` as the index.
    birth_month_name = MONTH_NAMES[month_number]

    # WHAT: Determines the 'sign info' text based on the month quarter.
    # WHY: Provides a fun, personalized message.
    # HOW: Uses a series of `if/elif` statements (conditional logic) to check the range of `month_number`.
    if 1 <= month_number <= 3:
        sign_info_text = "You're an early bird, true pioneer!"
    elif 4 <= month_number <= 6:
        sign_info_text = "You're blossoming like spring, full of growth!"
    elif 7 <= month_number <= 9:
        sign_info_text = "You're a warm summer soul, full of bright ideas!"
    elif 10 <= month_number <= 12:
        sign_info_text = "You're a reflective autumn spirit, wise and deep!"
    # An 'else' here (for month_number outside 1-12) is not strictly needed as
    # get_valid_month_input ensures the number is always 1-12.

    # WHAT: Returns the two calculated string values.
    # WHY: Provides the results of this function's work back to its caller.
    # HOW: The `return` keyword with comma-separated variables, which Python packs into a tuple.
    return birth_month_name, sign_info_text


def get_valid_month_input():
    """
    WHAT: Defines a function named `get_valid_month_input`.
    WHY: To robustly prompt the user for a month number (1-12), handling both non-numeric
         and out-of-range inputs gracefully with dynamic and specific feedback.
         Centralizes validation logic.
    HOW: Uses a 'while True' loop for repetition, 'try-except' for catching conversion errors,
         and nested conditional logic to manage retry attempts and distinct dynamic feedback.
         Returns a validated integer or exits the program after too many invalid attempts.
    WHERE: Any CLI application needing robust, validated numerical input.
    SECURITY: CRITICAL for input validation (establishing a trust boundary), DoS prevention,
              and preventing information leakage (no raw tracebacks).
    MISTAKES: Incorrect retry logic, vague error messages, not using `sys.exit()` for critical failures.
    """
    retry_count = (
        0  # WHAT: Local variable, initialized to 0. WHY: Tracks invalid user attempts.
    )
    MAX_RETRIES = 3  # WHAT: Local constant. WHY: Defines the maximum number of retries before exiting.

    # WHAT: Predefined sets of messages for clarity and maintainability. (New Data Structure: Dictionaries)
    # WHY: Allows for truly distinct and dynamic messages without redundant string concatenation.
    # HOW: Each dictionary key (1, 2, 3) corresponds to the retry count, mapping to a specific message.
    NON_NUMERIC_MESSAGES = {
        1: "Error: Input must be a whole number (e.g., 1 for January). Please try again.",
        2: "Still non-numerical. Remember, just digits, like '5' or '12'.",
        3: "Too many non-numerical attempts. Please focus on entering a number.",
    }
    OUT_OF_RANGE_MESSAGES = {
        1: "Error: Month must be a number between 1 and 12. Please try again.",
        2: "Still out of range. Check the numbers: 1=Jan, 12=Dec.",
        3: "Too many out-of-range attempts. The number must be between 1 and 12.",
    }

    while (
        True
    ):  # WHAT: An infinite loop. WHY: Continuously asks for input until valid or max retries.
        month_input_str = input(
            "What month were you born in (1-12)? "
        )  # WHAT: Gets raw string input.

        current_error_type = None  # WHAT: Local variable, initialized to None. Stores an internal code ("non_numeric" or "out_of_range") for the error.

        try:  # WHAT: 'try' block. WHY: Protects code that might raise a ValueError.
            month_input_int = int(
                month_input_str
            )  # WHAT: Attempts string to integer conversion.

            # WHAT: Checks if number is OUTSIDE the valid range 1-12.
            # WHY: This is a logical validation check after successful type conversion.
            if not (1 <= month_input_int <= 12):
                current_error_type = "out_of_range"  # WHAT: Sets internal error code.

        except (
            ValueError
        ):  # WHAT: Catches ValueError (if int() failed due to non-numeric input).
            current_error_type = "non_numeric"  # WHAT: Sets internal error code.

        # --- Centralized Error Handling and Retry Logic ---
        if (
            current_error_type
        ):  # WHAT: If 'current_error_type' is not None (meaning an error occurred).
            retry_count += (
                1  # WHAT: Increments retry_count. WHY: Tracks this invalid attempt.
            )

            final_message_for_user = ""  # WHAT: Local variable to build the final error message for this attempt.

            # WHAT: Conditional logic to select the correct set of messages based on error type.
            # WHY: Ensures distinct, non-redundant messages for different error categories.
            if current_error_type == "non_numeric":
                # WHAT: Retrieves the message for the current retry_count from the dictionary.
                # WHY: `get()` with a default fallback (using `NON_NUMERIC_MESSAGES[MAX_RETRIES]`) handles `retry_count` > MAX_RETRIES.
                final_message_for_user = NON_NUMERIC_MESSAGES.get(
                    retry_count, NON_NUMERIC_MESSAGES[MAX_RETRIES]
                )

            elif current_error_type == "out_of_range":
                final_message_for_user = OUT_OF_RANGE_MESSAGES.get(
                    retry_count, OUT_OF_RANGE_MESSAGES[MAX_RETRIES]
                )

            # WHAT: Check if max retries reached AFTER selecting the message.
            # WHY: Ensures the user sees the final, specific error message before program termination.
            if retry_count >= MAX_RETRIES:
                print(
                    f"Too many invalid attempts: {final_message_for_user} Exiting program."
                )  # WHAT: Prints final exit message.
                sys.exit(1)  # WHAT: Terminates script with error code 1 (failure).

            print(
                final_message_for_user
            )  # WHAT: Prints the dynamic, specific error message for the current retry.

        else:  # WHAT: 'else' for 'if current_error_type:'. WHY: This path means input was fully valid.
            return month_input_int  # WHAT: Returns the valid integer. WHY: Successful exit from function and loop.


# === Main Program Execution ===
# WHAT: The main script flow. This orchestrates the program by calling functions.

print("Welcome to the Enhanced Greeter Program!")  # WHAT: Initial welcome.

user_name = input("Please enter your name: ")  # WHAT: Gets user name.
user_city = input("Where are you from? ")  # WHAT: Gets user city.

display_greeting(
    user_name, user_city
)  # WHAT: Calls display_greeting to show personalized welcome.

# WHAT: Calls validation function. WHY: Ensures we get a GUARANTEED VALID month number (1-12).
birth_month_int = get_valid_month_input()

# WHAT: Calls processing function and unpacks its two returned string values.
# WHY: Captures the month name and sign info into separate, local variables in the main script's scope.
final_birth_month_name, final_sign_info_text = process_birth_month_and_sign(
    birth_month_int
)

# WHAT: Prints the final personalized output using all collected and processed information.
print(
    f"\nOkay, {user_name}, based on your birth month ({final_birth_month_name}), {final_sign_info_text}"
)
print("Remember, this is just for fun and learning!")  # WHAT: Closing message.
