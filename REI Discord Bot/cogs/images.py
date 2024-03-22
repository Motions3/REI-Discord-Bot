import os, sys, discord, random
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Images(commands.Cog):

  def __init__(self, client):
    self.client = client

  # PRAISE THE SUN
  @commands.command()
  async def praise(self, ctx):
      '''Praise the Sun'''
      await ctx.send('https://i.imgur.com/K8ySn3e.gif')

  # How Dare You
  @commands.command()
  async def furious(self, ctx):
      '''How Dare You'''
      await ctx.send('https://media0.giphy.com/media/cpkQpkVFOOoNi/giphy.gif')

  # Cha Cha Cha
  @commands.command()
  async def chacha(self, ctx):
      '''Cha Cha Cha'''
      await ctx.send('https://media.tenor.com/images/33e555b1839136e3dbe3b536ac0f0441/tenor.gif')

def setup(client):
  client.add_cog(Images(client))