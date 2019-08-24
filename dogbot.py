#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bs4 import BeautifulSoup as bs
import os
import requests
import re
import random

def cssformat(input):
    return "```css\n" + input + "```"


def htmlformat(input):
    return "```html\n" + input + "```"


def bold(input):
    return "**" + input + "**"


bot = commands.Bot(command_prefix='!')
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/DogBot/" % (HOMEDIR)
bot.remove_command('help')

with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

@bot.command(name='dogbot', pass_context=True)
async def dogbot(ctx):
    embed = discord.Embed(title="𝐃𝐨𝐠𝐁𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:", description=" ", color=0xeee657)
    embed.add_field(name="!streams", value="Displays currently running ROR twitch streams.", inline=False)
    embed.add_field(name="!dice", value="Rolls the dices! Syntax: !dice <amount of dices> <number>.", inline=False)
    embed.add_field(name="!warpop", value="Displays the current amount of population on the server, and currently players in T1 and T2+ ( excluding anonymous players)", inline=False)
    embed.add_field(name="!serverinvite", value="Generates an invitelink to this Discord server. Will be sent to you in a private message.", inline=False)
    embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/81-yKbVND-L._SY355_.png")
    await bot.say(embed=embed)


@bot.command(name='warpop', pass_context=True)
async def warpop():
    htmldata = requests.get('https://www.returnofreckoning.com/whos_online.php').text
    soup = bs(htmldata, "html5lib")
    pop = soup.find(class_="realm-info realm-info-detail").getText()
    pop = pop.replace("Total :", "")
    pop = pop.replace("Faction ratio (Order/Destruction) :", "")
    pop = pop.replace(":", "")
    pop = pop.replace("Martyrs Square (EN)", "")
    pop = pop.strip().splitlines()
    pop = list(filter(None, pop))
    pop = '\n'.join(pop)
    await bot.say(cssformat(str(pop)))


@bot.command(name='streams', pass_context=True)
async def streams():
    htmldata = requests.get('https://www.returnofreckoning.com/')
    soup = bs(htmldata.text, 'html5lib')
    outstuff = []
    for link in soup.findAll(class_="topictitle"):
        outstuffers = link.getText().rstrip()
        outstuff.append(" ⟿  "  + "[" + str(outstuffers) + "]" + "(" + link.get('href') + ")" + "£")
    outstuff = ''.join(outstuff)
    outstuff = outstuff.replace("£", "\n")
    embed=discord.Embed(title=" ")
    embed.add_field(name="Currently running ROR Streams:", value=str(outstuff), inline=False)
    await bot.say(embed=embed) 


@bot.command(name='dice', pass_context=True)
async def dice(ctx, arg, arg1):
    min = 1
    max = int(arg1)
    if int(arg) >= 6:
        await bot.say("To many dices, try 5 or less")
    else:
        number = []
        for i in range(1, int(arg)+1):
            number.append(random.randint(min, max))
        number = number.replace(",", "\n")
    await bot.say("The dice(s) tumbles and rolls for " + ctx.message.author.mention + " and it gives the numbers: " + cssformat(str(number)))
    await bot.say(cssformat(bold(str(number))))


@bot.command(name='serverinvite', pass_context=True)
async def inv(ctx ):
    invite = await bot.create_invite(ctx.message.channel, max_uses=1, xkcd=True)
    await bot.send_message(ctx.message.author, "Invite URL is {}".format(invite.url))
    await bot.say(ctx.message.author.mention + " Invite URL generated, check your PM's! ")


@bot.event
async def on_ready():
    print("Connected!")
    await bot.change_presence(game=discord.Game(name="Doge Of War"))

bot.run(TOKEN)
