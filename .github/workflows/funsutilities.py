import discord
from discord.ext import commands
import os
import requests
import json
import random
from keep_alive import keep_alive
import asyncio
from discord import Color
import datetime
import aiofiles
import youtube_dl

client = commands.Bot(command_prefix = '+')

client.remove_command('help')

rolling = ["1", "2", "3", "4", "5", "6",]


def get_quote():
  response = requests.get ("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  # Setting `Playing ` status
  await client.change_presence(activity=discord.Game(name=f" With admins | +help"))

  # Setting `Streaming ` status
  await client.change_presence(activity=discord.Streaming(name="Among Us", url='https://www.twitch.tv/directory/game/Minecraft'))

  # Setting `Listening ` status
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="To you"))

  # Setting `Watching ` status
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Server Moderators"))


  print('Bot logged into server as {0.user}'.format(client))

async def ch_pr():
  await client.wait_until_ready()

  plays = ["+help", "Minecraft", "Fortnite", "Lets be awesome! | +help"]
  streams = ["Minecraft", "How to use a keyboard", "Fortnite", "Nothing"]
  listens = ["You", "Spotify", "Singers", "The coders singing", "Nothing", "Some music"]
  watches = ["Moderators", "For naughty people", "How to ban a person", "Something"]

  while not client.is_closed():

    rplays = random.choice(plays)
    rstream = random.choice(streams)
    rlisten = random.choice(listens)
    rwatch = random.choice(watches)

    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name=rplays))

    await asyncio.sleep(15)
    
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=rstream, url='https://twitch.tv/'))
    
    await asyncio.sleep(20)
    
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=rlisten))
    
    await asyncio.sleep(15)
    
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=rwatch))
    
    await asyncio.sleep(16)

client.loop.create_task(ch_pr())



@client.event
async def on_member_join(member):
  channel = client.get_channel(id=812241417493676082)
  await channel.send(f'Welcome to our server {member.mention}!')
  await member.send('Welcome to our server!')

@client.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f":white_check_mark: {member.mention} has been kicked")

@client.command(aliases=['p', 'q'])
async def ping(ctx, arg=None):
  if arg == "pong":
    await ctx.send('Noice job! You just ponged yourself >:)')
  else:
    await ctx.send(f'Pong! Here is your ping: {round(client.latency * 1000)}ms')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f" <:BlurpleBanHammer:808700770877964369> {member.mention} has been banned")
@client.command()
async def dice(ctx):
  uer_dice = random.choice(rolling)
  embed = discord.Embed(
    title = 'Rolling, rolling, rolling',
    description = 'Stats:',
    colour = discord.Colour.magenta()
  )

  embed.set_footer(text='Ok, its a dice machine ;)')
  embed.add_field(name='You rolled:', value=uer_dice, inline=False)

  await ctx.send(embed=embed)
@client.command()
async def game(ctx):
  user_dice = random.choice(rolling)
  bot_dice = random.choice(rolling)
  if user_dice > bot_dice:
    embed = discord.Embed(
      title = 'You winned',
      description = 'Stats:',
      colour = discord.Colour.green()
    )

    embed.set_footer(text='Gaming machine v10.0')
    embed.add_field(name='You rolled', value=user_dice, inline=True)
    embed.add_field(name='Bot rolled', value=bot_dice, inline=True)

    await ctx.send(embed=embed)
  if user_dice < bot_dice:
    embed = discord.Embed(
      title = 'Bot winned',
      description = 'Stats:',
      colour = discord.Colour.red()
    )

    embed.set_footer(text='Gaming machine v10.0')
    embed.add_field(name='You rolled', value=user_dice, inline=True)
    embed.add_field(name='Bot rolled', value=bot_dice, inline=True)

    await ctx.send(embed=embed)
  if user_dice == bot_dice:
    embed = discord.Embed(
      title = 'No winners!',
      description = 'Stats:',
      colour = discord.Colour.orange()
    )

    embed.set_footer(text='Gaming machine v10.0')
    embed.add_field(name='You rolled', value=user_dice, inline=True)
    embed.add_field(name='Bot rolled', value=bot_dice, inline=True)

    await ctx.send(embed=embed)
    

