import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
import os
import sys

from io import BytesIO
from discord.ext import commands
from utils import http, default, argparser

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # F for respect
    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(
            f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}"
        )

    # Countdown
    @commands.command()
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('**:ok:** DING DING DING')

    # I AM GROOT
    @commands.command()
    async def groot(self, ctx):
        """Who... who are you?"""
        groots = [
            "I am Groot",
            "**I AM GROOT**",
            "I... am... *Groot*",
            "I am Grooooot",
        ]
        punct = [
            "!",
            ".",
            "?"
        ]

        # Build our groots
        groot_max = 5
        groot = " ".join([random.choice(groots) + (random.choice(punct)*random.randint(0, 5)) for x in range(random.randint(1, groot_max))])
        await ctx.send(groot)

    # Coin flip
    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(
            f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!"
        )

    # Urban Dictionary
    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Urban Dictionary """
        async with ctx.channel.typing():
            try:
                url = await http.get(
                    f'https://api.urbandictionary.com/v0/define?term={search}',
                    res_method="json")
            except Exception:
                return await ctx.send(
                    "Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url['list']):
                return await ctx.send(
                    "Couldn't find your search in the dictionary...")

            result = sorted(url['list'],
                            reverse=True,
                            key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(
                f"📚 Definitions for **{result['word']}**```fix\n{definition}```"
            )

    # Reverse text
    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")


    # Generate Password
    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(
                f"Sending you a private message with your random generated password **{ctx.author.name}**"
            )
        await ctx.author.send(
            f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    # Rate anything
    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(
            f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    # Share a beer
    @commands.command()
    async def beer(self,
                   ctx,
                   user: discord.Member = None,
                   *,
                   reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(
                f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/"
            )

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(
                    m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add',
                                    timeout=30.0,
                                    check=reaction_check)
            await msg.edit(
                content=
                f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻"
            )
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(
                f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;"
            )
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    # How hot is someone
    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    # Notice me senpai!!!!
    @commands.command(aliases=['noticemesenpai', 'nms'])
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """

        bio = BytesIO(await http.get("https://i.alexflipnote.dev/500ce4.gif",
                                     res_method="read"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

    # Slot machine
    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} Two in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    # Penis size
    @commands.command(aliases=['dick'])
    async def penis(self, ctx, member: discord.Member = None):
        """
        Get the penis's length of a user or yourself.
        """
        if not member:
            member = ctx.author
        length = random.randrange(15)
        embed = discord.Embed(description=f"8{'='*length}D", color=0xD75BF4)
        embed.set_author(name=f"{member.display_name}'s penis",
                         icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    # Rock Paper Scissors
    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {0: "rock", 1: "paper", 2: "scissors"}
        reactions = {"🪨": 0, "🧻": 1, "✂": 2}
        embed = discord.Embed(title="Please choose", color=0xF59E42)
        embed.set_author(name=context.author.display_name,
                         icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(
                reaction) in reactions

        try:
            reaction, user = await self.client.wait_for("reaction_add",
                                                        timeout=10,
                                                        check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            client_choice_emote = random.choice(list(reactions.keys()))
            client_choice_index = reactions[client_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name,
                                    icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == client_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {client_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and client_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {client_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and client_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {client_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and client_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {client_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {client_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name,
                                     icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)

    # 8ball
    @commands.command(aliases=['8ball', 'eightball'])
    async def eight_ball(self, context, *args):
        """
        Ask any question to the bot.
        """
        answers = [
            'It is certain.', 'It is decidedly so.', 'You may rely on it.',
            'Without a doubt.', 'Yes - definitely.', 'As I see, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again later.', 'Don\'t count on it.',
            'My reply is no.', 'My sources say no.', 'Outlook not so good.',
            'Very doubtful.'
        ]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C)
        embed.set_footer(text=f"Question asked by: {context.message.author}")
        await context.send(embed=embed)

    # Dice
    @commands.command(aliases=["roll", "100"])
    async def dice(self, ctx, number=1):
        '''Rolls a certain number of dice'''
        if number > 20:
            number = 20

        fmt = ''
        for i in range(1, number + 1):
            fmt += f'`Dice {i}: {random.randint(1, 100)}`\n'
            color = discord.Color.green()
        em = discord.Embed(color=color, title='Roll a 100 sided die', description=fmt)
        await ctx.send(embed=em)

    # Random Comic
    @commands.command(aliases=['xkcd', 'comic'])
    async def randomcomic(self, ctx):
        '''Get a comic from xkcd.'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/info.0.json') as resp:
                data = await resp.json()
                currentcomic = data['num']
        rand = random.randint(0, currentcomic)  # max = current comic
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/{rand}/info.0.json') as resp:
                data = await resp.json()
        em = discord.Embed(color=discord.Color.green())
        em.title = f"XKCD Number {data['num']}- \"{data['title']}\""
        em.set_footer(text=f"Published on {data['month']}/{data['day']}/{data['year']}")
        em.set_image(url=data['img'])
        await ctx.send(embed=em)

    # Random number fact
    @commands.command(aliases=['number'])
    async def numberfact(self, ctx, number: int):
        '''Get a fact about a number.'''
        if not number:
            await ctx.send(f'Usage: `{ctx.prefix}numberfact <number>`')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://numbersapi.com/{number}?json') as resp:
                    file = await resp.json()
                    fact = file['text']
                    await ctx.send(f"**Senpai, did you know?**\n*{fact}*")
        except KeyError:
            await ctx.send("No facts are available for that number.")

    # Ask Trump
    @commands.command(aliases=['trump', 'trumpquote'])
    async def asktrump(self, ctx, *, question):
        '''Ask Donald Trump a question!'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}') as resp:
                file = await resp.json()
        quote = file['message']
        em = discord.Embed(color=discord.Color.green())
        em.title = "What does Trump say?"
        em.description = quote
        em.set_footer(text="Made possible by whatdoestrumpthink.com", icon_url="http://www.stickpng.com/assets/images/5841c17aa6515b1e0ad75aa1.png")
        await ctx.send(embed=em)

    # Bad Joke
    @commands.command(aliases=['joke'])
    async def badjoke(self, ctx):
        '''Get a bad joke.'''
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/random_joke') as resp:
                data = await resp.json()
        em = discord.Embed(color=discord.Color.green())
        em.title = data['setup']
        em.description = data['punchline']
        await ctx.send(embed=em)

    # Cat
    @commands.command(aliases=['kittycat', 'cat'])
    async def kitty(self, ctx):
        '''Get a cat pic.'''
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
              if resp.status != 200:
                  return await ctx.send('No cat found :(')
              js = await resp.json()
              await ctx.send(embed=discord.Embed(title='Random Cat').set_image(url=js[0]['url']))

def setup(client):
    client.add_cog(Fun(client))