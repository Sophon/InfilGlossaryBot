import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import discord_util
import utils


def output_embed(term, glossary, author, avatar):
    term = utils.remove_tag(term)
    item = infil_glossary.search_dictionary(glossary, term)
    return discord_util.create_embed(
        title=term,
        item=item,
        color=discord.Color.blue(),
        author=author,
        avatar=avatar
    )


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(
        command_prefix=commands.when_mentioned,
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
            embed = output_embed(
                term=message.content,
                glossary=my_glossary,
                author=message.author.display_name,
                avatar=message.author.avatar.url
            )
            await message.channel.send(embed=embed)

    @bot.tree.command(name="glossary")
    @app_commands.describe(term="term to search")
    async def glossary(interaction: discord.Interaction, term: str):
        embed = output_embed(
            term=term,
            glossary=my_glossary,
            author=interaction.user.display_name,
            avatar=interaction.user.avatar.url
        )
        await interaction.response.send_message(embed=embed)

    bot.run(constants.TOKEN)


main()

