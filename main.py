# Atomizer, nukebot recreation in Python
# -----------------------------------------
# This code is very old, and honestly not very great. Made mostly to learn slash commands & buttons in discord.py
# Feel free to use this in whatever you'd like, or to help you learn as I did
# Again, don't expect too much from this as it was made in around an hour
# ------------------------------------------------------------------------------
# The main purpose of this was to be a recreation of nukebot, because as when initially making this bot,
# the actual nukebot was down for a while, so while bored one day I decided to recreate it for a friend's server
# credits to the original nukebot creators for the original bot and the "inspiration" (if you can call it that)
# --------------------------------------------------------------------------------------------------------------------
# How to use:
# 1. Open config.json, and change token to your bot's token.
# 2. In config.json, change botowner to your discord id.
# 3. [Optional] Go to https://apyhub.com, and make an account.
# Then, find your API key, and put it in apytoken in config.json.
# 4. In config.json, change supportserver to the invite to your support server, or leave blank for none.
# 5. If you don't already have python, get it at https://python.org
# 6. Run "pip install -r requirements.txt"
# 7. Run this file
# ---------------------------------------------------------------------------

import discord
from discord import app_commands, AutoShardedClient
from discord.ext import tasks
import json
import os
import random
import time
import asyncio
import datetime
import requests

intents = discord.Intents.all()
client = discord.AutoShardedClient(intents=intents)
tree = app_commands.CommandTree(client)

with open('config.json') as token:
    data = json.load(token)

# hex color variables for ease of use
yellow = 0xFFFF00
green = 0x00FF00
red = 0xFF0000

# for uptime
start_time = time.time()

class claimNitro(discord.ui.View):
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("https://www.tenor.com/view/rick-rolled-no-nitro-for-you-22954713",ephemeral=True)

        
@tasks.loop(seconds=60.0)
async def serverStatus():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help | {str(len(client.guilds))} servers"))


@client.event
async def on_ready():
    await tree.sync()
    serverStatus.start()
    os.system("cls")
    os.system("title Atomizer")
    print("Ready!\n")


# command formerly named nuke
@tree.command(name = "clear", description = "Delete all messages in a channel")
async def clear(interaction):
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    channel = interaction.channel
    try:
        newchannel = await channel.clone(reason=f"Channel has been cleared by {interaction.user}")
        await newchannel.edit(position=channel.position)
        await channel.delete()
    except Exception as err:
        await interaction.response.send_message(f"Unable to clear channel. Debug information: {err}", ephemeral = True)
        return
    await newchannel.send(":warning:Cleared this channel:warning:")
    await newchannel.send("https://media.discordapp.net/attachments/1074082244286750780/1074082360578031677/nuke.gif")


@tree.command(name = "nitrogen", description = "Generates some nitro")
async def nitrogen(interaction):
    embed=discord.Embed(title="You've been gifted a subscription!", description=f"**{interaction.user}** gifted you nitro for **1 month!**")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082360263442512/Nitro.png")
    await interaction.response.send_message(embed=embed,view=claimNitro(timeout=None))


@tree.command(name = "ping", description = "Shows the bot's latency")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! The bot's latency is {round(client.latency * 1000)}ms")


@tree.command(name = "flipacoin", description = "A simple coin flip")
async def flipacoin(interaction):
        choice = random.randint(1,2)
        if choice == 1:
            embed=discord.Embed(title="Head")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082359747559474/euro-head.png")
        if choice == 2:
            embed = discord.Embed(title="Tails")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082360024375296/euro-tail.png")
        await interaction.response.send_message(embed=embed)
        

