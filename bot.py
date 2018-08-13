import discord
import random
import os
from discord.ext import commands

from music import Music
from league import League, API_KEY
import pycurl
import certifi

TOKEN = os.environ.get("DISCORD_TOKEN")

curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, certifi.where())

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description='Da Music bot that hates Greg for some reason!')
bot.add_cog(Music(bot))
bot.add_cog(League(bot))


@bot.event
async def on_ready():
    print(
        f'Logged in as:\n{bot.user} (ID: {bot.user.id}, API_KEY {bool(API_KEY)}'
    )


@bot.event
async def on_member_join(member):
    print(f'{member} has joined')
    name = member.name
    greg = "inbetweenis#8163"
    if name == greg:
        await bot.say(f"{member} you suck!")
    else:
        await bot.say(f"Welcomw {member}! How can I help you?")


@bot.command(pass_context=True)
async def hello(self, ctx):
    await bot.say(f'Hello {ctx.message.author}')


@bot.command(pass_context=True)
async def roll(ctx, max_roll):
    roll = random.randrange(0, int(max_roll))
    await bot.say(f'{ctx.message.author} rolls a {roll}')


bot.run(TOKEN)
