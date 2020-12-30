import discord
from discord.ext import commands
import gspread
from player import Player

gc = gspread.service_account(filename='sheets_credentials.json')
sh = gc.open_by_key('15iLeVfNwbXgy4h8SvZr00y6viT7bH95VLbN32JKFOKI')
worksheet = sh.sheet1

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.has_role(config.role_dict.get("admin"))
    async def ping(self, ctx, num: int):
        # testing = Player("Martin", 1, 10, 100)
        # await ctx.send(testing.name)
        x = lambda a : a + 10
        await ctx.send(x(num))

    async def get_track_rows(self, sheet_data, track_name: str) -> list:
        """
        Returns a list of rows containing records of the requested track
        """
        required = False # are the current rows required
        current_row = 1 # track the number of the current row
        track_times_list = []
        # loop through each row and return the details of the requested track
        for row in sheet_data:
            if required and row[0] == '':
                required = False
                break
            if track_name in row:
                required = True
            if required:
                track_times_list.append(row)
            current_row += 1
        return track_times_list

    async def get_track_times(self, rows: list, track_name: str) -> dict:
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
        stripped_data = rows[1:len(rows)-1]
        for data in stripped_data:
            track_score_dict[data[0]] = data[column_number]
        return track_score_dict

    async def track_time_conversion(self, track_time_dict: dict) -> list:
        """
        Convert a dictionary of players and their times into a list of player objects
        """
        player_list = [] # create a list of players to return
        for player in track_time_dict:
            if(track_time_dict[player] != ''): # check the player has a recorded time for the current track
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

    async def sort_track_times(self, leaderboard_dictionary):
        """
        Sort a dictionary of users and scores from fastest to slowest
        """
        return
        # NEW WAY
        # https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects

        # OLD WAY
        # player_list = [] # create a list of players to return
        # for player in leaderboard_dictionary:
        #     if(leaderboard_dictionary[player] != ''): # check the player has a recorded time for the current track
        #         # get the player time
        #         # format of player times = m:ss:iii
        #         time = leaderboard_dictionary[player].replace(".", ":").split(":")
        #         min = int(time[0])
        #         sec = int(time[1])
        #         ms = int(time[2])
        #         # create a player instance to store in list (keeps order)
        #         player_to_insert = Player(player, min, sec, ms)
        #         # check where to insert new player in player_list
        #         if not player_list: # if player_list is empty then insert name
        #             player_list.append(player_to_insert)
        #         else: # check through the list and insert new player in appropriate place
        #             n = 0
        #             inserted = False
        #             while n < len(player_list) and inserted == False:
        #                 # create an instance of the comparison player
        #                 comparison_player = player_list[n]
        #                 print(f"{player_to_insert.name()}: {player_to_insert.min()} COMPARED TO {comparison_player.name()}: {comparison_player.min()}")
        #                 if player_to_insert.min() >= comparison_player.min():
        #                     player_list.insert(n, player_to_insert)
        #                     inserted = True
        #                 elif player_to_insert.sec() >= comparison_player.sec():
        #                     player_list.insert(n, player_to_insert)
        #                     inserted = True
        #                 elif player_to_insert.ms() >= comparison_player.ms():
        #                     player_list.insert(n, player_to_insert)
        #                     inserted = True
        #                 n += 1
        # for player in player_list:
        #     print(player.name())

    async def get_leaderboard(self, sheet_data, track_name: str) -> list:
        """
        Return a sorted list of player objects in from fastest to slowest
        """
        track_rows = await self.get_track_rows(sheet_data, track_name) # get a list of rows containing the track data
        track_times = await self.get_track_times(track_rows, track_name) # get a dictionary of players and their scores from the requested track
        unsorted_leaderboard_list = await self.track_time_conversion(track_times) # convert the player dictionary into a list of player objects
        sorted_leaderboard_list = await self.sort_leaderboard(unsorted_leaderboard_list) # sort the list of player objects in order of fastest to slowest
        # return the final list

    @commands.command()
    async def track(self, ctx, *, track_name: str):
        """
        Takes in a track name and returns a leaderboard for the chosen track
        """
        sheet_data = worksheet.get_all_values() # Retrieve the track data from the sheet
        leaderboard_dictionary = await self.get_leaderboard(sheet_data, track_name) # Get a list of all players and their times on the requested track
        # Send an embed to the discord channel with the leaderboard

def setup(bot):
    bot.add_cog(Fun(bot))

# --GET THE FASTEST PLAYER FROM A LIST--
# # check if there is a current fastest player
# if not fastest_player: # assign the first player as the fastest
#     fastest_player = Player(player, min, sec, ms)
# else: # check the current player against the fastest
#     if(min < fastest_player.min()): # if the minutes are lower
#         fastest_player = Player(player, min, sec, ms)
#     elif(min == fastest_player.min()): # if the minutes are the same then check the seconds
#         if(sec < fastest_player.sec()): # if the seconds are lower
#             fastest_player = Player(player, min, sec, ms)
#         elif(sec == fastest_player.sec()): # if the seconds are the same then check the milliseconds
#             if(ms < fastest_player.ms()): # if the milliseconds are lower
#                 fastest_player = Player(player, min, sec, ms)
#             elif(ms == fastest_player.ms()):