@client.command()
async def help(ctx, arg=None):
  if arg == None:
    embed = discord.Embed(
      title = 'Help page',
      description = 'Help pages:',
      colour = discord.Colour.blue()
    )

    embed.set_footer(text='Choose help page')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='My prefix is:', value='`+`')
    embed.add_field(name='Management', value='`+help management`', inline=False)
    embed.add_field(name='Fun', value='`+help fun`', inline=False)
    embed.add_field(name='Other commands', value='`+help other`', inline=False)
    embed.add_field(name='Economy commands', value='`+help economy`', inline=False)
    embed.add_field(name='Voice and Audio', value='`+help audio`')
    embed.add_field(name='Remember!', value='`ALL commands in Management commands tab are for members, who have administator permissions!`', inline=False) 

    await ctx.send(embed=embed)
  if arg == 'management':
    embed = discord.Embed(
      title = 'Management Commands',
      description = 'Commands list:',
      colour = discord.Colour.red()
    )

    embed.set_footer(text='These work only for admins!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Ban', value='`+ban [optional reason]`', inline=False)
    embed.add_field(name='Kick', value='`+kick [optional reason]`', inline=False)
    embed.add_field(name='Slowmode', value='`+slowmode [seconds]`', inline=False)
    embed.add_field(name='Nuke', value='`+nuke` - Nukes 100 messages in this channel', inline=False) 
    embed.add_field(name='Super Nuke', value='`+supernuke` - Nukes 1000 messages in this channel', inline=False)
    embed.add_field(name='THANOS NUKE TIME!', value='`+thanos` - Nukes ALL MESSAGES in this channel', inline=False) 

    await ctx.send(embed=embed)

  if arg == 'fun':
    embed = discord.Embed(
      title = 'Fun commands',
      description = 'Commands:',
      colour = discord.Colour.blue()
    )

    embed.set_footer(text='Choose your command!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Dice', value='`+dice` rolls a dice', inline=False)
    embed.add_field(name='Game', value='`+game` play a game with bot!', inline=False)

    await ctx.send(embed=embed)

  if arg == 'other':
    embed = discord.Embed(
      title = 'Other commands',
      description = 'Commands:',
      colour = discord.Colour.green()
    )

    embed.set_footer(text='Choose your command!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Ping', value='`+ping [optional: pong] ` Ping yourself', inline=False)
    embed.add_field(name='FAQ', value='`+faq [list or number(1-5)] ` Shows the FAQ, use this when you have problems. FAQ`s are from Funs Community server', inline=False)
    embed.add_field(name='Admin FAQ', value='`+adminfaq ` Shows the FAQ, use this when you have problems.', inline=False)
    embed.add_field(name='Bot FAQ', value='`+botfaq ` Shows the FAQ, use this when you have problems.', inline=False)
    embed.add_field(name='pfp', value='`+pfp [member.mention]` - Get a member`s pfp', inline=False)

    await ctx.send(embed=embed)
  if arg == 'economy':
    embed = discord.Embed(
      title = 'Economy commands',
      description = 'Commands:',
      colour = discord.Colour.green()
    )

    embed.set_footer(text='Choose your command!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Balance', value='`+balance` Shows your balance', inline=False)
    embed.add_field(name='Deposite money', value='`+deposite [amount]` deposite money (save it in the bank)', inline=False)
    embed.add_field(name='Withdraw money', value='`+withdraw [amount]` Withdraw money straight into your wallet', inline=False)
    embed.add_field(name='Shopping', value='`+shop` Shows items in shop', inline=False)

    await ctx.send(embed=embed)
  if arg == 'audio':
    embed = discord.Embed(
      title = 'Voice and Audio commands',
      description = 'Commands:',
      colour = discord.Colour.teal()
    )

    embed.set_footer(text='Choose your command!')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Bot join the VC', value='`+join [VC.name]` Bot is joining VC then', inline=False)
    embed.add_field(name='Play a song', value='`+play [url]` Bot plays the song URL then', inline=False)
    embed.add_field(name='Pause', value='`+pause` Stops audio playing', inline=False)
    embed.add_field(name='Resume', value='`+resume` Resumes audio', inline=False)
    embed.add_field(name='Leave', value='`+leave` Bot leaves VC', inline=False)
    embed.add_field(name='Stop audio', value='`+stop` Bot Stops the current audio and you can`t resume it', inline=False)
    await ctx.send(embed=embed)
  
  
