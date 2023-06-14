from urllib.request import urlopen
import json
import constants
import utils


def get_full_glossary():
    print("DEBUG: getting the glossary\n\n")

    url = constants.JSON_URL
    response = urlopen(url)
    return json.loads(response.read())


def add_source(string):
    return "\n========"\
        + "\nsource: " + utils.wrap_link(constants.URL + "?t=" + string.replace(" ", "%20")) \
        + "\nBug reports: " + utils.wrap_link(constants.GITHUB)


def search_dictionary(dictionary, term):
    cleaned_input = utils.clean_string(term)
    for item in dictionary:
        if cleaned_input == item["term"]:
            query = item["def"]
            return query + add_source(term)

    return "Not found"
