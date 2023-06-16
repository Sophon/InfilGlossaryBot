import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import utils


def create_embed(title, description, item, author, avatar):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )
    embed.set_author(name=author, icon_url=avatar)

    if 'games' in item:
        embed.add_field(name="Games", value=item["games"], inline=True)

    if 'altterm' in item:
        embed.add_field(name="Synonyms", value=item["altterm"], inline=True)

    if 'video' in item:
        link = utils.create_gfycat_link(item["video"][0])
        embed.add_field(name="Gif", value=utils.wrap_link(link), inline=False)

    embed.add_field(name="Source", value=utils.create_source(searched_term=title), inline=False)

    return embed


my_glossary = infil_glossary.get_full_glossary()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=intents,
    activity=discord.Game(name="@me [TERM]")
)


@bot.event
async def on_ready():
        print(f"Bot is ready. Logged in as {bot.user.name}")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


# TAG TRIGGER
@bot.event
async def on_message(message):
    user = bot.user
    if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
        term = utils.remove_mention_tag(message.content)
        item = infil_glossary.search_dictionary(my_glossary, term)
        description, tags = utils.search_and_replace(item["def"])

        embed = create_embed(
            title=term,
            description=description,
            item=item,
            author=message.author.display_name,
            avatar=message.author.avatar.url
        )

        await message.channel.send(embed=embed)


# SLASH TRIGGER
@bot.tree.command(name="glossary")
@app_commands.describe(query="term to search")
async def glossary(interaction: discord.Interaction, query: str):
    term = utils.remove_mention_tag(query)
    item = infil_glossary.search_dictionary(my_glossary, term)
    description, tags = utils.search_and_replace(item["def"])

    embed = create_embed(
        title=term,
        description=description,
        item=item,
        author=interaction.user.display_name,
        avatar=interaction.user.avatar.url
    )

    await interaction.response.send_message(embed=embed)

bot.run(constants.TOKEN)



