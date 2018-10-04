import discord
import random
import os
from discord.ext import commands

from music import Music
from league import League, API_KEY
import pycurl
import certifi
import asyncio

TOKEN = os.environ.get("DISCORD_TOKEN")

curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, certifi.where())

if not discord.opus.is_loaded():

    discord.opus.load_opus('opus')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description='Da Music bot that hates Greg for some reason!')
bot.add_cog(Music(bot))
bot.add_cog(League(bot))


@bot.event
async def on_member_join(member):
    print(f'{member} has joined')
    name = member.name
    greg = "inbetweenis#8163"
    channel = member.server.default_channel
    if name == greg:
        await bot.say(f"{member.mention} you suck!")
    else:
        await bot.send_message(
            channel, f"Welcome {member.mention}! How can I help you?")


@bot.event
async def on_voice_state_update(before, after):
    matt = "bobbelly8463".casefold()
    greg = "inbetweenis8163".casefold()
    unique_user = str(after.name + after.discriminator).casefold()

    if before.voice.voice_channel is None and after.voice.voice_channel is not None:
        for channel in before.server.channels:
            if channel.name == 'fieldsofjustice':
                msg = await bot.send_message(
                    channel,
                    f"Howdy {before.mention} :wave:",
                )

                if unique_user == matt:
                    author = after
                    url = "https://www.youtube.com/watch?v=qLdUG3id2rs"
                    voice_channel = author.voice.voice_channel
                    vc = await bot.join_voice_channel(voice_channel)
                    player = await vc.create_ytdl_player(url)
                    player.start()
                    await asyncio.sleep(20)
                    player.stop()

                if unique_user == greg:
                    await bot.send_message(
                        channel,
                        f"Ewww it's {before.mention} :poop:",
                    )

                await asyncio.sleep(10)
                await bot.delete_message(msg)


@bot.event
async def on_ready():
    print(
        f'Logged in as:\n{bot.user} (ID: {bot.user.id}, API_KEY {bool(API_KEY)})'
    )


@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say(f'Hello {ctx.message.author}')


@bot.command(pass_context=True)
async def roll(ctx, max_roll):
    roll = random.randrange(0, int(max_roll))
    await bot.say(f'{ctx.message.author.mention} rolls a {roll}')


bot.run(TOKEN)
