import json
import discord
from dotenv import load_dotenv
import os
from fetch import weekly_track_chart


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
        # await message.channel.send("Getting your data...")

        # res = weekly_track_chart(username)
        tracks = parse_res()
        embed = create_embed_top_tracks("jake6969696969", tracks)

        await message.channel.send(embed=embed)


# Converts weekly track chart response into discord message
def parse_res():
    with open("example.json", "r") as res:
        data = json.load(res)
        tracklist = data["weeklytrackchart"]["track"][:3]
        return tracklist


# Creates embeds for the discord message
def create_embed_top_tracks(username, tracks):
    embed = discord.Embed(
        title=f"{username}'s Top Tracks Last Week", color=0xD91F11, description="")
    
    for track in tracks:
        title = track["name"]
        artist = track["artist"]["#text"]
        # int for coverart size = 0:small, 1:medium, 2:large
        # but it turns out, lastfm doesn't provide valid coverarts in this response anyway...
        cover_art = track["image"][1]["#text"]
        play_count = track["playcount"]

        track_details = f"\n**{title}** by **{artist}** — {play_count} plays\n"
        embed.description += track_details

    return embed


client.run(discord_token)
