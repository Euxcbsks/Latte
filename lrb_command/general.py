from datetime import date
from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import slash_command

from core.cog import GeneralCog

if TYPE_CHECKING:
    from pymongo.collection import Collection

    from core.bot import LuxRay


class General(GeneralCog):
    @slash_command(name="簽到")
    async def login(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        server_data: "Collection" = self.db.login.get_collection(str(inter.guild_id))
        user_data = await server_data.find_one(inter.author.id)
        today = date.today()

        if user_data and user_data["last_login"] != today.isoformat():
            user_data["login_days"] += 1
            await server_data.update_one(
                {"_id": inter.author.id},
                {
                    "$set": {
                        "last_login": today.isoformat(),
                        "login_days": user_data["login_days"],
                    }
                },
            )
        elif user_data:
            return await inter.send(f"你今天已經簽到過了 總簽到日數: {user_data['login_days']}")
        else:
            user_data = {
                "_id": inter.author.id,
                "last_login": today.isoformat(),
                "login_days": 1,
            }
            await server_data.insert_one(user_data)

        await inter.send(f"簽到成功! 總簽到日數: {user_data['login_days']}", ephemeral=True)


def setup(bot: "LuxRay"):
    bot.add_cog(General(bot))
