import time
import discord
import psutil
import os
import sys

from datetime import datetime
from discord.ext import commands
from utils import default

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Information(commands.Cog):

    def __init__(self, client):
      self.client = client



    # Ping
    @commands.command()
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        embed = discord.Embed(
            color=0x42F56C
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"Pong request by {context.message.author}"
        )
        await context.send(embed=embed)

    # Invite Bot
    @commands.command(aliases=['joinme', 'join', 'botinvite'])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.client.user.id)}>")

    @commands.command()
    async def server(self, context):
        """
        Get the invite link of the discord server of the bot for some support.
        """
        await context.send("I sent you a private message!")
        await context.author.send("Join my creator's discord server by clicking here: https://discord.gg/4eH7mxajum")

    # Poll
    @commands.command()
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    # User Info
    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        '''Get user info for yourself or someone in the guild'''
        user = user or ctx.message.author
        guild = ctx.message.guild
        guild_owner = guild.owner
        avi = user.avatar_url
        roles = sorted(user.roles, key=lambda r: r.position)

        for role in roles:
            if str(role.color) != '#000000':
                color = role.color
        if 'color' not in locals():
            color = 0

        rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
        time = ctx.message.created_at
        desc = f'{user.name} is currently in {user.status} mode.'
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(color=color, description=desc, timestamp=time)
        em.add_field(name='Name', value=user.name),
        em.add_field(name='Member Number', value=member_number),
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %B %d, %Y')),
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %B %d, %Y')),
        em.add_field(name='Roles', value=rolenames)
        em.set_thumbnail(url=avi or None)
        await ctx.send(embed=em)


    # Math
    @commands.group(invoke_without_command=True)
    async def math(self, ctx):
        '''A command group for math commands'''
        await ctx.send('Available commands:\n`add <a> <b>`\n`subtract <a> <b>`\n`multiply <a> <b>`\n`divide <a> <b>`\n`remainder <a> <b>`\n`power <a> <b>`\n`factorial <a>`')

    @math.command(aliases=['*', 'x'])
    async def multiply(self, ctx, a: int, b: int):
        '''Multiply two numbers'''
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}*{b}`\n✅ Solution: `{a * b}`'
        await ctx.send(embed=em)

    @math.command(aliases=['/', '÷'])
    async def divide(self, ctx, a: int, b: int):
        '''Divide a number by a number'''
        try:
            em = discord.Embed(color=discord.Color.green())
            em.title = "Result"
            em.description = f'❓ Problem: `{a}/{b}`\n✅ Solution: `{a / b}`'
            await ctx.send(embed=em)
        except ZeroDivisionError:
            em = discord.Embed(color=discord.Color.green())
            em.title = "Error"
            em.description = "You can't divide by zero"
            await ctx.send(embed=em)

    @math.command(aliases=['+'])
    async def add(self, ctx, a: int, b: int):
        '''Add a number to a number'''
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}+{b}`\n✅ Solution: `{a + b}`'
        await ctx.send(embed=em)

    @math.command(aliases=['-'])
    async def subtract(self, ctx, a: int, b: int):
        '''Substract two numbers'''
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}-{b}`\n✅ Solution: `{a - b}`'
        await ctx.send(embed=em)

    @math.command(aliases=['%'])
    async def remainder(self, ctx, a: int, b: int):
        '''Gets a remainder'''
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}%{b}`\n✅ Solution: `{a % b}`'
        await ctx.send(embed=em)

    @math.command(aliases=['^', '**'])
    async def power(self, ctx, a: int, b: int):
        '''Raise A to the power of B'''
        if a > 100 or b > 100:
            return await ctx.send("Numbers are too large.")
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}^{b}`\n✅ Solution: `{a ** b}`'
        await ctx.send(embed=em)

    @math.command(aliases=['!'])
    async def factorial(self, ctx, a: int):
        '''Factorial something'''
        if a > 813:
            await ctx.send("That number is too high to fit within the message limit for discord.")
        else:
            em = discord.Embed(color=discord.Color.green())
            em.title = "Result"
            result = 1
            problem = a
            while a > 0:
                result = result * a
                a = a - 1
            em.description = f'❓ Problem: `{problem}!`\n✅ Solution: `{result}`'
            await ctx.send(embed=em)

    @commands.command()
    async def botinfo(self, ctx):
        '''Shows info about bot'''
        em = discord.Embed(color=discord.Color.green())
        em.title = 'NAISU Bot'
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        try:
            em.description = self.client.psa + '\n[Support Server](https://discord.gg/ZrPMHv7ww6)'
        except AttributeError:
            em.description = 'A multi-purpose fun bot designed by NAISU as a commemoration for 1k subscribers.\n[Official Server](https://discord.gg/ZrPMHv7ww6)'
        em.add_field(name="Servers", value=len(self.client.guilds))
        em.add_field(name="Online Users", value=str(len({m.id for m in self.client.get_all_members() if m.status is not discord.Status.offline})))
        em.add_field(name='Total Users', value=len(self.client.users))
        em.add_field(name='Channels', value=f"{sum(1 for g in self.client.guilds for _ in g.channels)}")
        em.add_field(name="Library", value=f"discord.py")
        em.add_field(name="Bot Latency", value=f"{self.client.ws.latency * 1000:.0f} ms")
        em.add_field(name="Invite", value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=268905542)")
        em.add_field(name='YouTube', value='[Click here](https://www.youtube.com/channel/UCxr8ljz13U8hGbcpjFbv_Og)')
        em.add_field(name='YouTube2', value='[Click here](https://www.youtube.com/channel/UCxr8ljz13U8hGbcpjFbv_Og)')
        em.set_footer(text="NAISU Bot | Powered by discord.py")
        await ctx.send(embed=em)




def setup(client):
  client.add_cog(Information(client))