import discord
from discord import app_commands
from discord.ext import commands
import infil_glossary
import constants
import utils


def create_embed(query, author="", avatar=""):
    term = utils.remove_mention_tag(query)
    print("searching for:" + term)
    item = infil_glossary.search_dictionary(my_glossary, term)
    description, tags = utils.search_and_replace(item["def"])

    embed = discord.Embed(
        title=term,
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

    embed.add_field(name="Source", value=utils.create_source(searched_term=term), inline=False)

    return embed, tags


my_glossary = infil_glossary.get_full_glossary()


class MyButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        embed, tags = create_embed(
            query=self.label,
            author=interaction.user.display_name,
            avatar=interaction.user.avatar.url
        )

        await interaction.response.send_message(embed=embed, view=ButtonsView(tags))


class ButtonsView(discord.ui.View):
    def __init__(self, labels: []):
        super().__init__()
        for label in labels:
            self.add_item(MyButton(label=label))


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=discord.Game(name="@me [TERM]")
        )

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.user.name}")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


bot = Bot()


# TAG TRIGGER
@bot.event
async def on_message(message):
    user = bot.user
    if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
        embed, tags = create_embed(
            query=message.content,
            author=message.author.display_name,
            avatar=message.author.avatar.url
        )

        await message.channel.send(embed=embed, view=ButtonsView(tags))


# SLASH TRIGGER
@bot.tree.command(name="glossary")
@app_commands.describe(query="term to search")
async def glossary(interaction: discord.Interaction, query: str):
    embed, tags = create_embed(
        query=query,
        author=interaction.user.display_name,
        avatar=interaction.user.avatar.url
    )

    await interaction.response.send_message(embed=embed, view=ButtonsView(tags))


bot.run(constants.TOKEN)
