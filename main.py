from urllib.request import urlopen
import json


def get_full_glossary():
    print("DEBUG: getting the glossary\n\n")

    url = "https://glossary.infil.net/json/glossary.json"
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


def search_dictionary(dictionary, term):
    cleaned_input = clean_string(term)
    for item in dictionary:
        if cleaned_input == item["term"]:
            return item["def"]

    return "Not found"


def read_input():
    return input()


term1 = "fireball"
term2 = "FireBall"
term3 = "fireBall__"

glossary = get_full_glossary()

while True:
    print("write the term: ")
    print(search_dictionary(glossary, read_input()))
    print()
