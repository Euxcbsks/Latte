from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction, Attachment, Embed
from disnake.ext.commands import message_command, slash_command
from pysaucenao import SauceNao

from core.cog import GeneralCog

if TYPE_CHECKING:
    from typing import BinaryIO

    from pysaucenao import GenericSource

    from core.bot import LuxRay


class Util(GeneralCog):
    def __init__(self, bot: "LuxRay") -> None:
        super().__init__(bot)
        self.sauce = SauceNao(
            api_key=self.bot.config.saucenao_api_key, results_limit=1, min_similarity=0
        )

    # Internal
    async def search_saucenao(self, *, url: str = None, file: "BinaryIO" = None):
        """If both url and file are provided, use url to search and ignore file"""
        if url:
            return await self.sauce.from_url(url)
        elif file:
            return await self.sauce.from_file(file)
        else:
            raise ValueError("Must provide one of url or file")

    async def get_attachment_fp(self, attachment: Attachment | None):
        if attachment:
            file = await attachment.to_file()
            return file.fp
        return None

    def generate_search_result_embed(self, result: "GenericSource"):
        embed = Embed(color=self.bot.config.color)
        embed.add_field("Author", result.author_name, inline=False).add_field(
            "Title", result.title
        ).add_field("Similarity", result.similarity).add_field(
            "Url", result.url, inline=False
        ).set_image(
            result.url
        )

        return embed

    # Slash commands
    @slash_command(name="reverse-image-search")
    async def reverse_image_search(self, inter: ApplicationCommandInteraction):
        pass

    @reverse_image_search.sub_command()
    async def saucenao(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str | None = None,
        image_file: Attachment | None = None,
    ):
        await inter.response.defer(with_message=True, ephemeral=True)

        # Hint user when provide both url and file
        if image_url and image_file:
            await inter.send(
                "Both image url and attachment are provided, use image url to search and ignore attachment."
            )

        # Do search
        results = await self.search_saucenao(
            url=image_url, file=await self.get_attachment_fp(image_file)
        )

        # Generate search result embed and send it
        await inter.send(
            f"Searches remaining today: {results.long_remaining}",
            embed=self.generate_search_result_embed(results[0]),
            ephemeral=True,
        )

    @message_command(name="Reverse image search(SauceNao)")
    async def message_search_saucenao(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(with_message=True, ephemeral=True)

        if attachments := inter.target.attachments:
            results = await self.sauce.from_url(attachments[0].url)
            return await inter.send(
                f"Search using the first image in this message\nSearches remaining today: {results.long_remaining}",
                embed=self.generate_search_result_embed(results[0]),
                ephemeral=True,
            )

        await inter.send("There are no pictures in this message", ephemeral=True)


def setup(bot: "LuxRay"):
    bot.add_cog(Util(bot))
