import os, sys, discord, random
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Test(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def test(self,ctx):
    await ctx.send('test')

def setup(client):
  client.add_cog(Test(client))