@tree.command(name = "purge", description = "Allows to delete a specific amount of messages.")
async def purge(interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    if amount > 100:
        amount = 100
    await interaction.response.defer(ephemeral=True)
    purgedMessages = await interaction.channel.purge(limit = amount)
    await interaction.followup.send(f"Purged ``{len(purgedMessages)}`` messages.",ephemeral=True)


@tree.command(name = "ban", description = "Ban a specified user")
async def ban(interaction, user: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    if reason == None:
        await user.ban()
        await interaction.response.send_message(f"Banned <@{user.id}>")
    else:
        await user.ban(reason = reason)
        await interaction.response.send_message(f"Banned <@{user.id}> for ``{reason}``")


@tree.command(name = "kick", description = "Kick a specified user")
async def kick(interaction, user: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    if reason == None:
        await user.kick()
        await interaction.response.send_message(f"Kicked <@{user.id}>")
    else:
        await user.kick(reason = reason)
        await interaction.response.send_message(f"Kicked <@{user.id}> for ``{reason}``")


@tree.command(name = "dice", description = "Rolls a virtual dice")
async def dice(interaction):
        choice = random.randint(1,6)
        if choice == 1:
            embed=discord.Embed(title="It's a 1")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082308962918441/dice1.png")
        if choice == 2:
            embed=discord.Embed(title="It's a 2")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082309290086411/dice2.png")
        if choice == 3:
            embed=discord.Embed(title="It's a 3")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082309562703943/dice3.png")
        if choice == 4:
            embed=discord.Embed(title="It's a 4")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082309864706198/dice4.png")
        if choice == 5:
            embed=discord.Embed(title="It's a 5")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082310175064155/dice5.png")
        if choice == 6:
            embed=discord.Embed(title="It's a 6")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074082244286750780/1074082310456090674/dice6.png")
        await interaction.response.send_message(embed=embed)


# I now realize how stupid I was to not use cogs
@tree.command(name = "help", description = "Returns the help menu")
async def help(interaction):
    embed=discord.Embed(title="Slash commands",)
    embed.set_thumbnail(url=client.user.avatar.url)
    embed.add_field(name="Moderation", value="``ban``, ``kick``, ``clear``, ``purge``", inline=False)
    embed.add_field(name="Fun", value="``dice``, ``dontasktoask``, ``flipacoin``, ``howgay``, ``nitrogen``, ``nohello``, ``screenshot``, ``tryitandsee``", inline=False)
    embed.add_field(name="Tools", value="``Coming soon!``", inline=False) # Ironic
    embed.add_field(name="Misc", value="``about``, ``help``, ``ping``, ``support``", inline=False)
    embed.set_footer(text="More commands coming soon!")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name = "nohello", description = "Advises to not just say hello")
async def nohello(interaction, user: discord.Member = None):
    if user == None:
        await interaction.response.send_message(f"https://nohello.net/")
    else:
        await interaction.response.send_message(f"<@{user.id}> https://nohello.net/")


@tree.command(name = "support", description = "Gives you the support server invite")
async def support(interaction):
    support_server = data["supportserver"]
    if data["supportserver"] == "": support_server = "There is currently not a support server."
    await interaction.response.send_message(support_server,ephemeral=True)


@tree.command(name = "tryitandsee", description = "Advises to try and see")
async def tryitandsee(interaction, user: discord.Member = None):
    if user == None:
        await interaction.response.send_message(f"https://tryitands.ee/")
    else:
        await interaction.response.send_message(f"<@{user.id}> https://tryitands.ee/")


@tree.command(name = "dontasktoask", description = "Advises to not ask to ask but to ask instead")
async def dontasktoask(interaction, user: discord.Member = None):
    if user == None:
        await interaction.response.send_message(f"https://dontasktoask.com/")
    else:
        await interaction.response.send_message(f"<@{user.id}> https://dontasktoask.com/")


@tree.command(name="warn", description="Warn a specified user")
async def warn(interaction, user: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    
    database = "./database/warns/"
    guild_id = interaction.guild.id
    filename = f"{database}{guild_id}.json"
    
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            json.dump({}, f)
    
    with open(filename, "r") as f:
        warns = json.load(f)
    
    if str(user.id) not in warns:
        warns[str(user.id)] = []
        
    warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warns[str(user.id)].append((reason, warn_time))
    
    with open(filename, "w") as f:
        json.dump(warns, f)
    
    if reason is None:
        embed = discord.Embed(description=f"You got warned in ``{interaction.guild}``", color=yellow)
        await user.send(embed=embed)
        await interaction.response.send_message(f"Warned <@{user.id}>")
    else:
        embed = discord.Embed(description=f"You got warned in ``{interaction.guild}`` for ``{reason}``", color=yellow)
        await user.send(embed=embed)
        await interaction.response.send_message(f"Warned <@{user.id}> for ``{reason}``")


@tree.command(name="warns", description="Check the warns a specified user has.")
async def warns(interaction, user: discord.Member):
    guild_id = interaction.guild.id
    database = "./database/warns/"
    filename = f"{database}{guild_id}.json"
    
    if not os.path.isfile(filename):
        return await interaction.response.send_message("No warns have been issued in this server yet.")
    
    with open(filename, "r") as f:
        warns = json.load(f)
    
    if str(user.id) not in warns:
        await interaction.response.send_message(f"<@{user.id}> has no warns in this server.")
    else:
        total_warns = len(warns[str(user.id)])
        warn_list = ""
        for reason, warn_time in warns[str(user.id)]:
            formatted_time = datetime.datetime.strptime(warn_time, "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y at %I:%M:%S %p")
            warn_list += f"**{reason}** - {formatted_time}\n"
        embed = discord.Embed(title=f"Warns for {user.name}", description=f"**Total Warns: {total_warns}**\n------------------------\n{warn_list}", color=yellow)
        await interaction.response.send_message(embed=embed)


@tree.command(name = "howgay", description = "Shows how gay you are")
async def howgay(interaction):
        gayPercent = random.randint(0,100)
        if gayPercent == 0:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You aren't gay")
        if gayPercent == 1:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You're maybe gay")
        if 2 <= gayPercent <= 10:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You are slightly gay")
        if 11 <= gayPercent <= 25:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You're somewhat gay")
        if 26 <= gayPercent <= 30:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You're kinda gay")
        if 36 <= gayPercent <= 49:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You're pretty gay")
        if 50 <= gayPercent <= 60:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You're quite gay")
        if 61 <= gayPercent <= 68:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="You feel gay")
        if gayPercent == 69:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="**Nice**")
        if 70 <= gayPercent <= 89:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="Call a doctor or a priest")
        if 90 <= gayPercent <= 99:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="Get the holy water")
        if gayPercent == 100:
            embed=discord.Embed(title=f"You are {str(gayPercent)}% gay",description="**You are gay.**")
        embed.set_thumbnail(url="https://static.dezeen.com/uploads/2018/06/lgbt-pride-flag-redesign-sq.jpg?width=402&height=402")
        await interaction.response.send_message(embed=embed)


