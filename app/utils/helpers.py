# Define a function to convert a string to snake case
from re import sub


def snake_case(s):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return '_'.join(sub('([A-Z][a-z]+)', r' \1', sub('([A-Z]+)', r' \1', s.replace('-', ' '))).split()).lower()


def convert_keys_to_snake_case(data):
    if isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    elif isinstance(data, dict):
        return {snake_case(key): convert_keys_to_snake_case(value) for key, value in data.items()}
    else:
        return data
