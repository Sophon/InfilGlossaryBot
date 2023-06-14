from urllib.request import urlopen
import json
import discord
from discord.ext import commands
import constants


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


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents, activity = discord.Game(name="use !glossary [TERM]"))
    my_glossary = get_full_glossary()

    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print('------')

    @bot.command()
    async def glossary(ctx, *, message):
        output = search_dictionary(my_glossary, message)
        await ctx.send(output)

    bot.run(constants.TOKEN)


main()
