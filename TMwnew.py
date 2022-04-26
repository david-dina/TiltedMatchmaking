#Same as TM.py but integrated with py-cord and the new slash commands and other features
import discord
from discord.ext import commands,tasks
from discord.ext.commands import BucketType
from discord.ui import Button,View
from discord.commands import Option
import pymongo
import asyncio
import datetime
from TMClass import UserProfiles, Profiles
from TMclassv2 import Reaction


#chen email
client = pymongo.MongoClient("mongodb+srv://starlord:Adeoluwa.05@playerinfo.t5g9l.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.games
RL = db.RocketLeague
dbv2 = client.Match
match = dbv2.Maker
dbv3 = client.Profile
profiling = dbv3.User
dbv4 = client.black
BL = dbv4.list
rbx = db.Roblox
#MC = db.MC
val = db.valorant
fort = db.fortnite
#main email
client = pymongo.MongoClient('mongodb+srv://starlord:Adeoluwa.05@cluster0.52enc.mongodb.net/myFirstDatabase&retryWrites=true&w=majority?ssl=true&ssl_cert_reqs=CERT_NONE')
db = client.server
connected = db.matches
#minecraft later
supported_games = ["Rocket League","Roblox","Valorant","Fortnite"]
intents = discord.Intents.all()


bot = commands.Bot(command_prefix='TM!',intents=intents,status=discord.Status.dnd,activity=discord.Activity(name='Coming back to you soon!',type=discord.ActivityType.watching))
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
    user = bot.get_user(member.id)
    if user.dm_channel:
        return
    else:
        emoji = bot.get_emoji(838234937743245382)
        embed = discord.Embed(title=f"{ctx.author.name}",
                              description=f"It looks like {ctx.guild} is your first guild using {emoji} Tilted Matchmaking",
                              color=0xCC071F)
        embed.set_author(icon_url=bot.user.avatar.url,
                         name="Tilted Matchmaking notification", url='https://discord.gg/rKWxkrCkUQ')
        embed.add_field(name='As a new server member you can claim these perks',
                        value=" :art: Be able to create your own customizable profile :art:  \n :hammer: Add,Edit, and remove games from your gaming profile. :hammer: \n :people_holding_hands: Match with users discord-Wide to play your favorite games with a few clicks. :people_holding_hands:")
        embed.set_footer(text="Tilted Matchmaking. Find The Teammate of Your Dreams.")
        await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.BotMissingPermissions):
        await ctx.respond('Error: I am missing the permissions to operate properly. Please fix my permissions.')
    elif isinstance(error,commands.NoPrivateMessage):
        embed = discord.Embed(title='While running, an error occured.', description='This command doesnt work in dm\'s please try it in a guild.', color=0xCC071F)
        await ctx.respond(embed = embed)
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
#Remember to remove below
supported = ['yes']
region = ['North America', 'Europe', 'South America','Asia','Australia']
@bot.slash_command(guild_ids=[877460893439512627])
async def setup(ctx,game:Option(str,"The game to setup with",required=True,choices=supported_games),region:Option(str,"Your closest location. For games that rely on ping.",required=True,choices=region)):
    """Set up your personal profile using this command"""
    await ctx.defer()
    #remember to remove below
    channel = bot.get_channel(12345)
    x = Profiles.profiles(ctx.author.id)
    #embed = discord.Embed(title=f'New Profile Setup by {ctx.author}',color=0xCC071F)
    #if (ctx.message.guild == None):
        #embed.add_field(name='Command ran in DMS',value='\u200b',inline=False)
    #else:
        #embed.add_field(name = f'Guild:',value=f'{ctx.guild}')
    #channel = bot.get_channel(826331977257844746)
    #await channel.send(embed = embed)
    perp = Profiles.blacklisted(ctx.author.id)
    if perp != None:
        embed = discord.Embed(title=f'Error: You have been blacklisted from our services for: {perp.get("reason")} ',description='If You wish to appeal your ban than please join our support server [here](https://discord.gg/5XAubY2v3N) and open a ticket.',color=0xCC071F)
        await ctx.respond(embed = embed)
    else:
        if x != None:
            await ctx.respond('Error: You have already set up a profile. To add games to your profile use the addgame command')
            return
        else:
            if game == 'Rocket League':
                embed = discord.Embed(title='What is your Rocket League rank?',color=0xCC071F)
                embed.add_field(name='you can either choose your 1\'s 2\'s or 3\'s',value='\u200b',inline=False)
                embed.add_field(name='When putting in your rank please be **TRUTHFUL** for this is to help you find a teammate around your rank.',value='if put in a False rank you account can be reported. Then can be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Rocket League rank?',color=0xCC071F)
                async def button_callback(interaction:discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2,view=None)
                            Profile = {'user': ctx.author.id, 'region': f'{region}'}
                            profiling.insert_one(Profile)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            rl = {'user': ctx.author.id, 'rank': f'{rank}'}
                            RL.insert_one(rl)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled",embed=None, view=None)
                button1 = Button(label="Bronze",style=discord.ButtonStyle.primary,custom_id='Bronze')
                button2 = Button(label="Silver", style=discord.ButtonStyle.primary, custom_id='Silver')
                button3 = Button(label="Gold", style=discord.ButtonStyle.primary, custom_id='Gold')
                button4 = Button(label="Platinum", style=discord.ButtonStyle.primary, custom_id='Platinum')
                button8 = Button(label="Diamond", style=discord.ButtonStyle.primary, custom_id='Diamond')
                button5 = Button(label="Champion", style=discord.ButtonStyle.primary, custom_id='Champion')
                button6 = Button(label="Grand Champ", style=discord.ButtonStyle.primary, custom_id='GC')
                button7 = Button(label="SSL", style=discord.ButtonStyle.primary, custom_id='SSL')
                cancel = Button(label="Cancel",style=discord.ButtonStyle.danger,custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                button4.callback = button_callback
                button5.callback = button_callback
                button6.callback = button_callback
                button7.callback = button_callback
                button8.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                view.add_item(button8)
                view.add_item(button5)
                view.add_item(button6)
                view.add_item(button7)
                view.add_item(cancel)
                await ctx.respond(embed=embed,view=view)
            elif game =='Roblox':
                embed = discord.Embed(title='What is your Roblox username?',color=0xCC071F)
                await ctx.respond(embed = embed)
                def check(message):
                    return (message.channel == ctx.channel) and (message.author == ctx.author)
                try:
                    answer = await bot.wait_for('message', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.respond('You didnt respond... Cancelling setup.')
                else:
                    Profile = {'user': ctx.author.id, 'region': f'{region}'}
                    profiling.insert_one(Profile)
                    embed = discord.Embed(title='Succesfully set up your account',
                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                          color=0xCC071F)
                    await ctx.respond(embed = embed)
                    rbx.insert_one({'user':ctx.author.id,'name':f'{answer.content}'})
    #figure out how to find multiple options with MC and take options and take and respond. Try without message content input
            # elif game == 'Minecraft':
            #     embed = discord.Embed(title='Do you play Minecraft Java or Bedrock?', color=0xCC071F)
            #     await ctx.respond(embed=embed)
            #     platform = ['Java','java','Bedrock','bedrock']
            #     def check(message):
            #         return (message.content in platform) and (message.channel == ctx.channel) and (message.author == ctx.author)
            #     try:
            #         platform = await bot.wait_for('message', timeout=30, check=check)
            #     except asyncio.TimeoutError:
            #         await ctx.respond('You didnt respond... Cancelling setup.')
            #     else:
            #         platform = platform.content.lower()
            #         if platform == 'java':
            #             embed = discord.Embed(title='What gamemode do you wish to find a partner for.',description='Survival \n PVP: ex.Hypixel Network \n Modded: ex. FeedTheBeast minecraft modpacks',color=0xCC071F)
            #             embed.set_footer(text='To change this you are going to have to delete and readd this to your profile')
            #             await ctx.respond(embed = embed)
            #             gamemode = ['Survival','survival','PVP','pvp','Pvp','Modded','modded']
            #             def check(message):
            #                 return (message.content in gamemode) and (message.channel == ctx.channel) and (message.author == ctx.author)
            #             try:
            #                 mode = await bot.wait_for('message', timeout=30, check=check)
            #             except asyncio.TimeoutError:
            #                 await ctx.respond('You didnt respond... Cancelling setup.')
            #             else:
            #                 embed = discord.Embed(title='What is your IGN?',color=0xCC071F)
            #                 await ctx.respond(embed = embed)
            #                 def check(message):
            #                     return(message.channel == ctx.channel) and (
            #                                 message.author == ctx.author)
            #                 try:
            #                     IGN = await bot.wait_for('message', timeout=30, check=check)
            #                 except asyncio.TimeoutError:
            #                     await ctx.respond('You didnt respond... Cancelling setup.')
            #                 else:
            #                     IGN = IGN.content.lower()
            #                     mode = mode.content.lower()
            #                     if mode =='pvp':
            #                         embed = discord.Embed(title='What are your current stars. In Hypixel (the only current supported server)',description='Choose any pvp mod you want',color=0xCC071F)
            #                         await ctx.respond(embed = embed)
            #                         def check(message):
            #                             return (message.channel == ctx.channel) and (message.author == ctx.author)
            #                         try:
            #                             stars = await bot.wait_for('message',timeout=30,check=check)
            #                         except asyncio.TimeoutError:
            #                             await ctx.respond('You didnt respond... Cancelling setup.')
            #                         else:
            #                             Profile = {'user': ctx.author.id, 'region': f'{region}'}
            #                             profiling.insert_one(Profile)
            #                             stars = int(stars.content)
            #                             embed = discord.Embed(title='Succesfully set up your account',
            #                                                   description='If you want to find a partner right away then try my `TM!search` command.',
            #                                                   color=0xCC071F)
            #                             info = {'user':ctx.author.id,'platform':f'{platform}','mode':'pvp','IGN':f'{IGN}','stars':stars}
            #                             MC.insert_one(info)
            #                             await ctx.respond(embed = embed)
            #                     elif mode == 'survival':
            #                         Profile = {'user': ctx.author.id, 'region': f'{region}'}
            #                         profiling.insert_one(Profile)
            #                         embed = discord.Embed(title='Succesfully set up your account',
            #                                                   description='If you want to find a partner right away then try my `TM!search` command.',
            #                                                   color=0xCC071F)
            #                         info = {'user':ctx.author.id,'platform':f'{platform}','mode':'survival','IGN':f'{IGN}'}
            #                         MC.insert_one(info)
            #                         await ctx.respond(embed = embed)
            #
            #                     elif mode == 'modded':
            #                         Profile = {'user': ctx.author.id, 'region': f'{region}'}
            #                         profiling.insert_one(Profile)
            #                         embed = discord.Embed(title='Succesfully set up your account',
            #                                               description='If you want to find a partner right away then try my `TM!search` command.',
            #                                               color=0xCC071F)
            #
            #                         info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'modded',
            #                                 'IGN': f'{IGN}'}
            #                         MC.insert_one(info)
            #                         await ctx.respond(embed=embed)
            #         elif platform == 'bedrock':
            #             embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
            #                                   description='Survival \n PVP: ex.Cubed Network',
            #                                   color=0xCC071F)
            #             embed.set_footer(
            #                 text='To change this you are going to have to delete and read this to your profile')
            #             await ctx.respond(embed=embed)
            #             gamemode = ['Survival', 'survival', 'PVP', 'pvp','Pvp']
            #             def check(message):
            #                 return (message.content in gamemode) and (message.channel == ctx.channel) and (
            #                             message.author == ctx.author)
            #             try:
            #                 mode = await bot.wait_for('message', timeout=30, check=check)
            #             except asyncio.TimeoutError:
            #                 await ctx.respond('You didnt respond... Cancelling setup.')
            #             else:
            #                 embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
            #                 await ctx.respond(embed=embed)
            #
            #                 def check(message):
            #                     return (message.channel == ctx.channel) and (
            #                             message.author == ctx.author)
            #
            #                 try:
            #                     IGN = await bot.wait_for('message', timeout=30, check=check)
            #                 except asyncio.TimeoutError:
            #                     await ctx.respond('You didnt respond... Cancelling setup.')
            #                 else:
            #                     IGN = IGN.content.lower()
            #                     mode = mode.content.lower()
            #                     Profile = {'user': ctx.author.id, 'region': f'{region}'}
            #                     profiling.insert_one(Profile)
            #                     embed = discord.Embed(title='Succesfully set up your account',
            #                                           description='If you want to find a partner right away then try my `TM!search` command.',
            #                                           color=0xCC071F)
            #                     MC.insert_one({'user':ctx.author.id,'platform':'bedrock','mode':f'{mode}','IGN':f'{IGN}'})
            #                     await ctx.respond(embed = embed)
            elif game == 'Valorant':
                embed = discord.Embed(title='What is your Valorant rank?',description='The ranks are from lowest to highest:**bronze, iron, silver, gold, platinum, diamond, immortal, radiant**',color=0xCC071F)
                embed.add_field(name='Please be **TRUTHFUL** when inserting your rank.',value='If found and reported inserting a incorrect rank you can and will be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Valorant rank?', color=0xCC071F)
                async def button_callback(interaction: discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2, view=None)
                            Profile = {'user': ctx.author.id, 'region': f'{region}'}
                            profiling.insert_one(Profile)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            VAL = {'user': ctx.author.id, 'rank': f'{rank}'}
                            val.insert_one(VAL)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled", embed=None, view=None)

                button1 = Button(label="Iron", style=discord.ButtonStyle.primary, custom_id='Iron')
                button2 = Button(label="Bronze", style=discord.ButtonStyle.primary, custom_id='Bronze')
                button3 = Button(label="Silver", style=discord.ButtonStyle.primary, custom_id='Silver')
                button4 = Button(label="Gold", style=discord.ButtonStyle.primary, custom_id='Gold')
                button8 = Button(label="Platinum", style=discord.ButtonStyle.primary, custom_id='Platinum')
                button5 = Button(label="Diamond", style=discord.ButtonStyle.primary, custom_id='Diamond')
                button6 = Button(label="Immortal", style=discord.ButtonStyle.primary, custom_id='Immortal')
                button7 = Button(label="Radiant", style=discord.ButtonStyle.primary, custom_id='Radiant')
                cancel = Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                button4.callback = button_callback
                button5.callback = button_callback
                button6.callback = button_callback
                button7.callback = button_callback
                button8.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                view.add_item(button8)
                view.add_item(button5)
                view.add_item(button6)
                view.add_item(button7)
                view.add_item(cancel)
                await ctx.respond(embed=embed,view=view)
            elif game == 'Fortnite':
                embed = discord.Embed(title='What league are you currently in?',description='The leagues are from lowest to highest:**Open, Contender, Champion**',color=0xCC071F)
                embed.add_field(name='Please be **TRUTHFUL** when inserting your league.',value='If found and reported inserting a incorrect league you can and will be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Fortnite league?', color=0xCC071F)
                #buttons for this too
                async def button_callback(interaction: discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2, view=None)
                            Profile = {'user': ctx.author.id, 'region': f'{region}'}
                            profiling.insert_one(Profile)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            forts = {'user': ctx.author.id, 'rank': f'{rank}'}
                            fort.insert_one(forts)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled", embed=None, view=None)
                button1 = Button(label="Open", style=discord.ButtonStyle.primary, custom_id='Open')
                button2 = Button(label="Contender", style=discord.ButtonStyle.primary, custom_id='Contender')
                button3 = Button(label="Champion", style=discord.ButtonStyle.primary, custom_id='Champion')
                cancel = Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(cancel)
                await ctx.respond(embed=embed, view=view)


@setup.error
async def setup_error(ctx,error):
    if isinstance(error,commands.MaxConcurrencyReached):
        await ctx.respond('Your already running this command.')


#@bot.command()
#async def games(ctx):
    #"""All of this bots supported games."""
    #embed = discord.Embed(title='All the currently supported games on our platform', color=0xCC071F)
    #embed.add_field(name='\u200b',value='Rocket League: RL \n Roblox \n Minecraft: MC\n Valorant: Val \n Fortnite')
    #embed.set_footer(text='If a game your play isnt on here and you want it to be added try the TM!suggest command')
    #await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[877460893439512627])
@commands.max_concurrency(1,per=BucketType.user,wait=False)
@commands.guild_only()
async def search(ctx,game:Option(str,"The game to search a partner for",required=True,choices=supported_games)):
    """Search for a teammate."""
    user = None
    looking = {'user':ctx.author.id}
    found = match.find_one(looking)
    if found != None:
        await ctx.respond(
            'Error: You already have a search running. If you are trying to cancel your search please do the `/cancel` command.')
    else:
        info = {'user': ctx.author.id}
        x = RL.find_one(info)
        z = profiling.find_one(info)
        if z == None:
            await ctx.respond('Error you didn\'t set up your profile. Please do `/setup` to do that.')
        else:
            if game == 'Rocket League':
                if x == None:
                    await ctx.respond('Error you dont have Rocket League added to your profile. Please do `/addgame` to do that.')
                    return
                embed = discord.Embed(title='Now Searching for teammates for the game: Rocket League',description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',color=0xCC071F)
                await ctx.respond(embed = embed)
                info = {'game':'RL','rank': f"{x.get('rank')}",'region':f"{z.get('region')}"}
                y = match.find(info)
                if y:
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


            elif game == 'Roblox':
                if rbx.find_one({'user':ctx.author.id}) == None:
                    await ctx.respond('Error: You havnt added this game to your profile. Please do that with `/addgame`.')
                else:
                    embed = discord.Embed(title='Now Searching for teammates for the game: Roblox',
                                          description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                          color=0xCC071F)
                    await ctx.respond(embed=embed)
                    info = {'game': 'RBX', 'region': f"{z.get('region')}"}
                    y = match.find(info)
                    if y:
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
            # elif game == 'Minecraft':
            #     if MC.find_one({'user':ctx.author.id}) == None:
            #         await ctx.respond('Error you have not setup this game in your profile. Please do so with `/addgame`.')
            #     else:
            #         embed = discord.Embed(title='Now Searching for teammates for the game: Minecraft',
            #                           description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
            #                           color=0xCC071F)
            #         await ctx.respond(embed = embed)
            #         yz = MC.find_one({'user':ctx.author.id})
            #         if yz.get('stars') != None:
            #             star = Profiles.MC_ranks(yz.get('stars'))
            #             info = {'game': 'MC', 'region': f"{z.get('region')}",
            #                     'rank': f'{star}',
            #                     'platform': f'{yz.get("platform")}'}
            #         else:
            #             info = {'game': 'MC', 'region': f"{z.get('region')}",
            #                     'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}'}
            #         y = match.find(info)
            #         if y:
            #             y = dict(y)
            #         for info in y:
            #             id = info.get('user')
            #             user = bot.get_user(id)
            #         if not y:
            #             if yz.get('stars') != None:
            #                 star = Profiles.MC_ranks(yz.get('stars'))
            #                 info = {'user': ctx.author.id,'game': 'MC', 'region': f"{z.get('region')}", 'rank': f'{star}',
            #                         'platform': f'{yz.get("platform")}','time':0}
            #             else:
            #                 info = {'user': ctx.author.id,'game': 'MC', 'region': f"{z.get('region')}",
            #                         'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}','time':0}
            #             match.insert_one(info)
            #         if user == None:
            #             return
            #         else:
            #             mel = await UserProfiles.teammateyes(ctx, user)
            #             if mel == False:
            #                 embed = discord.Embed(title='Alright. Removing you from the Queue.',
            #                                       description='You can requeue anytime just make sure that you will be able to accept the invitation next time.',
            #                                       color=0xCC071F)
            #                 await user.send(embed=embed)
            #                 match.delete_one({"user": user.id})
            #                 if yz.get('stars') != None:
            #                     star = Profiles.MC_ranks(yz.get('stars'))
            #                     info = {'user': ctx.author.id, 'game': 'MC', 'region': f"{z.get('region')}",
            #                             'rank': f'{star}',
            #                             'platform': f'{yz.get("platform")}'}
            #                 else:
            #                     info = {'user': ctx.author.id, 'game': 'MC', 'region': f"{z.get('region')}",
            #                             'platform': f'{yz.get("platform")}', 'mode': f'{yz.get("mode")}','time':0}
            #                 match.insert_one(info)
            elif game == 'Valorant':
                if val.find_one({'user':ctx.author.id}) == None:
                    await ctx.respond('Error you have not setup this game in your profile. Please do so with `/addgame`.')
                else:
                    embed = discord.Embed(title='Now Searching for teammates for the game: Valorant',
                                          description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                          color=0xCC071F)
                    await ctx.respond(embed=embed)
                    x = val.find_one({'user':ctx.author.id})
                    info = {'game': 'Val', 'rank': f"{x.get('rank')}", 'region': f"{z.get('region')}"}
                    y = match.find(info)
                    if y:
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
            elif game == 'Fortnite':
                if fort.find_one({'user':ctx.author.id}) == None:
                    await ctx.respond('Error you have not setup this game in your profile. Please do so with `/addgame`.')
                else:
                    embed = discord.Embed(title='Now Searching for teammates for the game: Fortnite',
                                          description='This lasts an hour at max, after an hour with no teammate found you will be DM\'ed to try again.',
                                          color=0xCC071F)
                    await ctx.respond(embed=embed)
                    x = fort.find_one({'user':ctx.author.id})
                    info = {'game': 'Fort', 'rank': f"{x.get('rank')}", 'region': f"{z.get('region')}"}
                    y = match.find(info)
                    if y:
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
        await ctx.respond('Error: You already have a search running. If you are trying to cancel your search please do the `/cancel` command.')


@bot.slash_command(guild_ids=[877460893439512627])
async def cancel(ctx):
    """cancel your search"""
    x = match.find_one({"user": ctx.author.id})
    if x == None:
        await ctx.respond('You dont have a current running search to cancel.')
    else:
        embed = discord.Embed(title='Are you sure you want to cancel your search?',color=0xCC071F)
        async def button_callback(interaction:discord.Interaction):
            ans = interaction.data.get('custom_id')
            if ans != 'No':
                try:
                    match.delete_one({"user": ctx.author.id})
                    await interaction.response.edit_message(embed=None, view=None,content="Successfully removed from the queue.")
                except:
                    await interaction.response.edit_message(embed=None, view=None,content="Having trouble removing from queue. Please try again.")
            else:
                await interaction.response.edit_message(embed=None, view=None,content="Not removing from queue.")
        button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
        button2 = Button(label="No", style=discord.ButtonStyle.primary, custom_id='No')
        view = View()
        button1.callback = button_callback
        button2.callback = button_callback
        view.add_item(button1)
        view.add_item(button2)
        await ctx.respond(embed=embed,view=view)
@bot.slash_command(guild_ids=[877460893439512627])
async def addgame(ctx,game:Option(str,"The game to setup with",required=True,choices=supported_games)):
    #"Rocket League", "Roblox", "Minecraft", "Valorant", "Fortnite"
    """Add games to your personal profile."""
    x = Profiles.profiles(ctx.author.id)
    if x == None:
        await ctx.respond('You dont have a profile to add games to. Please go set one up using `TM!setup`.')
    else:
        await ctx.defer()
        if game == 'Rocket League':
            user = Profiles.rocket(ctx.author.id)
            if user != None:
                await ctx.respond('Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
            else:
                embed = discord.Embed(title='What is your Rocket League rank?', color=0xCC071F)
                embed.add_field(name='you can either choose your 1\'s 2\'s or 3\'s', value='\u200b', inline=False)
                embed.add_field(
                    name='When putting in your rank please be **TRUTHFUL** for this is to help you find a teammate around your rank.',
                    value='if put in a False rank you account can be reported. Then can be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Rocket League rank?', color=0xCC071F)
                async def button_callback(interaction: discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2, view=None)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            rl = {'user': ctx.author.id, 'rank': f'{rank}'}
                            RL.insert_one(rl)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled", embed=None, view=None)
                button1 = Button(label="Bronze", style=discord.ButtonStyle.primary, custom_id='Bronze')
                button2 = Button(label="Silver", style=discord.ButtonStyle.primary, custom_id='Silver')
                button3 = Button(label="Gold", style=discord.ButtonStyle.primary, custom_id='Gold')
                button4 = Button(label="Platinum", style=discord.ButtonStyle.primary, custom_id='Platinum')
                button8 = Button(label="Diamond", style=discord.ButtonStyle.primary, custom_id='Diamond')
                button5 = Button(label="Champion", style=discord.ButtonStyle.primary, custom_id='Champion')
                button6 = Button(label="Grand Champ", style=discord.ButtonStyle.primary, custom_id='GC')
                button7 = Button(label="SSL", style=discord.ButtonStyle.primary, custom_id='SSL')
                cancel = Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                button4.callback = button_callback
                button5.callback = button_callback
                button6.callback = button_callback
                button7.callback = button_callback
                button8.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                view.add_item(button8)
                view.add_item(button5)
                view.add_item(button6)
                view.add_item(button7)
                view.add_item(cancel)
                await ctx.respond(embed=embed, view=view)
        elif game == 'Roblox':
            x = rbx.find_one({'user':ctx.author.id})
            if x != None:
                await ctx.respond(
                    'Error. You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
            else:
                embed = discord.Embed(title='What is your Roblox username?', color=0xCC071F)
                await ctx.respond(embed=embed)
                def check(message):
                    return (message.channel == ctx.channel) and (message.author == ctx.author)
                try:
                    answer = await bot.wait_for('message', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.respond('You didnt respond... Cancelling setup.')
                else:
                    Profile = {'user': ctx.author.id, 'region': f'{region}'}
                    profiling.insert_one(Profile)
                    embed = discord.Embed(title='Succesfully set up your account',
                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                          color=0xCC071F)
                    await ctx.respond(embed=embed)
                    rbx.insert_one({'user': ctx.author.id, 'name': f'{answer.content}'})
        # elif game == 'Minecraft':
        #     x = MC.find_one({'user':ctx.author.id})
        #     if x != None:
        #         await ctx.respond('Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
        #     else:
        #         embed = discord.Embed(title='Do you play Minecraft Java or Bedrock?', color=0xCC071F)
        #         await ctx.respond(embed=embed)
        #         platform = ['Java', 'java', 'Bedrock', 'bedrock']
        #
        #         def check(message):
        #             return (message.content in platform) and (message.channel == ctx.channel) and (
        #                         message.author == ctx.author)
        #
        #         try:
        #             platform = await bot.wait_for('message', timeout=30, check=check)
        #         except asyncio.TimeoutError:
        #             await ctx.respond('You didnt respond... Cancelling setup.')
        #         else:
        #             platform = platform.content.lower()
        #             if platform == 'java':
        #                 embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
        #                                       description='Survival \n PVP: ex.Hypixel Network \n Modded: ex. FeedTheBeast minecraft modpacks',
        #                                       color=0xCC071F)
        #                 embed.set_footer(
        #                     text='To change this you are going to have to delete and readd this to your profile')
        #                 await ctx.respond(embed=embed)
        #                 gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp', 'Modded', 'modded']
        #
        #                 def check(message):
        #                     return (message.content in gamemode) and (message.channel == ctx.channel) and (
        #                                 message.author == ctx.author)
        #
        #                 try:
        #                     mode = await bot.wait_for('message', timeout=30, check=check)
        #                 except asyncio.TimeoutError:
        #                     await ctx.respond('You didnt respond... Cancelling setup.')
        #                 else:
        #                     embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
        #                     await ctx.respond(embed=embed)
        #
        #                     def check(message):
        #                         return (message.channel == ctx.channel) and (
        #                                 message.author == ctx.author)
        #
        #                     try:
        #                         IGN = await bot.wait_for('message', timeout=30, check=check)
        #                     except asyncio.TimeoutError:
        #                         await ctx.respond('You didnt respond... Cancelling setup.')
        #                     else:
        #                         IGN = IGN.content.lower()
        #                         mode = mode.content.lower()
        #                         if mode == 'pvp':
        #                             embed = discord.Embed(
        #                                 title='What are your current stars. In Hypixel (the only current supported server)',
        #                                 description='Choose any pvp mod you want', color=0xCC071F)
        #                             await ctx.respond(embed=embed)
        #
        #                             def check(message):
        #                                 return (message.channel == ctx.channel) and (message.author == ctx.author)
        #
        #                             try:
        #                                 stars = await bot.wait_for('message', timeout=30, check=check)
        #                             except asyncio.TimeoutError:
        #                                 await ctx.respond('You didnt respond... Cancelling setup.')
        #                             else:
        #                                 stars = int(stars.content)
        #                                 embed = discord.Embed(title='Succesfully set up your account',
        #                                                       description='If you want to find a partner right away then try my `TM!search` command.',
        #                                                       color=0xCC071F)
        #                                 info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'pvp',
        #                                         'IGN': f'{IGN}', 'stars': stars}
        #                                 MC.insert_one(info)
        #                                 await ctx.respond(embed=embed)
        #                         elif mode == 'survival':
        #                             embed = discord.Embed(title='Succesfully set up your account',
        #                                                   description='If you want to find a partner right away then try my `TM!search` command.',
        #                                                   color=0xCC071F)
        #
        #                             info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'survival',
        #                                     'IGN': f'{IGN}'}
        #                             MC.insert_one(info)
        #                             await ctx.respond(embed=embed)
        #
        #
        #                         elif mode == 'modded':
        #                             embed = discord.Embed(title='Succesfully set up your account',
        #                                                   description='If you want to find a partner right away then try my `TM!search` command.',
        #                                                   color=0xCC071F)
        #
        #                             info = {'user': ctx.author.id, 'platform': f'{platform}', 'mode': 'modded',
        #                                     'IGN': f'{IGN}'}
        #                             MC.insert_one(info)
        #                             await ctx.respond(embed=embed)
        #                             return
        #             elif platform == 'bedrock':
        #                 embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
        #                                       description='Survival \n PVP: ex.Cubed Network',
        #                                       color=0xCC071F)
        #                 embed.set_footer(
        #                     text='To change this you are going to have to delete and readd this to your profile')
        #                 await ctx.respond(embed=embed)
        #                 gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp']
        #
        #                 def check(message):
        #                     return (message.content in gamemode) and (message.channel == ctx.channel) and (
        #                             message.author == ctx.author)
        #
        #                 try:
        #                     mode = await bot.wait_for('message', timeout=30, check=check)
        #                 except asyncio.TimeoutError:
        #                     await ctx.respond('You didnt respond... Cancelling setup.')
        #                 else:
        #                     embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
        #                     await ctx.respond(embed=embed)
        #
        #                     def check(message):
        #                         return (message.channel == ctx.channel) and (
        #                                 message.author == ctx.author)
        #
        #                     try:
        #                         IGN = await bot.wait_for('message', timeout=30, check=check)
        #                     except asyncio.TimeoutError:
        #                         await ctx.respond('You didnt respond... Cancelling setup.')
        #                     else:
        #                         IGN = IGN.content.lower()
        #                         mode = mode.content.lower()
        #                         embed = discord.Embed(title='Succesfully set up your account',
        #                                               description='If you want to find a partner right away then try my `TM!search` command.',
        #                                               color=0xCC071F)
        #                         MC.insert_one({'user': ctx.author.id, 'platform': 'bedrock', 'mode': f'{mode}',
        #                                        'IGN': f'{IGN}'})
        #                         await ctx.respond(embed=embed)
        #                         return
        elif game == 'Valorant':
            x = val.find_one({'user':ctx.author.id})
            if x != None:
                await ctx.respond('Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
            else:
                embed = discord.Embed(title='What is your Valorant rank?',
                                      description='The ranks are from lowest to highest:**bronze, iron, silver, gold, platinum, diamond, immortal, radiant**',
                                      color=0xCC071F)
                embed.add_field(name='Please be **TRUTHFUL** when inserting your rank.',
                                value='If found and reported inserting a incorrect rank you can and will be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Valorant rank?', color=0xCC071F)

                async def button_callback(interaction: discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2, view=None)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            VAL = {'user': ctx.author.id, 'rank': f'{rank}'}
                            val.insert_one(VAL)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled", embed=None, view=None)

                button1 = Button(label="Iron", style=discord.ButtonStyle.primary, custom_id='Iron')
                button2 = Button(label="Bronze", style=discord.ButtonStyle.primary, custom_id='Bronze')
                button3 = Button(label="Silver", style=discord.ButtonStyle.primary, custom_id='Silver')
                button4 = Button(label="Gold", style=discord.ButtonStyle.primary, custom_id='Gold')
                button8 = Button(label="Platinum", style=discord.ButtonStyle.primary, custom_id='Platinum')
                button5 = Button(label="Diamond", style=discord.ButtonStyle.primary, custom_id='Diamond')
                button6 = Button(label="Immortal", style=discord.ButtonStyle.primary, custom_id='Immortal')
                button7 = Button(label="Radiant", style=discord.ButtonStyle.primary, custom_id='Radiant')
                cancel = Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                button4.callback = button_callback
                button5.callback = button_callback
                button6.callback = button_callback
                button7.callback = button_callback
                button8.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)
                view.add_item(button8)
                view.add_item(button5)
                view.add_item(button6)
                view.add_item(button7)
                view.add_item(cancel)
                await ctx.respond(embed=embed, view=view)
        elif game == 'Fortnite':
            x = fort.find_one({'user': ctx.author.id})
            if x != None:
                await ctx.respond(
                    'Error You already have this game on your profile. If you need to remove the game try the `TM!remove` command.')
            else:
                embed = discord.Embed(title='What league are you currently in?',
                                      description='The leagues are from lowest to highest:**Open, Contender, Champion**',
                                      color=0xCC071F)
                embed.add_field(name='Please be **TRUTHFUL** when inserting your league.',
                                value='If found and reported inserting a incorrect league you can and will be blacklisted from our services.')
                embed2 = discord.Embed(title='What is your Fortnite league?', color=0xCC071F)

                # buttons for this too
                async def button_callback(interaction: discord.Interaction):
                    if interaction.user.id == ctx.author.id:
                        if interaction.data.get('custom_id') != 'Cancel':
                            rank = interaction.data.get('custom_id')
                            embed2.add_field(name=f'You chose {rank}', value='\u200b')
                            await interaction.response.edit_message(embed=embed2, view=None)
                            embed = discord.Embed(title='Successfully set up your account',
                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                  color=0xCC071F)
                            forts = {'user': ctx.author.id, 'rank': f'{rank}'}
                            fort.insert_one(forts)
                            await ctx.respond(embed=embed)
                        else:
                            await interaction.response.edit_message(content="Cancelled", embed=None, view=None)

                button1 = Button(label="Open", style=discord.ButtonStyle.primary, custom_id='Open')
                button2 = Button(label="Contender", style=discord.ButtonStyle.primary, custom_id='Contender')
                button3 = Button(label="Champion", style=discord.ButtonStyle.primary, custom_id='Champion')
                cancel = Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancel")
                button1.callback = button_callback
                button2.callback = button_callback
                button3.callback = button_callback
                cancel.callback = button_callback
                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(cancel)
                await ctx.respond(embed=embed, view=view)

@bot.slash_command(guild_ids=[877460893439512627])
async def removegame(ctx,game:Option(str,"The game you want removed",required=True,choices=supported_games)):
    """Remove games from your personal profile."""
    if game == 'Rocket League':
        embed = discord.Embed(title='Are you sure you want to delete Rocket League from your profile?',
                              color=0xCC071F)
        async def button_callbacks(interaction: discord.Interaction):
            if interaction.data.get('custom_id') != 'Cancel':
                try:
                    RL.delete_one({'user':ctx.author.id})
                    await interaction.response.edit_message(embed=None,view=None,content="Successfully removed the game.")
                except:
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="A problem occurred, please try again soon.")
            else:
                await interaction.response.edit_message(embed=None,view=None,content="Cancelled")
        button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
        cancel = Button(label="No", style=discord.ButtonStyle.primary, custom_id="No")
        button1.callback = button_callbacks
        cancel.callback = button_callbacks
        view = View()
        view.add_item(button1)
        view.add_item(cancel)
        await ctx.respond(embed=embed, view=view)
    elif game == 'Roblox':
        embed = discord.Embed(title='Are you sure you want to delete Roblox from your profile?',
                              color=0xCC071F)
        async def button_callbacks(interaction: discord.Interaction):
            if interaction.data.get('custom_id') != 'Cancel':
                try:
                    rbx.delete_one({'user': ctx.author.id})
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="Successfully removed the game.")
                except:
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="A problem occurred, please try again soon.")
            else:
                await interaction.response.edit_message(embed=None, view=None, content="Cancelled")

        button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
        cancel = Button(label="No", style=discord.ButtonStyle.primary, custom_id="No")
        button1.callback = button_callbacks
        cancel.callback = button_callbacks
        view = View()
        view.add_item(button1)
        view.add_item(cancel)
        await ctx.respond(embed=embed, view=view)
    # elif game == 'Minecraft':
    #     embed = discord.Embed(title='Are you sure you want to delete Minecraft from your profile?',
    #                           color=0xCC071F)
    #
    #     async def button_callbacks(interaction: discord.Interaction):
    #         if interaction.data.get('custom_id') != 'Cancel':
    #             try:
    #                 MC.delete_one({'user': ctx.author.id})
    #                 await interaction.response.edit_message(embed=None, view=None,
    #                                                         content="Successfully removed the game.")
    #             except:
    #                 await interaction.response.edit_message(embed=None, view=None,
    #                                                         content="A problem occurred, please try again soon.")
    #         else:
    #             await interaction.response.edit_message(embed=None, view=None, content="Cancelled")
    #     button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
    #     cancel = Button(label="No", style=discord.ButtonStyle.primary, custom_id="No")
    #     button1.callback = button_callbacks
    #     cancel.callback = button_callbacks
    #     view = View()
    #     view.add_item(button1)
    #     view.add_item(cancel)
    #     await ctx.respond(embed=embed, view=view)
    elif game == 'Valorant':
        embed = discord.Embed(title='Are you sure you want to delete Valorant from your profile?',
                              color=0xCC071F)

        async def button_callbacks(interaction: discord.Interaction):
            if interaction.data.get('custom_id') != 'Cancel':
                try:
                    RL.delete_one({'user': ctx.author.id})
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="Successfully removed the game.")
                except:
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="A problem occurred, please try again soon.")
            else:
                await interaction.response.edit_message(embed=None, view=None, content="Cancelled")

        button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
        cancel = Button(label="No", style=discord.ButtonStyle.primary, custom_id="No")
        button1.callback = button_callbacks
        cancel.callback = button_callbacks
        view = View()
        view.add_item(button1)
        view.add_item(cancel)
        await ctx.respond(embed=embed, view=view)
    elif game == 'Fortnite':
        embed = discord.Embed(title='Are you sure you want to delete Fortnite from your profile?',
                              color=0xCC071F)


        async def button_callbacks(interaction: discord.Interaction):
            if interaction.data.get('custom_id') != 'Cancel':
                try:
                    fort.delete_one({'user': ctx.author.id})
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="Successfully removed the game.")
                except:
                    await interaction.response.edit_message(embed=None, view=None,
                                                            content="A problem occurred, please try again soon.")
            else:
                await interaction.response.edit_message(embed=None, view=None, content="Cancelled")

        button1 = Button(label="Yes", style=discord.ButtonStyle.danger, custom_id='Yes')
        cancel = Button(label="No", style=discord.ButtonStyle.primary, custom_id="No")
        button1.callback = button_callbacks
        cancel.callback = button_callbacks
        view = View()
        view.add_item(button1)
        view.add_item(cancel)
        await ctx.respond(embed=embed,view=view)
