import discord
from discord.ext import commands
# import config

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.has_role(config.role_dict.get("admin"))
    async def ping(self, ctx):
        await ctx.send(f'pong')

def setup(bot):
    bot.add_cog(Fun(bot))
