import discord
import fetch
from time import sleep


class EmbedResponse:
    def __init__(self, embed, emoji):
        self.embed = embed
        self.emoji = emoji


# Returns an embed for the message and an emoji for the status
def generate_response(args):
    # No args -> help message
    if (len(args) == 1 or len(args) == 2):
        embed = helper("List of commands")
        return EmbedResponse(embed, "❔")
    command = args[1]

    # "user" command
    if (command == "user"):
        if (len(args) > 3):
            embed = error(title="Too many usernames",
                          reason="When using the `user` command, please only request one user at a time.\nTo look at multiple users at the same time, use the `compare` command.")
            return EmbedResponse(embed, "⛔")

        username = args[2]
        res = fetch.weekly_track_chart(username)

        if "error" in res:
            embed = error(title="Error contacting Last.FM API",
                          reason=res["message"])
            return EmbedResponse(embed, "⛔")

        tracklist = res["weeklytrackchart"]["track"]
        embed = user_recap(username, tracklist)
        return EmbedResponse(embed, "✅")

    # todo: "compare" command
    elif (command == "compare"):
        if (len(args) < 4):
            embed = error(title="Invalid comparison",
                          reason="Please add 2 or more usernames to compare.")
            return EmbedResponse(embed, "⛔")
        # todo: get data for each user (unsure what we will be comparing yet xd)

        embed = error(title="Not yet implemented",
                      reason="Sorry, the `compare` command hasn't been fully implemented yet.")
        return EmbedResponse(embed, "😔")

    else:
        embed = helper("List of commands")
        return EmbedResponse(embed, "❔")


### util embeds ###

def helper(title):
    embed = discord.Embed(
        title=title, color=0x000000
    )
    embed.description = "- **user**: recap of a single user's stats for the past week\n- **compare**: compare last week's status for any number of users _(not yet implemented)_"
    return embed


def error(title, reason):
    embed = discord.Embed(
        title=title, description=reason, color=0x000000
    )
    embed.set_footer(
        text="Use `$lastfm` with no arguments to see a help message")
    return embed


### functional embeds ###
lastfm_red = 0xD91F11


def user_recap(username, tracks):
    embed = discord.Embed(
        title=f"{username}'s Music This Week", color=lastfm_red, description="", url=f"https://www.last.fm/user/{username}")

    # gets data about all tracks
    artists_map = {}
    total_tracks = 0
    total_listens = 0
    for track in tracks:
        playcount = int(track["playcount"])
        total_tracks += 1
        total_listens += playcount

        artist = track["artist"]["#text"]
        if artist not in artists_map:
            artists_map[artist] = playcount
        else:
            artists_map[artist] += playcount

    embed.description += "**Top Tracks**\n"
    # formats top 3 tracks
    for track in tracks[:3]:
        title = track["name"]
        artist = track["artist"]["#text"]
        play_count = track["playcount"]

        track_details = f"- **{title}** by **{artist}** — {play_count} plays\n"
        embed.description += track_details

    artists = [{"artist": k, "count": v} for (k, v) in artists_map.items()]
    artists.sort(key=lambda x: x["count"], reverse=True)
    # formats top 3 artists
    embed.description += "------------------------------------------------------\n**Top Artists**\n"
    for artist in artists[:3]:
        name = artist["artist"]
        count = artist["count"]
        artist_details = f"- **{name}** — {count} plays\n"
        embed.description += artist_details

    footer = f"{total_listens} total listens — {total_tracks} unique tracks — {len(artists)} unique artists"
    embed.set_footer(text=footer)

    return embed


# some overlap with the `user_recap` fn but eh
def user_compare(usernames):
    tracklists = []
    for user in usernames:
        res = fetch.weekly_track_chart(user)
        tracklist = res["weeklytrackchart"]["track"]
        tracklists.append(tracklist)
        sleep(0.5)

    title = usernames.join(", ")
    embed = discord.Embed(
        title=f"Last Week for {title}", color=lastfm_red, description="")
    pass
