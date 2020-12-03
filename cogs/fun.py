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
        testing = Player("Martin", 1, 10, 100)
        await ctx.send(testing.get_name())

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

    async def get_score_dictionary(self, rows, track_name):
        """
        Return a dictionary containing each player and their best time on the given track
        """
        # Check which column to take the times from based on the track name (either 1, 3, 5 or 7)
        column_number = 0
        for row in rows[0]:
            if row == track_name:
                break
            column_number += 1
        # loop through each row minus the first and last, and create a dictionary of players and scores from the correct column
        track_score_dict = {}
        stripped_data = rows[1:len(rows)-1]
        for data in stripped_data:
            track_score_dict[data[0]] = data[column_number]
        return track_score_dict

    async def sort_track_times(self, leaderboard_dictionary):
        """
        Sort a dictionary of users and scores from fastest to slowest
        """
        sorted_list = []
        # loop through the dictionary, first
        # format is m:ss:iii
        # convert the score to a time and sort by smallest
        fastest_player = None
        print(f"The current fastest player is {fastest_player}")
        for player in leaderboard_dictionary:
            # get the player time
            time = leaderboard_dictionary[player].replace(".", ":").split(":")
            min = int(time[0])
            sec = int(time[1])
            ms = int(time[2])
            # check if there is a current fastest player
            if not fastest_player: # assign the first player as the fastest
                fastest_player = Player(player, min, sec, ms)
            else: # check the current player against the fastest
                print(f"The current fastest player is {fastest_player.get_name()} with {fastest_player.get_minutes()}m {fastest_player.get_seconds()}s {fastest_player.get_milliseconds()}ms and the comparison is{min}m {sec}s {ms}ms")

            print(f"The current fastest player is {fastest_player.get_name()}")

            # print(f"{player} score before conversion is {leaderboard_dictionary[player]} and the score after conversion: min={str(min)}, sec={str(sec)}, ms={str(ms)}")

    @commands.command()
    async def track(self, ctx, *, track_name: str):
        """
        Takes in a track name and returns a leaderboard for the chosen track
        """
        # Retrieve the track data from the sheet
        sheet_data = worksheet.get_all_values()
        track_rows = await self.get_track_rows(sheet_data, track_name)
        leaderboard_dictionary = await self.get_score_dictionary(track_rows, track_name)
        sorted_time_list = await self.sort_track_times(leaderboard_dictionary)
        # Send an embed to the discord channel with the leaderboard

class Player():
    def __init__(self, name, min, sec, ms):
        self.name = name
        self.min = min
        self.sec = sec
        self.ms = ms

    def get_name(self):
        return self.name

    def get_minutes(self):
        return self.min

    def get_seconds(self):
        return self.sec

    def get_milliseconds(self):
        return self.ms

def setup(bot):
    bot.add_cog(Fun(bot))
