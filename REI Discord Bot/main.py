import discord
import os
import requests
import json
import asyncio
import platform
import sys
from discord.ext import commands
from discord.ext.commands import Bot
from keep_alive import keep_alive


if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

client = commands.Bot (command_prefix =config.BOT_PREFIX)
client.remove_command("help")

# Quote API backlog
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# Bot Online / Status / Username
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('<help'))
    print('Logged in as {0.user}'.format(client))

# Inspire quote command
@client.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)

# Load command
@client.command()
async def lamish(ctx, extension):
  client.load_extension(f'cogs.{extension}')

# Unload command
@client.command()
async def unlamish(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

# Reload command
@client.command()
async def relamish(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv('TOKEN'))