@client.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    if seconds > 21600:
      await ctx.send("You are restricted to 21600 seconds!")
    if seconds < 0:
      await ctx.send("You can't set slowmode to this delay!")
    if seconds < 21601 and seconds > -1:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command()
async def botinfo(ctx):
  embed=discord.Embed(
    title='Bot stats:', 
    description = '', 
    colour = discord.Colour.gold()
  )
   
  embed.set_footer(text='Stats')
  embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
  embed.add_field(name='Lines of code:', value='`561`', inline=True)
  embed.add_field(name='Functions:', value='`43 [included 5 faqs]`', inline=True)
  embed.add_field(name='Im in servers:', value=f'`{len(client.guilds)}`')
   
  await ctx.send(embed=embed)

@client.command()
async def faq(ctx, arg=None):
  if arg == 'list':
    embed = discord.Embed(title='Showing faq list:', description='', colour=discord.Colour.gold())
    embed.set_footer(text="There are 5 faqs now")
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/813380083951337492/05a66befa8829b3e8df361af84ef4faf.webp')
    embed.add_field(name='Faq #1: Why rules exist?', value='type `+faq 1` to show more', inline=False)
    embed.add_field(name='Faq #2: Why I get warned?', value='type `+faq 2` to show more', inline=False)
    embed.add_field(name='Faq #3: What are bots?', value='type `+faq 3` to show more', inline=False)
    embed.add_field(name='Faq #4: What is leveling?', value='type `+faq 4` to show more', inline=False)
    embed.add_field(name='Faq #5: What is zalgo? Why I get warned for this?', value='type `+faq 5` to show more', inline=False)

    await ctx.send(embed=embed)

  if arg == '1':
    embed = discord.Embed(title='Faq #1: Why rules exist?', description='Rules are to keep server family-friendly. If someone brake rules, then will be warned. Ofc, if you will  continiue, this will result a mute/ban', colour=discord.Colour.teal())
    embed.set_footer(text="There are 5 faqs now. This is #1")

    await ctx.send(embed=embed)

  if arg == '2':
    embed = discord.Embed(title='Faq #2: Why I get warned?', description='Return to #1. If you brake rules, for using bad words, zalgo, etc.', colour=discord.Colour.magenta())
    embed.set_footer(text="There are 5 faqs now. This is #2")

    await ctx.send(embed=embed)

  if arg == '3':
    embed = discord.Embed(title='Faq #3: What are bots?', description='Bots are using to leveling, invites, and message system. If you level up, send some message, maybe you will get some perks: change nick, get acces to some channels.', colour=discord.Colour.red())
    embed.set_footer(text="There are 5 faqs now. This is #3")

    await ctx.send(embed=embed)

  if arg == '4':
    embed = discord.Embed(title='Faq #4: What is leveling?', description='Leveling, messaging and invite system is used to give you roles. Once you gain level, invite or send messages you will get a role', colour=discord.Colour.teal())
    embed.set_footer(text="There are 5 faqs now. This is #4")

    await ctx.send(embed=embed)

  if arg == '5':
    embed = discord.Embed(title='Faq #5: What is zalgo?', description='Zalgo is connecting letters with symbors, like T҉o', colour=discord.Colour.orange())
    embed.set_footer(text="There are 5 faqs now. This is #5")

    await ctx.send(embed=embed)

    
  
@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx, amount=100):
  await ctx.channel.purge(limit=amount)
  await ctx.send(':white_check_mark: Succesfully used `1 nuke` to nuke 100 messages in this channel')
  
@client.command()
@commands.has_permissions(administrator=True)
async def supernuke(ctx, amount=1000):
  await ctx.channel.purge(limit=amount)
  await ctx.send('Succesfully nuked 1000 messages using `1 Super Nuke`')
  