@tree.command(name = "about", description = "Displays information about the bot")
async def about(interaction):
    current_time = time.time()
    embed=discord.Embed(title="About",description=f"""
        **Owner**: {await client.fetch_user(data["botowner"])}
        **Servers**: {str(len(client.guilds))}
        **Users**: {str(len(client.users))}
        **Shards**: {client.shard_count}
        **Created**: {client.user.created_at.strftime("%a %#d %B %Y, %I:%M %p")}
        **Language**: Python
        **API**: [discord.py v{discord.__version__}](https://github.com/Rapptz/discord.py)
        **Uptime**: {str(datetime.timedelta(seconds=int(round(current_time - start_time))))}
    """)
    embed.set_thumbnail(url=client.user.avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# a friend asked for this and i thought it'd be pretty interesting, heres the result of that
@tree.command(name = "screenshot", description = "Screenshot any website")
async def screenshot(interaction, website: str):
    current_time = time.time()
    #embed=discord.Embed(title="Screenshotted",description=website)
    await interaction.response.defer()
    
    # added to work with config.json
    if data["apytoken"] == "": await interaction.followup.send("No API key provided!", ephemeral = True); return
    
    headers = {'apy-token': data["apytoken"]}
    url = f'https://api.apyhub.com/generate/screenshot/webpage/image-file?url={website}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("screenshot.png", "wb") as f:
            f.write(response.content)
        file = discord.File("screenshot.png", filename="screenshot.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://screenshot.png")
        await interaction.followup.send(file=file,embed=embed)
    else:
        print("Request failed with status code:", response.status_code)
        failembed=discord.Embed(title="Error - Please Try Again", description=f"Request failed with status code: {response.status_code}", color=red)
        await interaction.followup.send(embed=failembed)


@tree.command(name = "say", description = "Sends a message as the bot")
async def say(interaction, message: str):
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("https://media.discordapp.net/attachments/1060663399379374080/1063484587646406697/togif.gif?width=428&height=428")
    await interaction.response.send_message(message)

token = data['token']
client.run(token)