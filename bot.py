import discord
from discord.ext import commands
import requests as r
from Helper.StableDiff import Txt2ImgAPI
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

def CheckUptime():
    try:
        r.get("http://192.168.178.21:7860")
        return "Worked!"
    except:
        return "Error"
        
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def Txt2Img(ctx, *arg):
    print (ctx.author)

    if ctx.author == bot.user:
        return

    # Include in every command -> checks if Stable Diffusion on Lab Desktop is reachable
    UptimeStatus = CheckUptime()
    if UptimeStatus == "Error":
        await ctx.channel.send("Error: Stable Diffusion is not available on LabDesktop!")
        return

    if not arg:
        await ctx.channel.send("Please provide a prompt!")

    await ctx.channel.send('On it!')

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f'archive/output_{timestamp}+{ctx.author}.png'

    try:
        await Txt2ImgAPI(" ".join(arg), str(ctx.author), filename)
        await ctx.channel.send(file=discord.File(filename))
    except Exception as e:
        await ctx.channel.send(f"An error occurred: {str(e)}")

bot.run("")