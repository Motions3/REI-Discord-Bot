import os, sys, discord, random
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Animerec(commands.Cog):

  def __init__(self, client):
    self.client = client

  # Recommends a random anime from AnimeList.csv
  @commands.command(aliases=['randomanime']) 
  async def rani(self, ctx):
      global anirec
      global sugg
      
      anirec = [line.strip() for line in open('AnimeList.csv')]
      sugg = random.choice(anirec)
      await ctx.send(f"**Here You Go** {ctx.author.mention} ^-^\n\"" + sugg + "\"")


  # Recommends a random anime character to cosplay from cosplay.csv
  @commands.command(aliases=['randomcosplay']) 
  async def rcosplay(self, ctx):
      global anirec
      global sugg
      
      anirec = [line.strip() for line in open('cosplay.csv')]
      sugg = random.choice(anirec)
      await ctx.send(f"**Try this character** {ctx.author.mention} **UwU**\n\"" + sugg + "\"")


def setup(client):
  client.add_cog(Animerec(client))