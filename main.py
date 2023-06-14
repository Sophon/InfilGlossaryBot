import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import discord_util
import utils


async def output(message, glossary):
    term = utils.remove_tag(message.content)
    item = infil_glossary.search_dictionary(glossary, term)
    embed = discord_util.create_full_embed(
        title=term,
        item=item,
        color=discord.Color.blue(),
        author=message.author.display_name,
        avatar=message.author.avatar.url
    )
    await message.channel.send(embed=embed)


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"),
        intents=intents,
        activity=discord.Game(name="@me [TERM]")
    )
    my_glossary = infil_glossary.get_full_glossary()

    @bot.event
    async def on_ready():
        print(f"Bot is ready. Logged in as {bot.user.name}")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        user = bot.user
        if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
            await output(message, my_glossary)

    @bot.tree.command(name="glossary")
    @app_commands.describe(term="term to search")
    async def glossary(interaction: discord.Interaction, term: str):
        item = infil_glossary.search_dictionary(my_glossary, term)
        embed = discord_util.create_lite_embed(
            title=term,
            item=item,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    bot.run(constants.TOKEN)


main()