@bot.slash_command(guild_ids=[877460893439512627])
async def suggest(ctx):
    """Suggest features and or games for the bot"""
    embed = discord.Embed(title='Thanks for making a suggestion.',description='Whatever your next message is will be send as a suggestion. Please try to be a through as you can.',color=0xCC071F)
    await ctx.respond(embed=embed)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.message.channel
    try:
        x = await bot.wait_for('message',timeout=600,check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title='You had 10 minutes to submit your suggestion.',description='If that isnt enought time just join our support server to submit your suggestion, which you can find [here](https://discord.gg/5XAubY2v3N)',color=0xCC071F)
        await ctx.respond(embed = embed)
    else:
        embed= discord.Embed(title='Thank you for submitting a suggestion.',description='The devs will be sure to look at it, and maybe consider adding it as a feature',color=0xCC071F)
        await ctx.respond(embed=embed)
        embed= discord.Embed(title=f'Suggestion from {ctx.author}',description=f'{x.content}',color=0xCC071F)
        channel = bot.get_channel(822858852143464558)
        await channel.send(embed = embed)

@bot.slash_command(guild_ids=[877460893439512627])
async def report(ctx):
    """report users."""
    embed = discord.Embed(title='Thank you for using our report feature to try and help keep our community troll-free',description='Now when submitting your report please include all of the following... Who are you reporting. Why are you reporting(include name and # or just user id. Your choice.). Add any sort of evidence.(pictures are accepted).',color=0xCC071F)
    await ctx.respond(embed = embed)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.message.channel
    try:
        x = await bot.wait_for('message',timeout=600,check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title='You had 10 minutes to submit your report.',description='If that isnt enought time just join our support server to report the user which you can find [here](https://discord.gg/5XAubY2v3N)',color=0xCC071F)
        await ctx.respond(embed = embed)
    else:
        embed = discord.Embed(title='Thank you for submitting a report.',description='Our Moderators will take a look at it soon.',color=0xCC071F)
        await ctx.respond(embed=embed)
        embed = discord.Embed(title=f'New report Submitted by {ctx.author}',description=f'{x.content}',color=0xCC071F)
        if x.attachments:
            embed.set_image(url=x.attachments[0].url)
        channel = bot.get_channel(822858888578990090)
        await channel.send(embed = embed)

