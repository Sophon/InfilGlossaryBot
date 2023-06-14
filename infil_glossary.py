from urllib.request import urlopen
import json
import constants


def get_full_glossary():
    print("DEBUG: getting the glossary\n\n")

    url = constants.JSON_URL
    response = urlopen(url)
    return json.loads(response.read())


def clean_string(string):
    words = string.split()
    transformed_words = []
    for word in words:
        if word.isalpha():
            transformed_words.append(word.capitalize())
    transformed_string = ' '.join(transformed_words)
    return transformed_string


def add_source(string):
    return "\n========"\
        + "\nsource: " + "<" + constants.URL + "?t=" + string.replace(" ", "%20") + ">" \
        + "\nBug reports: " + "<" + constants.GITHUB + ">"


def search_dictionary(dictionary, term):
    cleaned_input = clean_string(term)
    for item in dictionary:
        if cleaned_input == item["term"]:
            query = item["def"]
            return query + add_source(term)

    return "Not found"
