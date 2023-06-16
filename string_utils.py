import constants
import re


def clean_string(string):
    words = string.split()
    transformed_words = []
    for word in words:
        if word.isalpha():
            transformed_words.append(word.capitalize())
    transformed_string = ' '.join(transformed_words)
    return transformed_string


def wrap_link(string):
    return "<" + string + ">"


def create_source(searched_term):
    return "\nSource: " + wrap_link(constants.URL + "?t=" + searched_term.replace(" ", "%20")) \
        + "\nCode: " + wrap_link(constants.GITHUB)


def create_gfycat_link(link_code):
    return constants.GFYCAT + "/" + link_code


def remove_mention_tag(string):
    return re.sub(r'<@(.*?)>', '', string)


def get_all_substrings(string, delim):
    substrings = []
    start_index = 0
    while True:
        start_index = string.find(delim, start_index)
        if start_index == -1:
            break
        end_index = string.find(delim, start_index + 1)
        if end_index == -1:
            break
        substrings.append(string[start_index + 1:end_index])
        start_index = end_index + 1
    return substrings


def search_and_replace(string):
    regex_pattern = r'!<.*?>'
    matches = re.findall(regex_pattern, string)
    occurrences = []
    for match in matches:
        tag = get_all_substrings(match[2:-1], "'")[-1]
        occurrences.append(tag)
        string = string.replace(match, tag)
    return string, occurrences
