import discord
from discord.ext import commands
import infil_glossary
import constants
import datetime
import logger


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="!glossary [TERM]"))
    my_glossary = infil_glossary.get_full_glossary()

    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print('------')

    @bot.command()
    async def glossary(ctx, *, message):
        output = infil_glossary.search_dictionary(my_glossary, message)
        await ctx.send(output)

    bot.run(constants.TOKEN)


main()
logger.log_call_count_of(function=infil_glossary.search_dictionary, rate=constants.RATE_OF_LOGGING)
