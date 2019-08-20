#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bs4 import BeautifulSoup as bs
import os

client = discord.Client()


def cssformat(input):
    return "```css\n" + input + "```"


def htmlformat(input):
    return "```html\n" + input + "```"


bot = commands.Bot(command_prefix='!')
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/DogBot/" % (HOMEDIR)
bot.remove_command('help')

with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

@bot.command(name='warpop', pass_context=True)
async def warpop():
    htmldata = requests.get('https://www.returnofreckoning.com/whos_online.php').text
    soup = bs(htmldata, 'lxml')
    pop = soup.find(class_="realm-info realm-info-detail").getText()
    pop = pop.replace("Total :", "")
    pop = pop.replace("Faction ratio (Order/Destruction) :", "")
    pop = pop.replace(":", "")
    pop = pop.replace("Martyrs Square (EN)", "")
    pop = pop.strip().splitlines()
    pop = list(filter(None, pop))
    pop = '\n'.join(pop)
    await bot.say(cssformat(str(*pop, sep = "\n")))


@bot.command(name='!streams', pass_context=True)
async def streams():
htmldata = requests.get('https://www.returnofreckoning.com/')
soup = bs(htmldata.text, 'lxml')
for link in soup.findAll(class_="topictitle"):
	titles = link.text
	streams = link.get('href')
	await bot.say(titles + " -> " + streams)

	
@bot.command(name='why', pass_context=True)
async def why(ctx):
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
    await bot.say(random.choice(soppa))


@client.event
async def on_ready():
    print("Connected!")
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name="Doge Of War"))

client.run(TOKEN)
