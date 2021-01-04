import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "This is the longer description of the help for this command", brief = "This is the brief text description")
    # @commands.has_role(config.role_dict.get("admin"))
    async def ping(self, ctx, num: int):
        # testing = Player("Martin", 1, 10, 100)
        # await ctx.send(testing.name)
        x = lambda a : a + 10
        await ctx.send(x(num))

def setup(bot):
    bot.add_cog(General(bot))
