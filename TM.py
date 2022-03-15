import discord
from discord.ext import commands,tasks
from discord.ext.commands import BucketType
import pymongo
import asyncio
import datetime
from TMClass import UserProfiles, Profiles
from TMclassv2 import Reaction


#chen email
client = pymongo.MongoClient("mongodb+srv://starlord:Adeoluwa.05@playerinfo.t5g9l.mongodb.net/myFirstDatabase&retryWrites=true&w=majority?ssl=true&ssl_cert_reqs=CERT_NONE",connect=False)
db = client.games
RL = db.RocketLeague
dbv2 = client.Match
match = dbv2.Maker
dbv3 = client.Profile
profiling = dbv3.User
dbv4 = client.black
BL = dbv4.list
rbx = db.Roblox
MC = db.MC
val = db.valorant
fort = db.fortnite
#main email
client = pymongo.MongoClient('mongodb+srv://starlord:Adeoluwa.05@cluster0.52enc.mongodb.net/myFirstDatabase&retryWrites=true&w=majority?ssl=true&ssl_cert_reqs=CERT_NONE',connect=False)
db = client.server
connected = db.matches

supported = ['RL','rl','Roblox','roblox','MC','mc','Mc','Val','val','Fortnite','fortnite']
intents = discord.Intents.default()
intents.members = True
async def get_pre(bot, message):
    return ['tm!','TM!','Tm!','tM!']

bot = commands.Bot(command_prefix=get_pre,case_insensitive=True,intents=intents,status=discord.Status.dnd,activity=discord.Activity(name='TM!help',type=discord.ActivityType.watching))
bot.remove_command('help')
UserProfiles = UserProfiles(bot)
Profiles = Profiles()
Reaction = Reaction(bot)
@bot.event
async def on_command(ctx):
    channel = bot.get_channel(827601440666288139)
    await channel.send(f'`{ctx.command}` was used')


@bot.event
async def on_member_join(member):
    if member.guild.id == 802368481840332820:
        #find if just the key is matching
        x = connected.find_one({}, {f'{member.id}':0,'_id':0})
        if not x:
            x = connected.find_one({}, {f'{member.id}':1,'_id':0})
        z = list(x.keys())
        a = list(x.values())
        if x == None:
            return
        else:
            y = bot.get_guild(802368481840332820)
            for channel in y.channels:
                if channel.name in z or channel.name in a or channel.name in str(member.id):
                    try:
                        try:
                            await channel.set_permissions(member, read_messages=True, send_messages=True,view_channel = True)
                        except Exception as e:
                            perms = discord.PermissionOverwrite()
                            perms.speak = True
                            perms.connect = True
                            perms.view_channel = True
                            await channel.set_permissions(member, overwrite=perms)
                    except Exception as ex:
                        pass

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.BotMissingPermissions):
        await ctx.send('Error: I am missing the permssions to operate properly. Please fix my permssions.')
    elif isinstance(error,commands.NoPrivateMessage):
        embed = discord.Embed(title='While running, an error occured.', description='This command doesnt work in dm\'s please try it in a guild.', color=0xCC071F)
        await ctx.send(embed = embed)
    elif isinstance(error,commands.CommandNotFound):
        return
    elif isinstance(error,commands.MissingPermissions):
        return
    else:
        await ctx.send(error)
        await ctx.send('If this problem consists, please join our support and send a screenshot of your issue.')


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title=f'Added to the guild: {guild.name}',
        description=f'The bot is now in {len(bot.guilds)} guilds!',
        color = discord.Color.green()
    )
    embed.add_field(name='**Owner**',value=f'{guild.owner.mention}|{guild.owner.id}',inline=False)
    embed.add_field(name='**Member Count**',value=f'{guild.member_count} members',inline=False)
    embed.add_field(name='**Boost Count**',value=f'{guild.premium_subscription_count} boosts',inline=False)
    embed.set_thumbnail(url=f'{guild.icon_url}')
    embed.set_footer(text=f'{guild.id} | {len(bot.users)} users')
    embed.timestamp = datetime.datetime.utcnow()
    ctx = bot.get_channel(822858833093066752)
    await ctx.send(embed = embed)

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
        title=f'Removed from the guild: {guild.name}',
        description=f'The bot is now in {len(bot.guilds)} guilds!',
        color = discord.Color.red())
    embed.add_field(name='**Owner**',value=f'{guild.owner.mention}|{guild.owner.id}',inline=False)
    embed.add_field(name='**Member Count**',value=f'{guild.member_count} members',inline=False)
    embed.add_field(name='**Boost Count**',value=f'{guild.premium_subscription_count} boosts',inline=False)
    embed.set_thumbnail(url=f'{guild.icon_url}')
    embed.set_footer(text=f'{guild.id} | {len(bot.users)} users')
    embed.timestamp = datetime.datetime.utcnow()
    ctx = bot.get_channel(822858833093066752)
    await ctx.send(embed = embed)




