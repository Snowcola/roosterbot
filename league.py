import discord
import arrow
import datetime
import os
import cassiopeia as cass
from cassiopeia import Summoner
from discord.ext import commands
from terminaltables import DoubleTable as SingleTable

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

API_KEY = os.environ.get("RIOT_API_KEY")
cass.set_riot_api_key(API_KEY)
cass.set_default_region("NA")


class League:
    def __init__(self, bot):
        self.bot = bot

    def convertMultikill(self, killnum):
        switcher = {
            0: "No Kills :(",
            1: "single",
            2: "double",
            3: "triple",
            4: "quadra",
            5: "penta"
        }
        return switcher.get(killnum, "")

    @commands.command(pass_context=True, no_pm=True)
    async def game(self, ctx, person):
        """Shows the current game and who is in it"""
        try:
            player = Summoner(name=person, region="NA")
            match = player.current_match()
            gametype = match.queue
            blue_team = match.blue_team().participants
            red_team = match.red_team().participants
            duration = match.duration

            data = []
            data.append(["Red Team", "Blue Team"])

            for x in range(len(red_team)):
                data.append(
                    [red_team[x].summoner.name, blue_team[x].summoner.name])

            table = SingleTable(data)
            response = f""" Current Game:

            **{person} is {duration} into a {gametype.value} game**\n\n```{table.table}```"""

            await self.bot.send_message(ctx.message.channel, response)

        except ValueError as e:
            await self.bot.say(f"Something went wrong there :(")
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
        matchhistory = cass.MatchHistory(
            summoner=summoner,
            begin_time=arrow.Arrow(year, month, day),
            end_time=arrow.now())

        total_games = len(matchhistory)

        for match in matchhistory:
            if match.participants[summoner].team.win:
                wins += 1

        winrate = round(wins / total_games * 100)

        await self.bot.send_message(
            ctx.message.channel,
            f"{person} has a win rate of **{winrate}%** with {wins} wins over {total_games} games this week. "
        )

    @commands.command(pass_context=True, no_pm=True)
    async def matches(self, ctx, person, num_games: int = 10):
        """Gets match history of a summoner

        Usage:
            !matches snowcola 15
        """
        summoner = Summoner(name=person, region="NA")
        match_history = summoner.match_history
        match_history = match_history[:num_games]
        await self.bot.say("Digging through the chronicles of Runeterra...")

        data = []
        data.append(
            ["W/L", "Champion", "K/D/A", "Multikill", "CS", "Gold Earned"])
        for match in match_history:
            result = ""
            champ = match.participants[summoner].champion.name
            stats = match.participants[summoner].stats
            k = stats.kills
            d = stats.deaths
            a = stats.assists
            spree = self.convertMultikill(stats.largest_multi_kill)
            cs = stats.total_minions_killed + stats.neutral_minions_killed
            gold = "{:,}".format(stats.gold_earned)

            if match.participants[summoner].team.win:
                result = "Win "
            else:
                result = "Loss"
            data.append([result, champ, f"{k}/{d}/{a}", spree, cs, gold])

        table = SingleTable(data)

        await self.bot.say(f"ahh here it is! \n\n```{table.table}```")

    @commands.command(pass_context=True, no_pm=True)
    async def rank(self, ctx, person):
        """Gets the current rank of a summoner"""

        summoner = Summoner(name=person, region="NA")
        positions = summoner.league_positions
        rank = f"{positions.fives.tier} {positions.fives.division}"

        await self.bot.say(f"{person} is in **{rank}**")