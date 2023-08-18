import os
from dotenv import load_dotenv
import discord
from fetch import weekly_track_chart
from embeds import error_embed, top_tracks_embed


load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$lastfm"):
        args = message.content.split()
        if (len(args) == 1):
            embed = error_embed(
                title="Invalid args", reason="Please provide a username to get a user's top tracks for this week.\nEx: `$lastfm jake6969696969`")
            await message.channel.send(embed=embed)
        elif (len(args) > 2):
            embed = error_embed(
                title="Invalid args", reason="Too many arguments provided.\nPlease provide a single username to get a users top tracks for this week.\nEx: `$lastfm jake6969696969`")
            await message.channel.send(embed=embed)
        else:
            username = args[1]
            res = weekly_track_chart(username)
            embed = discord.Embed()
            if "error" in res:
                embed = error_embed(
                    title="Error contacting Last.FM API", reason=res["message"])
            else:
                tracklist = res["weeklytrackchart"]["track"]
                embed = top_tracks_embed(username, tracklist)
            await message.channel.send(embed=embed)


client.run(discord_token)