@bot.command()
@commands.max_concurrency(1,per=BucketType.user,wait=False)
async def setup(ctx):
    """Set up your personal profile using this command"""
    x = Profiles.profiles(ctx.author.id)
    embed = discord.Embed(title=f'New Profile Setup by {ctx.author}',color=0xCC071F)
    if (ctx.message.guild == None):
        embed.add_field(name='Command ran in DMS',value='\u200b',inline=False)
    else:
        embed.add_field(name = f'Guild:',value=f'{ctx.guild}')
    channel = bot.get_channel(826331977257844746)
    await channel.send(embed = embed)
    perp = Profiles.blacklisted(ctx.author.id)
    if perp != None:
        embed = discord.Embed(title=f'Error: You have been blacklisted from our services for: {perp.get("reason")} ',description='If You wish to appeal your sentence than please join our support server [here](https://discord.gg/5XAubY2v3N) and open a ticket.',color=0xCC071F)
        await ctx.send(embed = embed)
    else:
        if x != None:
            await ctx.send('Error: You have already set up a profile. To add games to your profile use the `TM!addgame` command')
            return
        else:
            embed = discord.Embed(title=f'Profile Setup for {ctx.author.name}',color=0xCC071F)
            embed.add_field(name=f'To setup your profile you first have to give a me one game that you play.',value='To find all the currently supported games please try `TM!games`')
            embed.set_footer(text='To add any more games to your profile try TM!addgame command')
            await ctx.send(embed = embed)
            def check(message):
                return (message.content in supported) and (message.channel == ctx.channel) and (message.author == ctx.author)
            try:
                msg = await bot.wait_for('message',timeout=30,check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didnt respond... Cancelling setup.')
            else:
                if msg.content == 'RL' or msg.content == 'rl':
                    embed = discord.Embed(title='What is your Rocket League rank?',description='The ranks are from lowest to highest:** bronze, silver, gold, platinum, diamond, gc, ssl**',color=0xCC071F)
                    embed.add_field(name='you can either choose your 1\'s 2\'s or 3\'s',value='Please also just put your rank not tier.',inline=False)
                    embed.add_field(name='When putting in your rank please be truthful for this is to help you find a teammate around your rank.',value='if put in a False rank you account can be reported. Then can be blacklisted from our services.')
                    embed.set_footer(text='When saying your rank please do it as exactly as you see above.')
                    await ctx.send(embed = embed)
                    rank = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'gc', 'ssl','Bronze','Silver','Gold','Platinum','Diamond','Gc','Ssl']

                    def check(message):
                        return message.content in rank and (message.channel == ctx.channel) and (message.author == ctx.author)
                    try:
                        answer = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia', 'australia']
                        embed = discord.Embed(title='Where are you from?',
                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                              color=0xCC071F)
                        embed.add_field(name='The supported locations are as followed.',
                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                        embed.set_footer(
                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                        await ctx.send(embed=embed)

                        def check(message):
                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                        try:
                            location = await bot.wait_for('message', timeout=30, check=check)
                        except asyncio.TimeoutError:
                            await channel.send('You didnt respond... Cancelling setup.')
                        else:
                            location = location.content.lower()
                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                            profiling.insert_one(Profile)
                        answer = answer.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',description='If you want to find a partner right away then try my `TM!search` command.',color=0xCC071F)
                        rl = {'user': ctx.author.id,'rank':f'{answer}'}
                        RL.insert_one(rl)
                        await ctx.send(embed = embed)
                elif msg.content =='Roblox' or msg.content =='roblox':
                    embed = discord.Embed(title='What is your Roblox username?',color=0xCC071F)
                    await ctx.send(embed = embed)
                    def check(message):
                        return (message.channel == ctx.channel) and (message.author == ctx.author)
                    try:
                        answer = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia', 'australia']
                        embed = discord.Embed(title='Where are you from?',
                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                              color=0xCC071F)
                        embed.add_field(name='The supported locations are as followed.',
                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                        embed.set_footer(
                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                        await ctx.send(embed=embed)

                        def check(message):
                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                        try:
                            location = await bot.wait_for('message', timeout=30, check=check)
                        except asyncio.TimeoutError:
                            await channel.send('You didnt respond... Cancelling setup.')
                        else:
                            location = location.content.lower()
                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                            profiling.insert_one(Profile)
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        await ctx.send(embed = embed)
                        rbx.insert_one({'user':ctx.author.id,'name':f'{answer.content}'})
                elif msg.content == 'MC' or msg.content == 'mc' or msg.content == 'Mc':
                    embed = discord.Embed(title='Do you play Minecraft Java or Bedrock?', color=0xCC071F)
                    await ctx.send(embed=embed)
                    platform = ['Java','java','Bedrock','bedrock']
                    def check(message):
                        return (message.content in platform) and (message.channel == ctx.channel) and (message.author == ctx.author)
                    try:
                        platform = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        platform = platform.content.lower()
                        if platform == 'java':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',description='Survival \n PVP: ex.Hypixel Network \n Modded: ex. FeedTheBeast minecraft modpacks',color=0xCC071F)
                            embed.set_footer(text='To change this you are going to have to delete and readd this to your profile')
                            await ctx.send(embed = embed)
                            gamemode = ['Survival','survival','PVP','pvp','Pvp','Modded','modded']
                            def check(message):
                                return (message.content in gamemode) and (message.channel == ctx.channel) and (message.author == ctx.author)
                            try:
                                mode = await bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await ctx.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?',color=0xCC071F)
                                await ctx.send(embed = embed)
                                def check(message):
                                    return(message.channel == ctx.channel) and (
                                                message.author == ctx.author)
                                try:
                                    IGN = await bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    if mode =='pvp':
                                        embed = discord.Embed(title='What are your current stars. In Hypixel (the only current supported server)',description='Choose any pvp mod you want',color=0xCC071F)
                                        await ctx.send(embed = embed)
                                        def check(message):
                                            return (message.channel == ctx.channel) and (message.author == ctx.author)
                                        try:
                                            stars = await bot.wait_for('message',timeout=30,check=check)
                                        except asyncio.TimeoutError:
                                            await ctx.send('You didnt respond... Cancelling setup.')
                                        else:
                                            region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia',
                                                      'australia']
                                            embed = discord.Embed(title='Where are you from?',
                                                                  description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                                                  color=0xCC071F)
                                            embed.add_field(name='The supported locations are as followed.',
                                                            value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                                            embed.set_footer(
                                                text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                                            await ctx.send(embed=embed)

                                            def check(message):
                                                return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                                            try:
                                                location = await bot.wait_for('message', timeout=30, check=check)
                                            except asyncio.TimeoutError:
                                                await channel.send('You didnt respond... Cancelling setup.')
                                            else:
                                                location = location.content.lower()
                                                Profile = {'user': ctx.author.id, 'region': f'{location}'}
                                                profiling.insert_one(Profile)
                                            stars = int(stars.content)
                                            embed = discord.Embed(title='Succesfully set up your account',
                                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                                  color=0xCC071F)
                                            info = {'user':ctx.author.id,'platform':f'{platform}','mode':'pvp','IGN':f'{IGN}','stars':stars}
                                            MC.insert_one(info)
                                            await ctx.send(embed = embed)
                                    elif mode == 'survival':
                                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia',
                                                  'australia']
                                        embed = discord.Embed(title='Where are you from?',
                                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                                              color=0xCC071F)
                                        embed.add_field(name='The supported locations are as followed.',
                                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                                        embed.set_footer(
                                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                                        await ctx.send(embed=embed)

                                        def check(message):
                                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                                        try:
                                            location = await bot.wait_for('message', timeout=30, check=check)
                                        except asyncio.TimeoutError:
                                            await channel.send('You didnt respond... Cancelling setup.')
                                        else:
                                            location = location.content.lower()
                                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                                            profiling.insert_one(Profile)
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                                  color=0xCC071F)
                                        info = {'user':ctx.author.id,'platform':f'{platform}','mode':'survival','IGN':f'{IGN}'}
                                        MC.insert_one(info)
                                        await ctx.send(embed = embed)


                                    elif mode == 'modded':
                                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia',
                                                  'australia']
                                        embed = discord.Embed(title='Where are you from?',
                                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                                              color=0xCC071F)
                                        embed.add_field(name='The supported locations are as followed.',
                                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                                        embed.set_footer(
                                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                                        await ctx.send(embed=embed)

                                        def check(message):
                                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                                        try:
                                            location = await bot.wait_for('message', timeout=30, check=check)
                                        except asyncio.TimeoutError:
                                            await channel.send('You didnt respond... Cancelling setup.')
                                        else:
                                            location = location.content.lower()
                                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                                            profiling.insert_one(Profile)
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                                              color=0xCC071F)

                                        info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'modded',
                                                'IGN': f'{IGN}'}
                                        MC.insert_one(info)
                                        await ctx.send(embed=embed)
                        elif platform == 'bedrock':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
                                                  description='Survival \n PVP: ex.Cubed Network',
                                                  color=0xCC071F)
                            embed.set_footer(
                                text='To change this you are going to have to delete and read this to your profile')
                            await ctx.send(embed=embed)
                            gamemode = ['Survival', 'survival', 'PVP', 'pvp','Pvp']
                            def check(message):
                                return (message.content in gamemode) and (message.channel == ctx.channel) and (
                                            message.author == ctx.author)
                            try:
                                mode = await bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await ctx.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
                                await ctx.send(embed=embed)

                                def check(message):
                                    return (message.channel == ctx.channel) and (
                                            message.author == ctx.author)

                                try:
                                    IGN = await bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia',
                                              'australia']
                                    embed = discord.Embed(title='Where are you from?',
                                                          description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                                          color=0xCC071F)
                                    embed.add_field(name='The supported locations are as followed.',
                                                    value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                                    embed.set_footer(
                                        text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                                    await ctx.send(embed=embed)

                                    def check(message):
                                        return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                                    try:
                                        location = await bot.wait_for('message', timeout=30, check=check)
                                    except asyncio.TimeoutError:
                                        await channel.send('You didnt respond... Cancelling setup.')
                                    else:
                                        location = location.content.lower()
                                        Profile = {'user': ctx.author.id, 'region': f'{location}'}
                                        profiling.insert_one(Profile)
                                    embed = discord.Embed(title='Succesfully set up your account',
                                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                                          color=0xCC071F)
                                    MC.insert_one({'user':ctx.author.id,'platform':'bedrock','mode':f'{mode}','IGN':f'{IGN}'})
                                    await ctx.send(embed = embed)
                elif msg.content == 'Val' or msg.content == 'val':
                    embed = discord.Embed(title='What is your Valorant rank?',description='The ranks are from lowest to highest:**bronze, iron, silver, gold, platinum, diamond, immortal, radiant**',color=0xCC071F)
                    embed.add_field(name='Please be Truthful when inserting your rank.',value='If found and reported inserting a incorrect rank you can and will be blacklisted from our services.')
                    await ctx.send(embed = embed)
                    rank = ['iron','bronze','silver','gold','platinum','diamond','immortal','radiant','Iron','Bronze','Silver','Gold','Platinum','Diamond','Immortal','Radiant']
                    def check(message):
                        return message.content in rank and message.author == ctx.author and message.channel == ctx.channel
                    try:
                        rank = await bot.wait_for('message',timeout=45,check = check)
                    except asyncio.TimeoutError:
                        await ctx.send('Error: You didnt respond in time... Cancelling setup.')
                    else:
                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia', 'australia']
                        embed = discord.Embed(title='Where are you from?',
                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                              color=0xCC071F)
                        embed.add_field(name='The supported locations are as followed.',
                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                        embed.set_footer(
                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                        await ctx.send(embed=embed)

                        def check(message):
                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                        try:
                            location = await bot.wait_for('message', timeout=30, check=check)
                        except asyncio.TimeoutError:
                            await channel.send('You didnt respond... Cancelling setup.')
                        else:
                            location = location.content.lower()
                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                            profiling.insert_one(Profile)
                        rank = rank.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        val.insert_one({'user':ctx.author.id,'rank':f'{rank}'})
                        await ctx.send(embed = embed)
                elif msg.content == 'Fortnite' or msg.content == 'fortnite':
                    embed = discord.Embed(title='What League are you currently in?',description='The leagues are from lowest to highest:**Open, Contender, Champion**',color=0xCC071F)
                    await ctx.send(embed = embed)
                    rank  = ['open','Open','Contender','contender','Champion','champion']
                    def check(message):
                        return message.content in rank and message.channel == ctx.channel and message.author == ctx.author
                    try:
                        rank = await bot.wait_for('message',timeout=30,check =check)
                    except asyncio.TimeoutError:
                        await ctx.send('Error: You didnt respond in time... Cancelling setup.')
                    else:
                        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia', 'australia']
                        embed = discord.Embed(title='Where are you from?',
                                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                                              color=0xCC071F)
                        embed.add_field(name='The supported locations are as followed.',
                                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
                        embed.set_footer(
                            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
                        await ctx.send(embed=embed)

                        def check(message):
                            return message.content in region and message.author == ctx.author and message.channel == ctx.channel

                        try:
                            location = await bot.wait_for('message', timeout=30, check=check)
                        except asyncio.TimeoutError:
                            await channel.send('You didnt respond... Cancelling setup.')
                        else:
                            location = location.content.lower()
                            Profile = {'user': ctx.author.id, 'region': f'{location}'}
                            profiling.insert_one(Profile)
                        rank = rank.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        fort.insert_one({'user': ctx.author.id, 'rank': f'{rank}'})
                        await ctx.send(embed=embed)







@setup.error
async def setup_error(ctx,error):
    if isinstance(error,commands.MaxConcurrencyReached):
        await ctx.send('Your already running this command.')


@bot.command()
async def games(ctx):
    """All of this bots supported games."""
    embed = discord.Embed(title='All the currently supported games on our platform', color=0xCC071F)
    embed.add_field(name='\u200b',value='Rocket League: RL \n Roblox \n Minecraft: MC\n Valorant: Val \n Fortnite')
    embed.set_footer(text='If a game your play isnt on here and you want it to be added try the TM!suggest command')
    await ctx.send(embed = embed)

@bot.command()
@commands.max_concurrency(1,per=BucketType.user,wait=False)
@commands.guild_only()
async def search(ctx):
    """Search for a teammate."""
    user = None
    looking = {'user':ctx.author.id}
    found = match.find_one(looking)
    if found != None:
        await ctx.send(
            'Error: You already have a search running. If you are trying to cancel your search please do the `TM!cancel` command.')
    else:
        info = {'user': ctx.author.id}
        x = RL.find_one(info)
        z = profiling.find_one(info)
        if z == None:
            await ctx.send('Error you didn\'t set up your profile. Please do `TM!setup` to do that.')
        else:
            embed = discord.Embed(title='What game are you trying to find a teammate for?',description='Make sure you have the game set up in your profile.',color=0xCC071F)
            await ctx.send(embed = embed)
            def check(message):
                return message.content in supported and message.author == ctx.author and message.channel == ctx.message.channel
            try:
                game = await bot.wait_for('message',timeout=30,check = check)
            except asyncio.TimeoutError:
                await ctx.send('You took to long to answer...Cancelling.')
            else:
                if game.content == 'RL' or game.content == 'rl':
                    embed = discord.Embed(title='Now Searching for teammates for the game: Rocket League',description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',color=0xCC071F)
                    await ctx.send(embed = embed)
                    info = {'game':'RL','rank': f"{x.get('rank')}",'region':f"{z.get('region')}"}
                    y = match.find(info)
                    num = match.count(info)
                    if num == 0:
                        y = dict(y)
                    for info in y:
                        id = info.get('user')
                        user = bot.get_user(id)
                    if not y:
                        info = {'game':'RL','user': ctx.author.id, 'rank': f"{x.get('rank')}",'region':f"{z.get('region')}", 'time': 0}
                        match.insert_one(info)
                    if user == None:
                        return
                    else:
                        mel = await UserProfiles.teammateyes(ctx,user)
                        if mel == False:
                            embed=discord.Embed(title='Alright. Removing you from the Queue.',description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',color=0xCC071F)
                            await user.send(embed = embed)
                            match.delete_one({"user": user.id})
                            info = {'game':'RL','user': ctx.author.id, 'rank': f"{x.get('rank')}",'region':f"{z.get('region')}", 'time': 0}
                            match.insert_one(info)


                elif game.content == 'Roblox' or game.content == 'roblox':
                    if rbx.find_one({'user':ctx.author.id}) == None:
                        await ctx.send('Error: You havnt added this game to your profile. Please do that with `TM!addgame`.')
                    else:
                        embed = discord.Embed(title='Now Searching for teammates for the game: Roblox',
                                              description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                              color=0xCC071F)
                        await ctx.send(embed=embed)
                        info = {'game': 'RBX', 'region': f"{z.get('region')}"}
                        y = match.find(info)
                        num = match.count(info)
                        if num == 0:
                            y = dict(y)
                        for info in y:
                            id = info.get('user')
                            user = bot.get_user(id)
                        if not y:
                            info = {'user': ctx.author.id, 'game': "RBX", 'region': f"{z.get('region')}",
                                    'time': 0}
                            match.insert_one(info)
                        if user == None:
                            return
                        else:
                            mel = await UserProfiles.teammateyes(ctx, user)
                            if mel == False:
                                embed = discord.Embed(title='Alright. Removing you from the Queue.',
                                                      description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',
                                                      color=0xCC071F)
                                await user.send(embed=embed)
                                match.delete_one({"user": user.id})
                                info = {'user': ctx.author.id, 'game': "RBX", 'region': f"{z.get('region')}",
                                        'time': 0}
                                match.insert_one(info)
                elif game.content == 'MC' or game.content == 'mc' or game.content == 'Mc':
                    if MC.find_one({'user':ctx.author.id}) == None:
                        await ctx.send('Error you have not setup this game in your profile. Please do so with `TM!addprofile`.')
                    else:
                        embed = discord.Embed(title='Now Searching for teammates for the game: Minecraft',
                                          description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                          color=0xCC071F)
                        await ctx.send(embed = embed)
                        yz = MC.find_one({'user':ctx.author.id})
                        if yz.get('stars') != None:
                            star = Profiles.MC_ranks(yz.get('stars'))
                            info = {'game': 'MC', 'region': f"{z.get('region')}",
                                    'rank': f'{star}',
                                    'platform': f'{yz.get("platform")}'}
                        else:
                            info = {'game': 'MC', 'region': f"{z.get('region')}",
                                    'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}'}
                        y = match.find(info)
                        num = match.count(info)
                        if num == 0:
                            y = dict(y)
                        for info in y:
                            id = info.get('user')
                            user = bot.get_user(id)
                        if not y:
                            if yz.get('stars') != None:
                                star = Profiles.MC_ranks(yz.get('stars'))
                                info = {'user': ctx.author.id,'game': 'MC', 'region': f"{z.get('region')}", 'rank': f'{star}',
                                        'platform': f'{yz.get("platform")}','time':0}
                            else:
                                info = {'user': ctx.author.id,'game': 'MC', 'region': f"{z.get('region')}",
                                        'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}','time':0}
                            match.insert_one(info)
                        if user == None:
                            return
                        else:
                            mel = await UserProfiles.teammateyes(ctx, user)
                            if mel == False:
                                embed = discord.Embed(title='Alright. Removing you from the Queue.',
                                                      description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',
                                                      color=0xCC071F)
                                await user.send(embed=embed)
                                match.delete_one({"user": user.id})
                                if yz.get('stars') != None:
                                    star = Profiles.MC_ranks(yz.get('stars'))
                                    info = {'user': ctx.author.id, 'game': 'MC', 'region': f"{z.get('region')}",
                                            'rank': f'{star}',
                                            'platform': f'{yz.get("platform")}'}
                                else:
                                    info = {'user': ctx.author.id, 'game': 'MC', 'region': f"{z.get('region')}",
                                            'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}','time':0}
                                match.insert_one(info)
                elif game.content == 'Val' or game.content == 'val':
                    if val.find_one({'user':ctx.author.id}) == None:
                        await ctx.send('Error you have not setup this game in your profile. Please do so with `TM!addprofile`.')
                    else:
                        embed = discord.Embed(title='Now Searching for teammates for the game: Valorant',
                                              description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                              color=0xCC071F)
                        await ctx.send(embed=embed)
                        x = val.find_one({'user':ctx.author.id})
                        info = {'game': 'Val', 'rank': f"{x.get('rank')}", 'region': f"{z.get('region')}"}
                        y = match.find(info)
                        num = match.count(info)
                        if num == 0:
                            y = dict(y)
                        for info in y:
                            id = info.get('user')
                            user = bot.get_user(id)
                        if not y:
                            info = {'game': 'Val', 'user': ctx.author.id, 'rank': f"{x.get('rank')}",
                                    'region': f"{z.get('region')}", 'time': 0}
                            match.insert_one(info)
                        if user == None:
                            return
                        else:
                            mel = await UserProfiles.teammateyes(ctx, user)
                            if mel == False:
                                embed = discord.Embed(title='Alright. Removing you from the Queue.',
                                                      description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',
                                                      color=0xCC071F)
                                await user.send(embed=embed)
                                match.delete_one({"user": user.id})
                                info = {'game': 'Val', 'user': ctx.author.id, 'rank': f"{x.get('rank')}",
                                        'region': f"{z.get('region')}", 'time': 0}
                                match.insert_one(info)
                elif game.content == 'Fortnite' or game.content == 'fortnite':
                    if fort.find_one({'user':ctx.author.id}) == None:
                        await ctx.send('Error you have not setup this game in your profile. Please do so with `TM!addprofile`.')
                    else:
                        embed = discord.Embed(title='Now Searching for teammates for the game: Fortnite',
                                              description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                              color=0xCC071F)
                        await ctx.send(embed=embed)
                        x = fort.find_one({'user':ctx.author.id})
                        info = {'game': 'Fort', 'rank': f"{x.get('rank')}", 'region': f"{z.get('region')}"}
                        y = match.find(info)
                        num = match.count(info)
                        if num == 0:
                            y = dict(y)
                        for info in y:
                            id = info.get('user')
                            user = bot.get_user(id)
                        if not y:
                            info = {'game': 'Fort', 'user': ctx.author.id, 'rank': f"{x.get('rank')}",
                                    'region': f"{z.get('region')}", 'time': 0}
                            match.insert_one(info)
                        if user == None:
                            return
                        else:
                            mel = await UserProfiles.teammateyes(ctx, user)
                            if mel == False:
                                embed = discord.Embed(title='Alright. Removing you from the Queue.',
                                                      description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',
                                                      color=0xCC071F)
                                await user.send(embed=embed)
                                match.delete_one({"user": user.id})
                                info = {'game': 'Fort', 'user': ctx.author.id, 'rank': f"{x.get('rank')}",
                                        'region': f"{z.get('region')}", 'time': 0}
                                match.insert_one(info)







@search.error
async def search_error(ctx,error):
    if isinstance(error,commands.MaxConcurrencyReached):
        await ctx.send('Error: You already have a search running. If you are trying to cancel your search please do the `TM!cancel` command.')


@bot.command()
async def cancel(ctx):
    """cancel your search"""
    x = match.find_one({"user": ctx.author.id})
    if x == None:
        await ctx.send('You dont have a current running search to cancel.')
    else:
        embed = discord.Embed(title='Are you sure you want to cancel your search?',description='Yes or No?',color=0xCC071F)
        await ctx.send(embed = embed)
        abcd = ['Yes','yes','y','Y','No','no','n','N']
        def check(message):
            return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel
        try:
            answer = await bot.wait_for('message',timeout=30,check=check)
        except asyncio.TimeoutError:
            await ctx.send('You took to long... Not cancelling your search.')
        else:
            if answer.content == 'yes' or answer.content == 'Yes' or answer.content == 'y' or answer.content == 'Y':
                try:
                    match.delete_one({"user": ctx.author.id})
                    await ctx.send('Search succesfully canclled')
                except:
                    await ctx.send('Having trouble deleting your search. Please try again.')
            elif answer.content == 'N' or answer.content == 'No' or answer.content == 'no' or answer.content == 'n':
                await ctx.send('Ok, Not cancelling your search.')


@bot.command()
@commands.max_concurrency(1,per=BucketType.user,wait=False)
async def addgame(ctx):
    """Add games to your personal profile."""
    x = Profiles.profiles(ctx.author.id)
    if x == None:
        await ctx.send('You dont have a profile to add games to. Please go set one up using `TM!setup`.')
    else:
        embed = discord.Embed(title='What game do you want to add to your profile?',description='You can see all supported games using the `TM!games` command.',color=0xCC071F)
        await ctx.send(embed = embed)
        def check(message):
            return message.content in supported and message.author == ctx.author and message.channel == ctx.message.channel
        try:
            answer = await bot.wait_for('message',timeout=30,check = check)
        except asyncio.TimeoutError:
            await ctx.send('Your taking too long...Cancelling')
        else:
            if answer.content == 'RL' or answer.content == 'rl':
                user = Profiles.rocket(ctx.author.id)
                if user != None:
                    await ctx.send('Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
                else:
                    embed = discord.Embed(title='What is your Rocket League rank?',description='The ranks are from lowest to highest:** bronze, silver, gold, platinum, diamond, gc, ssl**',color=0xCC071F)
                    embed.add_field(name='you can either choose your 1\'s 2\'s or 3\'s',
                                    value='Please also just put your rank not tier.', inline=False)
                    embed.add_field(
                        name='When putting in your rank please be truthful for this is to help you find a teammate around your rank.',
                        value='if put in a False rank you account can be reported. Then can be blacklisted from our services.')
                    embed.set_footer(text='When saying your rank please do it as exactly as you see above.')
                    await ctx.send(embed=embed)
                    rank = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'gc', 'ssl','Bronze','Silver','Gold','Platinum','Diamond','Gc','Ssl']
                    def check(message):
                        return message.content in rank and (message.channel == ctx.channel) and (message.author == ctx.author)
                    try:
                        answer = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        answer = answer.content.lower()
                        RL.insert_one({'user':ctx.author.id,'rank':f'{answer}'})
                        embed = discord.Embed(title='Succesfully added Rocket League to your profile',color=0xCC071F)
                        await ctx.send(embed= embed)
                        return
            elif answer.content == 'Roblox' or answer.content == 'roblox':
                x = rbx.find_one({'user':ctx.author.id})
                if x != None:
                    await ctx.send(
                        'Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
                else:
                    embed = discord.Embed(title='What is your Roblox username?', color=0xCC071F)
                    await ctx.send(embed=embed)
                    def check(message):
                        return (message.channel == ctx.channel) and (message.author == ctx.author)
                    try:
                        answer = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        await ctx.send('Successfully added to your profile.')
                        rbx.insert_one({'user':ctx.author.id,'name':f'{answer.content}'})
                        return
            elif answer.content == 'mc' or answer.content == 'MC' or answer.content == 'Mc':
                x = MC.find_one({'user':ctx.author.id})
                if x != None:
                    await ctx.send('Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
                else:
                    embed = discord.Embed(title='Do you play Minecraft Java or Bedrock?', color=0xCC071F)
                    await ctx.send(embed=embed)
                    platform = ['Java', 'java', 'Bedrock', 'bedrock']

                    def check(message):
                        return (message.content in platform) and (message.channel == ctx.channel) and (
                                    message.author == ctx.author)

                    try:
                        platform = await bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send('You didnt respond... Cancelling setup.')
                    else:
                        platform = platform.content.lower()
                        if platform == 'java':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
                                                  description='Survival \n PVP: ex.Hypixel Network \n Modded: ex. FeedTheBeast minecraft modpacks',
                                                  color=0xCC071F)
                            embed.set_footer(
                                text='To change this you are going to have to delete and readd this to your profile')
                            await ctx.send(embed=embed)
                            gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp', 'Modded', 'modded']

                            def check(message):
                                return (message.content in gamemode) and (message.channel == ctx.channel) and (
                                            message.author == ctx.author)

                            try:
                                mode = await bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await ctx.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
                                await ctx.send(embed=embed)

                                def check(message):
                                    return (message.channel == ctx.channel) and (
                                            message.author == ctx.author)

                                try:
                                    IGN = await bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    if mode == 'pvp':
                                        embed = discord.Embed(
                                            title='What are your current stars. In Hypixel (the only current supported server)',
                                            description='Choose any pvp mod you want', color=0xCC071F)
                                        await ctx.send(embed=embed)

                                        def check(message):
                                            return (message.channel == ctx.channel) and (message.author == ctx.author)

                                        try:
                                            stars = await bot.wait_for('message', timeout=30, check=check)
                                        except asyncio.TimeoutError:
                                            await ctx.send('You didnt respond... Cancelling setup.')
                                        else:
                                            stars = int(stars.content)
                                            embed = discord.Embed(title='Succesfully set up your account',
                                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                                  color=0xCC071F)
                                            info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'pvp',
                                                    'IGN': f'{IGN}', 'stars': stars}
                                            MC.insert_one(info)
                                            await ctx.send(embed=embed)
                                    elif mode == 'survival':
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                                              color=0xCC071F)

                                        info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'survival',
                                                'IGN': f'{IGN}'}
                                        MC.insert_one(info)
                                        await ctx.send(embed=embed)


                                    elif mode == 'modded':
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                                              color=0xCC071F)

                                        info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'modded',
                                                'IGN': f'{IGN}'}
                                        MC.insert_one(info)
                                        await ctx.send(embed=embed)
                                        return
                        elif platform == 'bedrock':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
                                                  description='Survival \n PVP: ex.Cubed Network',
                                                  color=0xCC071F)
                            embed.set_footer(
                                text='To change this you are going to have to delete and readd this to your profile')
                            await ctx.send(embed=embed)
                            gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp']

                            def check(message):
                                return (message.content in gamemode) and (message.channel == ctx.channel) and (
                                        message.author == ctx.author)

                            try:
                                mode = await bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await ctx.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
                                await ctx.send(embed=embed)

                                def check(message):
                                    return (message.channel == ctx.channel) and (
                                            message.author == ctx.author)

                                try:
                                    IGN = await bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    embed = discord.Embed(title='Succesfully set up your account',
                                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                                          color=0xCC071F)
                                    MC.insert_one({'user': ctx.author.id, 'platform': 'bedrock', 'mode': f'{mode}',
                                                   'IGN': f'{IGN}'})
                                    await ctx.send(embed=embed)
                                    return
            elif answer.content == 'Val' or answer.content == 'val':
                embed = discord.Embed(title='What is your Valorant rank?',
                                      description='The ranks are from lowest to highest:**bronze, iron, silver, gold, platinum, diamond, immortal, radiant**',
                                      color=0xCC071F)
                embed.add_field(name='Please be Truthful when inserting your rank.',
                                value='If found and reported inserting a incorrect rank you can and will be blacklisted from our services.')
                await ctx.send(embed=embed)
                rank = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'immortal', 'radiant', 'Iron',
                        'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Immortal', 'Radiant']

                def check(message):
                    return message.content in rank and message.author == ctx.author and message.channel == ctx.channel

                try:
                    rank = await bot.wait_for('message', timeout=45, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Error: You didnt respond in time... Cancelling setup.')
                else:
                    rank = rank.content.lower()
                    embed = discord.Embed(title='Succesfully set up your account',
                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                          color=0xCC071F)
                    val.insert_one({'user': ctx.author.id, 'rank': f'{rank}'})
                    await ctx.send(embed=embed)
                    return

            elif answer.content == 'Fortnite' or answer.content == 'fortnite':
                embed = discord.Embed(title='What League are you currently in?',
                                      description='The leagues are from lowest to highest:**Open, Contender, Champion**',
                                      color=0xCC071F)
                await ctx.send(embed=embed)
                rank = ['open', 'Open', 'Contender', 'contender', 'Champion', 'champion']

                def check(message):
                    return message.content in rank and message.channel == ctx.channel and message.author == ctx.author

                try:
                    rank = await bot.wait_for('message', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Error: You didnt respond in time... Cancelling setup.')
                else:
                    rank = rank.content.lower()
                    embed = discord.Embed(title='Succesfully set up your account',
                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                          color=0xCC071F)
                    fort.insert_one({'user': ctx.author.id, 'rank': f'{rank}'})
                    await ctx.send(embed=embed)






@bot.command(aliases =['Rgame'])
async def removegame(ctx):
    """Remove games from your personal profile."""
    embed = discord.Embed(title='What game do you want to remove from your profile?',color=0xCC071F)
    await ctx.send(embed=embed)
    abcd = ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'n', 'N']

    def check(message):
        return message.content in supported and message.author == ctx.author and message.channel == ctx.message.channel
    try:
        answer = await bot.wait_for('message', timeout=30, check=check)
    except asyncio.TimeoutError:
        await ctx.send('You took to long... cancelling')
    else:
        if answer.content == 'RL' or answer.content == 'rl':
            embed = discord.Embed(title='Are you sure you want to delete Rocket League from your profile?',color=0xCC071F)
            await ctx.send(embed = embed)
            def check(message):
                return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel
            try:
                gotti = await bot.wait_for('message',timeout=30,check = check)
            except:
                await ctx.send('You took to long... cancelling')
            else:
                if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
                    try:
                        RL.delete_one({"user": ctx.author.id})
                        await ctx.send('succesfully deleted')
                    except:
                        await ctx.send('Having trouble deleting the game. Please try again.')
                elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
                    await ctx.send('Ok, Not deleting Rocket League')
        elif answer.content == 'Roblox' or answer.content == 'roblox':
            embed = discord.Embed(title='Are you sure you want to delete Roblox from your profile?',
                                  color=0xCC071F)
            await ctx.send(embed=embed)
            def check(message):
                return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel
            try:
                gotti = await bot.wait_for('message', timeout=30, check=check)
            except:
                await ctx.send('You took to long... cancelling')
            else:
                if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
                    try:
                        rbx.delete_one({"user": ctx.author.id})
                        await ctx.send('succesfully deleted')
                    except:
                        await ctx.send('Having trouble deleting the game. Please try again.')
                elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
                    await ctx.send('Ok, Not deleting Roblox')
        elif answer.content == 'MC' or answer.content == 'mc' or answer.content == 'Mc':
            embed = discord.Embed(title='Are you sure you want to delete Minecraft from your profile?',
                                  color=0xCC071F)
            await ctx.send(embed=embed)

            def check(message):
                return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel

            try:
                gotti = await bot.wait_for('message', timeout=30, check=check)
            except:
                await ctx.send('You took to long... cancelling')
            else:
                if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
                    try:
                        MC.delete_one({"user": ctx.author.id})
                        await ctx.send('succesfully deleted')
                    except:
                        await ctx.send('Having trouble deleting the game. Please try again.')
                elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
                    await ctx.send('Ok, Not deleting Roblox')
        elif answer.content == 'Val' or answer.content == 'val':
            embed = discord.Embed(title='Are you sure you want to delete Valorant from your profile?',
                                  color=0xCC071F)
            await ctx.send(embed=embed)

            def check(message):
                return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel

            try:
                gotti = await bot.wait_for('message', timeout=30, check=check)
            except:
                await ctx.send('You took to long... cancelling')
            else:
                if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
                    try:
                        val.delete_one({"user": ctx.author.id})
                        await ctx.send('succesfully deleted')
                    except:
                        await ctx.send('Having trouble deleting the game. Please try again.')
                elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
                    await ctx.send('Ok, Not deleting Valorant')
        elif answer.content == 'Fortnite' or answer.content == 'fortnite':
            embed = discord.Embed(title='Are you sure you want to delete Fortnite from your profile?',
                                  color=0xCC071F)
            await ctx.send(embed=embed)

            def check(message):
                return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel

            try:
                gotti = await bot.wait_for('message', timeout=30, check=check)
            except:
                await ctx.send('You took to long... cancelling')
            else:
                if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
                    try:
                        fort.delete_one({"user": ctx.author.id})
                        await ctx.send('succesfully deleted')
                    except:
                        await ctx.send('Having trouble deleting the game. Please try again.')
                elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
                    await ctx.send('Ok, Not deleting Valorant')

@bot.command()
async def suggest(ctx):
    """Suggest features and or games for the bot"""
    embed = discord.Embed(title='Thanks for making a suggestion.',description='Whatever your next message is will be send as a suggestion. Please try to be a through as you can.',color=0xCC071F)
    await ctx.send(embed=embed)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.message.channel
    try:
        x = await bot.wait_for('message',timeout=600,check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title='You had 10 minutes to submit your suggestion.',description='If that isnt enought time just join our support server to submit your suggestion, which you can find [here](https://discord.gg/5XAubY2v3N)',color=0xCC071F)
        await ctx.send(embed = embed)
    else:
        embed= discord.Embed(title='Thank you for submitting a suggestion.',description='The devs will be sure to look at it, and maybe consider adding it as a feature',color=0xCC071F)
        await ctx.send(embed=embed)
        embed= discord.Embed(title=f'Suggestion from {ctx.author}',description=f'{x.content}',color=0xCC071F)
        channel = bot.get_channel(822858852143464558)
        await channel.send(embed = embed)

@bot.command()
async def report(ctx):
    """report users."""
    embed = discord.Embed(title='Thank you for using our report feature to try and help keep our community troll-free',description='Now when submitting your report please include all of the following... Who are you reporting. Why are you reporting(include name and discrim or just user id your choice). and any sort of evidence.(pictures are accepted)',color=0xCC071F)
    await ctx.send(embed = embed)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.message.channel
    try:
        x = await bot.wait_for('message',timeout=600,check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title='You had 10 minutes to submit your report.',description='If that isnt enought time just join our support server to report the user which you can find [here](https://discord.gg/5XAubY2v3N)',color=0xCC071F)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title='Thank you for submitting a report.',description='Our Moderators will take a look at it soon.',color=0xCC071F)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=f'New report Submitted by {ctx.author}',description=f'{x.content}',color=0xCC071F)
        if x.attachments:
            embed.set_image(url=x.attachments[0].url)
        channel = bot.get_channel(822858888578990090)
        await channel.send(embed = embed)

@bot.command(hidden=True)
async def getid(ctx,user:discord.User):
    if user != None:
        await ctx.send('Found')
        await ctx.send(user.id)
    else:
        await ctx.send('Couldnt find user...')

@bot.command(hidden=True,aliases = ['BL'])
async def blacklist(ctx,func,user:discord.User,*,reason=None):
    if ctx.author.id == 705992469426339841:
        if func == 'add' or func =='Add':
            await ctx.send(f'Added {user}')
            BL.insert_one({'user': user.id, 'reason': f'{reason}'})
        elif func == 'remove' or func =='Delete' or 'func' == 'delete' or func == 'Del':
            BL.delete_one({'user':user.id})
            await ctx.send(f'Deleted {user}')
        elif func =='Find' or func == 'find':
            x = BL.find_one({'user':user.id})
            await ctx.send(f'Blacklist for {user}: {x.get("reason")}')
    else:
        return

@blacklist.error
async def bl_error(ctx,error):
    await ctx.send(error)

@bot.command(hidden=True)
async def admindelete(ctx,user:discord.User):
    if ctx.author.id == 705992469426339841:
        user = user.id
        Profiles.deletion(user)
        await ctx.send('Deleted User\'s profile successfully')

@tasks.loop(minutes=1)
async def update():
    await bot.wait_until_ready()
    x = match.find()
    for info in x:
        x = dict(info)
        time = x.get('time')
        user = x.get('user')
        time = time + 1
        match.update_one({"user":user},{"$set": {"time":time}})
        if time >= 60:
            embed = discord.Embed(title='It has been an hour and no one has been matched with you.',description='You could either do the following: Requeue using `TM!search` or just wait for a little bit of time for some other users who are the same rank as you to queue aswell: sorry for the inconvience',color=0xCC071F)
            embed.set_footer(text='Thank you for using our services.')
            match.delete_one({"user":user})
            user = int(user)
            person = bot.get_user(user)
            await person.send(embed = embed)
        else:
            return

@bot.command(aliases=['deleteprofile','DP','dprofile'])
@commands.max_concurrency(1,per=BucketType.user,wait=False)
async def delprofile(ctx):
    """Delete your profile."""
    embed=discord.Embed(title='Are you sure you want to delete your profile.',description='If you say yes you lose all the games set up with your account and you will have to reset it up.',color=0xCC071F)
    await ctx.send(embed = embed)
    abcd = ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'n', 'N']
    def check(message):
        return message.content in abcd and message.author == ctx.author and message.channel == ctx.message.channel
    try:
        gotti = await bot.wait_for('message',timeout=30,check=check)
    except asyncio.TimeoutError:
        await ctx.send("You took to long... Cancelling deletion.")
    else:
        if gotti.content == 'yes' or gotti.content == 'Yes' or gotti.content == 'y' or gotti.content == 'Y':
            Profiles.deletion(ctx.author.id)
            await ctx.send('succesfully deleted')
        elif gotti.content == 'N' or gotti.content == 'No' or gotti.content == 'no' or gotti.content == 'n':
            await ctx.send('Ok, Not deleting Your profile.')

@bot.command(aliases=['account'])
async def profile(ctx,user:discord.User = None):
    """Check out your profile"""
    if user == None:
        user = ctx.author
    x = Profiles.profiles(user.id)
    if x == None:
        await ctx.send('Error: user doesnt have a profile. Set up one using the `TM!setup` command')
    else:
        embed = discord.Embed(title=f'Profile for {user}',description=f'Region: {x.get("region")} ',color=0xCC071F)
        x = Profiles.rocket(user.id)
        if x != None:
            embed.add_field(name='Rocket League',value=f'Rank: {x.get("rank")}',inline=False)
        x = None
        x = rbx.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Roblox', value=f'Username: {x.get("name")}', inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        x = MC.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Minecraft',value=f'IGN: {x.get("IGN")} \n Platform: {x.get("platform")}', inline=False)
        x = val.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Valorant',value=f'rank: {x.get("rank")}',inline=False)
        x = fort.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Fortnite',value=f'rank: {x.get("rank")}',inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title='Invite TM to your server today!',description='[click here](https://discord.com/api/oauth2/authorize?client_id=822637954769879100&permissions=379905&scope=bot)',color=0xCC071F)
    await ctx.send(embed = embed)

@bot.command()
async def tutorial(ctx):
    embed = discord.Embed(title='Do you find TM a bit to hard to understand?',description='Then have a look at a very simple tutorial on how to setup your profile. You can find that video [here](https://youtu.be/dOZHazMxcag)',color=0xCC071F)
    await ctx.send(embed = embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Tilted Matchmaking Help Section',description='All of TM\'s commands. If you need any assistance join our help server which you can find [here](https://discord.gg/rKWxkrCkUQ)',color=0xCC071F)
    embed.add_field(name='Profile Commands',value='`TM!setup`\n`TM!profile`\n`TM!delprofile` \n`TM!addgame`\n`TM!removegame`',inline=False)
    embed.add_field(name='Matchmaking Commands',value='`TM!search` \n`TM!cancel `',inline= False)
    embed.add_field(name='Utilities',value='`TM!suggest`\n`TM!panel` \n`TM!report`\n`TM!games` \n`TM!invite`\n`TM!tutorial`',inline=False)
    embed.add_field(name='\u200b',value='Need help with TM but dont want to join the support server? check out the tutorial video thats on youtube. You can find it [here](https://youtu.be/dOZHazMxcag)')
    await ctx.send(embed = embed)

@bot.command()
async def vote(ctx):
    embed = discord.Embed(title='Vote for us on top.gg!',description='You can find the link [here.](https://top.gg/bot/822637954769879100/vote)',color=0xCC071F)
    await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def panel(ctx,channel:discord.TextChannel = None):
    if channel == None:
        channel = ctx.channel
    first = await ctx.send(f"Sending A setup panel to <#{channel.id}>")
    embed = discord.Embed(title='Account Setup',description='React to this embed to setup your account.',color=0xCC071F)
    embed.set_footer(text='If you react to this embed you will be sent a DM by the bot to set up your account.')
    x = await channel.send(embed = embed)
    emoji = bot.get_emoji(838234937743245382)
    await x.add_reaction(emoji)
    await asyncio.sleep(3)
    await ctx.message.delete()
    await first.delete()


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.id == 822637954769879100:
        return
    else:
        if payload.emoji.id == 838234937743245382:
            x = bot.get_channel(payload.channel_id)
            y = await x.fetch_message(payload.message_id)

            if y.author.id == 822637954769879100:
                user = bot.get_user(payload.member.id)
                emoji = bot.get_emoji(838234937743245382)
                try:
                    await y.remove_reaction(emoji,user)
                except:
                    pass
                z = profiling.find_one({'user':user.id})
                if z == None:
                    await Reaction.setup(payload.member.id)
                else:
                    await user.send('Error you already have your profile setup. If you wish to add more games try the `TM!addgame` command.')


update.start()
bot.run('ODIyNjM3OTU0NzY5ODc5MTAw.YFVLTA.ynYbEzL4witqVPnDOZPpbYLRUgE')