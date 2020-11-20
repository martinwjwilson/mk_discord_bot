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

    async def get_track_rows(self, sheet_data, track_name):
        """
        Returns a list containing records of the requested track
        """
        required = False # are the current rows required
        current_row = 1 # track the number of the current row
        track_times_list = []
        # loop through each row and return the details of the requested track
        for row in sheet_data:
            if required and row[0] == '':
                required = False
            if track_name in row:
                required = True
            if required:
                track_times_list.append(row)
            current_row += 1
        return track_times_list

    @commands.command()
    async def track(self, ctx, *, track_name: str):
        # Retrieve the track data from the sheet
        sheet_data = worksheet.get_all_values()
        await self.get_track_rows(sheet_data, track_name)
        # Create a dictionary of users and their scores for the specific track
        # Create an instance of a track using a dictionary of users and scores


def setup(bot):
    bot.add_cog(Fun(bot))
