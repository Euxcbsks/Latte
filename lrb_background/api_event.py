from typing import TYPE_CHECKING

from disnake import Member
from disnake.ext.commands.cog import Cog

from core.cog import GeneralCog

if TYPE_CHECKING:
    from core.bot import LuxRay


class ApiEvent(GeneralCog):
    @Cog.listener()
    async def on_connect(self):
        print("Connected to Discord")

    @Cog.listener()
    async def on_ready(self):
        print("Bot is ready")

    @Cog.listener()
    async def on_member_join(self, member: Member):
        server = await self.get_server(member.guild.id)

        if auto_roles := server.role.auto:
            await member.add_roles(
                member.guild.get_role(role_id) for role_id in auto_roles
            )


def setup(bot: "LuxRay"):
    bot.add_cog(ApiEvent(bot))
