import constants


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
