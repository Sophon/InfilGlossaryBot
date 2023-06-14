from urllib.request import urlopen
import json
import constants
import utils
import logger


def get_full_glossary():
    print("DEBUG: getting the glossary\n\n")

    url = constants.JSON_URL
    response = urlopen(url)
    return json.loads(response.read())


def search_dictionary(dictionary, term):
    cleaned_input = utils.clean_string(term)
    for item in dictionary:
        if cleaned_input == item["term"]:
            return item
        if 'altterm' in item:
            for alt in item["altterm"]:
                if cleaned_input == utils.clean_string(alt):
                    return item

    return "Not found"
