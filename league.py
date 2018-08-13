import discord
import arrow
import datetime
import os
import math
import cassiopeia as cass
from cassiopeia import Summoner, GameMode, GameType
from discord.ext import commands

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

API_KEY = os.environ.get("RIOT_API_KEY")
cass.set_riot_api_key(API_KEY)
cass.set_default_region("NA")


class League:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def game(self, ctx,  person):
        """Shows the current game and who is in it"""
        try:
            # summoner = cass.get_summoner(name=person)
            player = Summoner(name=person, region="NA")
            match = player.current_match()
            gametype = match.queue
            blue_team = match.blue_team().participants
            red_team = match.red_team().participants
            duration = match.duration

            response = f""" Current Game:

            **{person} is {duration} into a {gametype.value} game**

            **Red Team:**
            {red_team[0].summoner.name}
            {red_team[1].summoner.name}
            {red_team[2].summoner.name}
            {red_team[3].summoner.name}
            {red_team[4].summoner.name}

            **Blue Team:**
            {blue_team[0].summoner.name}
            {blue_team[1].summoner.name}
            {blue_team[2].summoner.name}
            {blue_team[3].summoner.name}
            {blue_team[4].summoner.name}"""

            await self.bot.send_message(ctx.message.channel, response)

        except ValueError as e:
           #await self.bot.say(f"AHHHHH.")
           print(e)

    @commands.command(pass_context=True, no_pm=True)
    async def winrate(self, ctx, person):
        """Gets winrate for a player over the past week"""
        summoner = Summoner(name=person, region="NA")
        await self.bot.say("It will take me a moment to do the math...")

        wins = 0
        
        last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
        year = last_week.year
        month = last_week.month
        day = last_week.day
        matchhistory = cass.MatchHistory(summoner=summoner, 
                                            begin_time=arrow.Arrow(year, month, day), 
                                            end_time=arrow.now())

        total_games = len(matchhistory)

        for match in matchhistory:
            if match.participants[summoner].team.win:
                wins += 1
        
        winrate = round(wins/total_games*100)

        await self.bot.send_message(ctx.message.channel, f"{person} has a win rate of **{winrate}%** with {wins} wins over {total_games} games this week. ")