@bot.command(hidden=True)
async def getid(ctx,user:discord.User):
    if user != None:
        await ctx.respond('Found')
        await ctx.respond(user.id)
    else:
        await ctx.respond('Couldnt find user...')

@bot.slash_command(guild_ids=[877460893439512627])
async def blacklist(ctx,func:Option(str,"what your doing to the blacklist",required=True,choices=['add','remove','find']),user:discord.User,*,reason=None):
    if ctx.author.id == 705992469426339841:
        if func == 'add':
            if reason == None:
                await ctx.respond("please add a reason.")
                return
            await ctx.respond(f'Added {user}. Reason: {reason}')
            BL.insert_one({'user': user.id, 'reason': f'{reason}'})
        elif func == 'remove':
            BL.delete_one({'user':user.id})
            await ctx.respond(f'Removed {user}')
        elif func == 'find':
            x = BL.find_one({'user':user.id})
            if x == None:
                await ctx.respond("User not found in blacklist")
                return
            await ctx.respond(f'Blacklist for {user}: {x.get("reason")}')
    else:
        return

@blacklist.error
async def bl_error(ctx,error):
    await ctx.respond(error)

@bot.slash_command(guild_ids=[877460893439512627])
async def admindelete(ctx,user:discord.User):
    if ctx.author.id == 705992469426339841:
        user = user.id
        Profiles.deletion(user)
        await ctx.respond('Deleted User\'s profile successfully')

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
            embed = discord.Embed(title='It has been an hour and no one has been matched with you.',description='You could either do the following: Requeue using `/search` or just wait for a little bit of time for some other users who are the same rank as you to queue aswell: sorry for the inconvience',color=0xCC071F)
            embed.set_footer(text='Thank you for using our services.')
            match.delete_one({"user":user})
            user = int(user)
            person = bot.get_user(user)
            await person.send(embed = embed)
        else:
            return

