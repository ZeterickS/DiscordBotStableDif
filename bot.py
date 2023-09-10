import discord
from discord.ext import commands
import requests as r
from Helper.StableDiff import Txt2ImgAPI, Img2ImgAPI
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TOKEN")

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


#TXT2IMG
messagePrompts = {}
regeneratedMessages = set()

@bot.command()
async def Txt2Img(ctx, *arg):
    print (ctx.author)

    if ctx.author == bot.user:
        return

    # Include in every command -> checks if Stable Diffusion on Lab Desktop is reachable
    try:
        CheckUptime()
    except:
        await ctx.channel.send("Error: Stable Diffusion is not Running! Cedric is offline.")
        return

    if not arg:
        await ctx.channel.send("Please provide a prompt!")
        return

    generatingImageMessage = await ctx.channel.send('Generating Image...')
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f'archive/output_{timestamp}+{ctx.author}.png'
    prompt = " ".join(arg)

    try:
        await Txt2ImgAPI(prompt, filename)
        imageMessage = await ctx.channel.send(file=discord.File(filename))
        await ctx.channel.send(f"<@{ctx.author.id}> {prompt}")
        await generatingImageMessage.delete()
        messagePrompts[imageMessage.id] = prompt
        await imageMessage.add_reaction("🔄")
    except Exception as e:
        await ctx.channel.send(f"An error occurred: {str(e)}")
        await generatingImageMessage.delete()
    
@bot.event
async def on_reaction_add(reaction, user): 
    if not user.bot and reaction.message.author == bot.user and str(reaction.emoji) == "🔄" and reaction.message.id not in regeneratedMessages:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f'archive/output_{timestamp}+{reaction.message.author}.png'
        prompt = messagePrompts.get(reaction.message.id, "Default Prompt")

        regeneratedMessages.add(reaction.message.id)
        
        #Same try except block as above / ctx is reaction here
        generatingImageMessage = await reaction.message.channel.send('Make simmilar image...')
        
        try:
            await Txt2ImgAPI(prompt, filename)
            newImageMessage = await reaction.message.channel.send(file=discord.File(filename))
            await reaction.message.channel.send(f"<@{reaction.message.author.id}> {prompt}")
            await generatingImageMessage.delete()
            await newImageMessage.add_reaction("🔄")
        except Exception as e:
            await reaction.message.channel.send(f"An error occurred: {str(e)}")
            await generatingImageMessage.delete()
    
#IMG2IMG
@bot.command()
async def Img2Img(ctx, *args):
    if ctx.author == bot.user:
        return

    # Include in every command -> checks if Stable Diffusion on Lab Desktop is reachable
    UptimeStatus = CheckUptime()
    if UptimeStatus == "Error":
        await ctx.channel.send("Error: Stable Diffusion is not Running! Cedric is offline.")
        return
    
    if ctx.message.attachments:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f'archive/output_{timestamp}+{ctx.author}.png'
        prompt = " ".join(args)
        for attachment in ctx.message.attachments:
            if attachment.url.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    await attachment.save(f'archive/{attachment.filename}')
                    await Img2ImgAPI(f'archive/{attachment.filename}' ,filename, prompt)
                    await ctx.channel.send(file=discord.File(filename))
                    await ctx.channel.send(f"<@{ctx.author.id}> {prompt}")
                except Exception as e:
                    await ctx.channel.send("Error...")
    else:
        await ctx.channel.send("No image provided. Please attach a image to your message!")
                


bot.run(token)