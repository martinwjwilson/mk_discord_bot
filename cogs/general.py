import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="This is the brief text description")
    # @commands.has_role(config.role_dict.get("admin"))
    async def ping(self, ctx, num: int):
        # testing = Player("Martin", 1, 10, 100)
        # await ctx.send(testing.name)
        x = lambda a: a + 10
        await ctx.send(x(num))

    @commands.command()
    async def help(self, ctx):
        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # create embed
        help_embed = discord.Embed(title="Help")
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f"Requested by {ctx.message.author.name}"
        )

        for cog in cogs:
            # Get a list of all commands under each cog

            cog_commands = self.bot.get_cog(cog).get_commands()
            commands_list = ''
            for comm in cog_commands:
                commands_list += f'**{comm.name}** - *{comm.description}*\n'

            # Add the cog's details to the embed.

            help_embed.add_field(
                name=cog,
                value=commands_list,
                inline=False
            ).add_field(
                name='\u200b', value='\u200b', inline=False
            )

        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(General(bot))