@client.command()
@commands.has_permissions(administrator=True)
async def thanos(ctx, amount=100000000):
  await ctx.channel.purge(limit=amount)
  embed = discord.Embed(
    title='Thanos is here! OH OH OH NO!', 
    description='Don`t, watch it kids!', 
    colour=discord.Colour.magenta()
  )
  embed.set_footer(text='Oh no!')
  embed.add_field(name='Thanos hacked!', value='Thanos hacked into server and nuked all messages is this channel! Holy bacons!<:Thanos:808700790717284383>', inline=False)
  await ctx.send(embed=embed)


@client.command(pass_context=True)
async def pfp(ctx, member : discord.Member, *, arg=None):
  embed = discord.Embed(title=f"{member.name}`s pfp", description='', colour=discord.Colour.red())
  embed.set_footer(text=f"Request by {ctx.author.name}")
  embed.set_image(url=f"{member.avatar_url}")
  
  await ctx.send(embed=embed)

mainshop = [{"name":"Watch", "price":1000, "description":"Watch out for some time!"},
            {"name":"PC", "price":12500, "description":"Play games with it"},
            {"name":"Car", "price":75250, "description":"Use it to ride"},
            {"name":"Dog", "price":250000, "description":"A happy funny dog!"},
            {"name":"NUKE", "price":1000000, "description":"Nukes channel"}]

@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  em = discord.Embed(title=f"Showing {ctx.author.name}`s balance", colour=discord.Colour.teal())
  em.add_field(name="Wallet balance", value=f":coin: {wallet_amt}", inline=True)
  em.add_field(name="Bank balance", value=f":coin: {bank_amt}", inline=True)
  await ctx.send(embed=em)



async def open_account(user):
  
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  return True

async def get_bank_data():
  with open("mainbank.json","r") as f:
    users = json.load(f)
  return users


@client.command()
async def beg(ctx):
  await open_account(ctx.author)
  
  users = await get_bank_data()

  user = ctx.author

  earning = random.randrange(250)

  await ctx.send(f"**Someone** donated :coin: {earning} to {ctx.author.name}")
  
  wallet_amt = users[str(user.id)]["wallet"] =  users[str(user.id)]["wallet"] + earning

  with open("mainbank.json","w") as f:
    json.dump(users,f)

@client.command()
async def deposite(ctx, number: int):
  await open_account(ctx.author)
  
  users = await get_bank_data()

  user = ctx.author

  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  if number <= wallet_amt:
    wallet_amt = users[str(user.id)]["wallet"] =  users[str(user.id)]["wallet"] - number
    bank_amt = users[str(user.id)]["bank"] = users[str(user.id)]["bank"] + number
    await ctx.send(f"{ctx.author.name} deposited :coin: {number} coins")
  else:
    await ctx.send("You cannot deposite this number of coins, you dumb!")

  with open("mainbank.json","w") as f:
    json.dump(users,f)

@client.command()
async def withdraw(ctx, number: int):
  await open_account(ctx.author)
  
  users = await get_bank_data()

  user = ctx.author

  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  if number <= bank_amt:
    wallet_amt = users[str(user.id)]["wallet"] =  users[str(user.id)]["wallet"] + number
    bank_amt = users[str(user.id)]["bank"] = users[str(user.id)]["bank"] - number
    await ctx.send(f"{ctx.author.name} withdrawed :coin: {number} coins!")
  else:
    await ctx.send("You cannot withdraw this number of coins, you dumb!")

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  
  


@client.command()
async def shop(ctx):
  em = discord.Embed(title='Here is our shop', colour=discord.Colour.magenta())

  for item in mainshop:
    name = item["name"]
    price = item["price"]
    description = item["description"]
    em.add_field(name=name, value=f"${price} | {description}", inline=False)

  await ctx.send(embed=em)



@client.command()
async def join(ctx, channel : str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voiceChannel.connect()
    await ctx.send("Succesfully joined :white_check_mark:")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        await ctx.send(":white_check_mark: Disconected")
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send(":white_check_mark: Paused")
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.resume()
    await ctx.send(":white_check_mark: Resumed")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send(":white_check_mark: Stopped")

# help on line 164
# info on line 258
# faq on line 274

keep_alive()
client.run(os.getenv('TOKEN'))
