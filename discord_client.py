import discord
from discord import app_commands
import infil_glossary
import string_utils
from typing import (
    Any,
)


class DiscordClient(discord.Client):
    __my_glossary = infil_glossary.get_full_glossary()
    tags = []

    intents: discord.Intents

    def __init__(self, *, intents: discord.Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.tree = app_commands.CommandTree(self)
        self.__my_glossary = infil_glossary.get_full_glossary()

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.user.name}")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    def embed_from_interaction(self, query, author_name, author_avatar):
        term = string_utils.remove_mention_tag(query)
        item = infil_glossary.search_dictionary(self.__my_glossary, term)

        return self.__create_embed(
            title=string_utils.remove_mention_tag(term),
            item=item,
            color=discord.Color.blue(),
            author=author_name,
            avatar=author_avatar
        )

    # TAG EVENT
    async def on_message(self, message):
        user = self.user
        if message.author.bot is False and user.mentioned_in(message) and len(message.content) >= len(user.mention) + 1:
            term = string_utils.remove_mention_tag(message.content)
            item = infil_glossary.search_dictionary(self.__my_glossary, term)

            embed = self.__create_embed(
                title=message.content,
                item=item,
                color=discord.Color.blue(),
                author=message.author.display_name,
                avatar=message.author.avatar.url
            )

            await message.channel.send(embed=embed)

    def __create_embed(self, title, item, color, author, avatar):
        string, self.tags = string_utils.search_and_replace(item["def"])

        embed = discord.Embed(
            title=title,
            description=string,
            color=color
        )
        embed.set_author(name=author, icon_url=avatar)

        if 'games' in item:
            embed.add_field(name="Games", value=item["games"], inline=True)

        if 'altterm' in item:
            embed.add_field(name="Synonyms", value=item["altterm"], inline=True)

        if 'video' in item:
            link = string_utils.create_gfycat_link(item["video"][0])
            embed.add_field(name="Gif", value=string_utils.wrap_link(link), inline=False)

        embed.add_field(name="Source", value=string_utils.create_source(searched_term=title), inline=False)

        return embed

    def __create_action_row_from_tags(self):
        buttons = []
        for tag in self.tags:
            buttons.append(discord.ui.Button(label=tag))

        return buttons