@bot.slash_command(guild_ids=[877460893439512627])
async def delprofile(ctx):
    """Delete your profile."""
    async def button_callback(interaction:discord.Interaction):
        if ctx.author.id == interaction.user.id:
            if interaction.data.get('custom_id') == 'Delete':
                Profiles.deletion(ctx.author.id)
                await interaction.response.edit_message(content="successfully deleted.",embed=None,view=None)
            else:
                await interaction.response.edit_message(content="Not deleting your profile.",embed=None,view=None)
    embed=discord.Embed(title='Are you sure you want to delete your profile.',description='If you say yes you lose all the games set up with your account and you will have to reset it up.',color=0xCC071F)
    button = Button(custom_id='Cancel',label='Cancel',style=discord.ButtonStyle.primary)
    button1 = Button(custom_id='Delete',label='Delete',style=discord.ButtonStyle.danger)
    button.callback = button_callback
    button1.callback = button_callback
    view = View()
    view.add_item(button)
    view.add_item(button1)
    await ctx.respond(embed = embed,view=view)
@bot.slash_command(guild_ids=[877460893439512627])
async def profile(ctx,user:discord.User = None):
    """Check out your profile"""
    if user == None:
        user = ctx.author
    x = Profiles.profiles(user.id)
    if x == None:
        if user.id != ctx.author.id:
            await ctx.respond('Error: User doesnt have a profile.')
        else:
            await ctx.respond('Error: user doesnt have a profile. Set up one using the `TM!setup` command')
    else:
        embed = discord.Embed(title=f'Profile for {user}',description=f'Region: {x.get("region")} ',color=0xCC071F)
        x = Profiles.rocket(user.id)
        if x != None:
            embed.add_field(name='Rocket League',value=f'Rank: {x.get("rank")}',inline=False)
        x = None
        x = rbx.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Roblox', value=f'Username: {x.get("name")}', inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        # x = MC.find_one({'user':user.id})
        # if x != None:
        #     embed.add_field(name='Minecraft',value=f'IGN: {x.get("IGN")} \n Platform: {x.get("platform")}', inline=False)
        x = val.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Valorant',value=f'rank: {x.get("rank")}',inline=False)
        x = fort.find_one({'user':user.id})
        if x != None:
            embed.add_field(name='Fortnite',value=f'rank: {x.get("rank")}',inline=False)
        await ctx.respond(embed=embed)

