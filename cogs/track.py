import discord
from discord.ext import commands
import gspread
from player import Player

gc = gspread.service_account(filename='sheets_credentials.json')
sh = gc.open_by_key('15iLeVfNwbXgy4h8SvZr00y6viT7bH95VLbN32JKFOKI')
worksheet_names = ["New Tracks", "Retro Tracks", "DLC Tracks"]


class Track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_track_rows(self, sheet_data, track_name: str) -> list:
        """
        Returns a list of rows containing records of the requested track
        Search all 3 sheets
        """
        track_times_list = []
        for sheet in sheet_data:
            required = False  # are the current rows required
            current_row = 1  # track the number of the current row
            # loop through each row and return the details of the requested track
            for row in sheet:
                if required and row[0] == '':
                    required = False
                    break
                if track_name in row:
                    required = True
                if required:
                    track_times_list.append(row)
                current_row += 1
        if track_times_list:
            return track_times_list
        else:
            print("There is no track with this name")

    @staticmethod
    async def get_track_times(rows: list, track_name: str) -> dict:
        """
        Return a dictinoary of players and their best time on the chosen track
        """
        # Check which column to take the times from based on the track name (either 1, 3, 5 or 7)
        column_number = 0
        for row in rows[0]:
            if row == track_name:
                break
            column_number += 1
        # loop through each row minus the first and last, and create a dictionary of player objects times from the correct column
        track_score_dict = {}
        stripped_data = rows[1:len(rows) - 1]
        for data in stripped_data:
            track_score_dict[data[0]] = data[column_number]
        return track_score_dict

    @staticmethod
    async def track_time_conversion(track_time_dict: dict) -> list:
        """
        Convert a dictionary of players and their times into a list of player objects
        """
        player_list = []  # create a list of players to return
        for player in track_time_dict:
            if track_time_dict[player] != '':  # check the player has a recorded time for the current track
                # get the player time
                # format of player times = m:ss:iii
                time = track_time_dict[player].replace(".", ":").split(":")
                min = int(time[0])
                sec = int(time[1])
                ms = int(time[2])
                # create a player instance to store in list (keeps order)
                player_to_insert = Player(player, min, sec, ms)
                player_list.append(player_to_insert)
        return player_list

    @staticmethod
    async def sort_leaderboard(unsorted_leaderboard_list: list) -> list:
        """
        Sort a list of player objects from fastest to slowest
        """
        return sorted(unsorted_leaderboard_list, key=lambda player: (player.min, player.sec, player.ms))

    async def get_leaderboard(self, sheet_data, track_name: str) -> list:
        """
        Return a sorted list of player objects in from fastest to slowest
        """
        track_rows = await self.get_track_rows(sheet_data, track_name)  # get a list of rows containing the track data
        track_times = await self.get_track_times(track_rows,
                                                 track_name)  # get a dictionary of players and their scores from the requested track
        unsorted_leaderboard_list = await self.track_time_conversion(
            track_times)  # convert the player dictionary into a list of player objects
        sorted_leaderboard_list = await self.sort_leaderboard(
            unsorted_leaderboard_list)  # sort the list of player objects in order of fastest to slowest
        return sorted_leaderboard_list  # return the final list

    @commands.command(
        name="track",
        description="Get leaderboard of a track",
        usage="<text>"
    )
    async def track(self, ctx, *, track_name: str):
        """
        Takes in a track name and returns a leaderboard for the chosen track
        """
        await ctx.trigger_typing()
        # Get a list of all the data from each sheet
        list_of_worksheet_data = []
        for sheet in worksheet_names:
            worksheet = sh.worksheet(sheet)
            sheet_data = worksheet.get_all_values()
            list_of_worksheet_data.append(sheet_data)
        leaderboard_list = await self.get_leaderboard(list_of_worksheet_data,
                                                      track_name)  # Get a list of all players and their times on the requested track
        # Send an embed to the discord channel with the leaderboard
        # check how many entries are in the list
        embed = discord.Embed(title=f"Leaderboard - {track_name}", description="The top 3 fastest time are:")
        if len(leaderboard_list) > 0:
            embed.add_field(name="First",
                            value=f"{leaderboard_list[0].name}: {leaderboard_list[0].min}.{leaderboard_list[0].sec}.{leaderboard_list[0].ms}",
                            inline=False)
            if len(leaderboard_list) > 1:
                embed.add_field(name="Second",
                                value=f"{leaderboard_list[1].name}: {leaderboard_list[1].min}.{leaderboard_list[1].sec}.{leaderboard_list[1].ms}",
                                inline=False)
                if len(leaderboard_list) > 2:
                    embed.add_field(name="Third",
                                    value=f"{leaderboard_list[2].name}: {leaderboard_list[2].min}.{leaderboard_list[2].sec}.{leaderboard_list[2].ms}",
                                    inline=False)
        else:
            await ctx.send("There are no entries for this track")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Track(bot))
