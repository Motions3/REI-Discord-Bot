import os, sys, discord
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Help(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx):
      embed = discord.Embed(
        color = discord.Color.purple()
      )

      embed.set_author(name="I'm here to help you senpai!! >.<")
      embed.add_field(name='Fun', value='f, flip, urban, reverse, password, rate, beer, hot, nms, slots, penis, rps, 8ball, dice, number, trump, badjoke, groot, countdown', inline=False )
      embed.add_field(name='Information', value='ping, invite, poll, user, math, botinfo', inline=False )
      embed.add_field(name='Images', value='praise, cat, comic, furious, chacha', inline=False )
      embed.add_field(name='Anime', value='rani, rcosplay', inline=False )

      await ctx.author.send(embed=embed)

def setup(client):
  client.add_cog(Help(client))