@bot.slash_command(guild_ids=[877460893439512627])
async def invite(ctx):
    """Invite me to your server today!"""
    embed = discord.Embed(title='Invite TM to your server today!',description='[click here](https://discord.com/api/oauth2/authorize?client_id=822637954769879100&permissions=379905&scope=bot)',color=0xCC071F)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[877460893439512627])
async def tutorial(ctx):
    """If you need help with Tilted Matchmaking"""
    embed = discord.Embed(title='Do you find TM a bit to hard to understand?',description='Then have a look at a very simple tutorial on how to setup your profile. You can find that video [here](https://youtu.be/dOZHazMxcag)',color=0xCC071F)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[877460893439512627])
async def help(ctx):
    """The help section"""
    embed = discord.Embed(title='Tilted Matchmaking Help Section',description='All of TM\'s commands. If you need any assistance join our help server which you can find [here](https://discord.gg/rKWxkrCkUQ)',color=0xCC071F)
    embed.add_field(name='Profile Commands',value='`/setup`\n`/profile`\n`/delprofile` \n`/addgame`\n`/removegame`',inline=False)
    embed.add_field(name='Matchmaking Commands',value='`/search` \n`/cancel `',inline= False)
    embed.add_field(name='Utilities',value='`/suggest`\n`/panel` \n`/report`\n`/games` \n`/invite`\n`/tutorial`',inline=False)
    embed.add_field(name='\u200b',value='Need help with TM but dont want to join the support server? check out the tutorial video thats on youtube. You can find it [here](https://youtu.be/dOZHazMxcag)')
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[877460893439512627])
async def vote(ctx):
    """Vote for us!!!"""
    embed = discord.Embed(title='Vote for us on top.gg!',description='You can find the link [here.](https://top.gg/bot/822637954769879100/vote)',color=0xCC071F)
    await ctx.respond(embed = embed)


@bot.slash_command(guild_ids=[877460893439512627])
@commands.has_permissions(manage_channels=True)
async def panel(ctx,channel:discord.TextChannel = None):
    """Member setup panel, A ease of use feature to help your server members gain a profile."""
    if channel == None:
        channel = ctx.channel
    first = await ctx.respond(f"Sending A setup panel to <#{channel.id}>")
    embed = discord.Embed(title='Account Setup',description='React to this embed to setup your account.',color=0xCC071F)
    embed.set_footer(text='If you react to this embed you will be sent a DM by the bot to set up your account.')
    x = await channel.send(embed = embed)
    emoji = bot.get_emoji(838234937743245382)
    await x.add_reaction(emoji)
    await asyncio.sleep(3)
    await ctx.delete()


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
