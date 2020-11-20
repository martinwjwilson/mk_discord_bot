import discord
from discord.ext import commands
import gspread

gc = gspread.service_account(filename='sheets_credentials.json')
sh = gc.open_by_key('15iLeVfNwbXgy4h8SvZr00y6viT7bH95VLbN32JKFOKI')
worksheet = sh.sheet1

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.has_role(config.role_dict.get("admin"))
    async def ping(self, ctx):
        await ctx.send(f'pong')

    # async def testing(self, number):
    #     return number * 2

    @commands.command()
    async def track(self, ctx, *, track_name: str):
        # Retrieve the track data from the sheet
        # print(await self.testing(track_name))
        res = worksheet.get_all_values()
        # res = worksheet.row_values(4)


        # show the row containing the track name
        # only print the rows after that
        # stop printing when the first cell is blank
        found = False
        i = 1
        for row in res:
            if found and row[0] == '':
                print("stop here")
            if track_name in row:
                found = True
                print(str(i))
            if found:
                print(row)
            i += 1
        # keep printing numbers until the first cell contains 'Best time:'




        # Create a dictionary of scores
        # Create an instance of a track


def setup(bot):
    bot.add_cog(Fun(bot))
