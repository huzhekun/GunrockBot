import discord
from discord.ext import menus
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
import operator
import random
import pickle
import datetime
import csv
import sys
import math

# initializes the prefixes dictionary
prefixes = {}

#loads the prefixes file
try:
    pickle_prefix_in = open("pickles/prefixes.pickle", "rb")
except FileNotFoundError:
    # If the code is being run for the first time and therefore a dictionary does not exist
    pickle_prefix_out = open("pickles/prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_prefix_out)
    pickle_prefix_out.close()

prefixes = pickle.load(pickle_prefix_in)

default_prefix = '.'

#a function to save new prefixes to the prefixes file
def prefix_saving():
    pickle_out = open("pickles/prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_out)
    pickle_out.close()

#the function to determine what the prefix is whenever a command is called
async def determine_prefix(bot, message):
    guild = message.guild

    if guild:
        return prefixes.get(guild.id, default_prefix)
    else:
        return default_prefix

initial_extensions = [
    'cogs.reactroles',
    'cogs.swearjar',
    'cogs.quotebook',
    'cogs.memes',
    'cogs.data'
]

client = commands.Bot(command_prefix = determine_prefix, description="Gunrock the Bot!")

if __name__ == '__main__':
    #adds the cogs as extensions
    for extension in initial_extensions:
        client.load_extension(extension)

# when the bot's ready
@client.event
async def on_ready():
    print('ready')

# on error
@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error!", description=str(error), color=0xd11313)
    await ctx.send(embed = embed)

# when a member joins
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name = "👋welcome")
    role = get(member.guild.roles, name = "Aggie")
    await member.add_roles(role)
    await channel.send(f"Fellow Aggie {member.mention} has joined! Go pick a role in #roles and introduce yourself in #introductions! Please join us in the voice chats as well!")
    print(f'Fellow Aggie {member} has joined!')

# when a member leaves
@client.event
async def on_member_remove(member):
    print(f'{member} yeeted away from the server.')

#
# HELP COMMAND
#

client.remove_command('help')
@client.command()
async def help(ctx):
    guild = ctx.guild
    prefix = ""
    if guild:
        prefix = prefixes.get(guild.id, default_prefix)
    else:
        prefix = default_prefix

    instructions = prefix + "add @user [number]: Adds [number] points to the mentioned user's swear jar. \n\n"
    instructions += prefix + "remove @user [nummber]: Removes [number] points from the mentioned user's swear jar. \n\n"
    instructions += prefix + "leaderboard: Shows the top 5 in the swear jar. \n\n"
    instructions += prefix + "addquote @user [quote]: Add a quote to the mentioned user's quotebook. \n\n"
    instructions += prefix + "quote @user: Outputs the random quote from the mentioned user's quotenook. \n\n"
    instructions += prefix + "listquotes @user: Lists all of the mentioned user's quotes. \n\n"
    instructions += prefix + "removequote @user [quote number]: Removes the designated quote from the mentioned user's quote book. \n\n"
    instructions += prefix + "editquote @user [quote number] [new quote]: Overwrites the user's quote at [number] with [new quote]. \n\n"
    instructions += prefix + "getcourse [course code]: Gives you the full course name and description. Make sure to put in zeros! For example, to get data about DRA 001, make sure those two 0's are there. Ex. " + prefix + "getcourse MAT 021A "

    embed = discord.Embed(title="Commands:", description=instructions, color=0xffbf00)

    await ctx.send(embed = embed)

# set prefix command
@client.command()
@has_permissions(manage_guild=True)
async def setprefix(ctx, arg):
    prefixes[ctx.guild.id] = arg
    prefix_saving()
    embed = discord.Embed(title="Prefix changed!", description="Prefix is now " + arg, color=0xffbf00)
    await ctx.send(embed = embed)

# cog reload command
@client.command()
@has_permissions(manage_guild=True)
async def cog_reload(ctx, *, cog: str):
    """Command which Reloads a Module.
    Remember to use dot path. e.g: cogs.owner"""

    try:
        client.unload_extension(cog)
        client.load_extension(cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')

class TimezoneTimes(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        embed = discord.Embed(title="the time", description="1. Pacific Time\n2. Eastern Time\n3. Korean Time\n4. HK Time", color=0xffbf00)
        return await channel.send(embed = embed)

    @menus.button('1️⃣')
    async def on_one(self, payload):
        embed = discord.Embed(title="The Time on the West Coast", description=(datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('2️⃣')
    async def on_two(self, payload):
        embed = discord.Embed(title="The Time on the East Coast", description=(datetime.datetime.utcnow() - datetime.timedelta(hours=4)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('3️⃣')
    async def on_three(self, payload):
        embed = discord.Embed(title="The Time on the Korean Coast", description=(datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('4️⃣')
    async def on_four(self, payload):
        embed = discord.Embed(title="The Time on the HK Coast", description=(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

@client.command()
async def telltime(ctx):
    m = TimezoneTimes()
    await m.start(ctx)

client.run(sys.argv[1])