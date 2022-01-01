import discord
import pymongo
import asyncio
from TMClass import Profiles, UserProfiles
Profiles = Profiles()
supported = ['RL','rl','Roblox','roblox','MC','mc','Mc','Val','val','Fortnite','fortnite',"CSGO",'Csgo','csgo']
#chenpickle
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
CSGO = db.CSGO

class Reaction:
    def __init__(self,bot):
        self.bot = bot

    async def setup(self,user):
        """Set up your personal profile using this command"""
        user = self.bot.get_user(user)
        embed = discord.Embed(title=f'New Profile Setup by {user} via panel', color=0xCC071F)
        channel = self.bot.get_channel(826331977257844746)
        await channel.send(embed = embed)
        perp = Profiles.blacklisted(user.id)
        if perp != None:
            embed = discord.Embed(
                title=f'Error: You have been blacklisted from our services for: {perp.get("reason")} ',
                description='If You wish to appeal your sentence than please join our support server [here](https://discord.gg/5XAubY2v3N) and open a ticket.',
                color=0xCC071F)
            await user.send(embed=embed)
        else:
            embed = discord.Embed(title=f'Profile Setup for {user.name}', color=0xCC071F)
            embed.add_field(name=f'To setup your profile you first have to give a me one game that you play.',
                            value='To find all the currently supported games please try `TM!games`')
            embed.set_footer(text='To add any more games to your profile try TM!addgame command')
            await user.send(embed=embed)

            def check(message):
                return (message.content in supported) and (message.author == user)
            try:
                msg = await self.bot.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                await user.send('You didnt respond... Cancelling setup.')
            else:
                if msg.content == 'RL' or msg.content == 'rl':
                    embed = discord.Embed(title='What is your Rocket League rank?',
                                          description='The ranks are from lowest to highest:** bronze, silver, gold, platinum, diamond, gc, ssl**',
                                          color=0xCC071F)
                    embed.add_field(name='you can either choose your 1\'s 2\'s or 3\'s',
                                    value='Please also just put your rank not tier.', inline=False)
                    embed.add_field(
                        name='When putting in your rank please be truthful for this is to help you find a teammate around your rank.',
                        value='if put in a False rank you account can be reported. Then can be blacklisted from our services.')
                    embed.set_footer(text='When saying your rank please do it as exactly as you see above.')
                    await user.send(embed=embed)
                    rank = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'gc', 'ssl', 'Bronze', 'Silver',
                            'Gold', 'Platinum', 'Diamond', 'Gc', 'Ssl']

                    def check(message):
                        return message.content in rank and (message.author == user)

                    try:
                        answer = await self.bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await user.send('You didnt respond... Cancelling setup.')
                    else:
                        await UserProfiles.location(self.bot,user)
                        answer = answer.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        rl = {'user': user.id, 'rank': f'{answer}'}
                        RL.insert_one(rl)
                        await user.send(embed=embed)
                elif msg.content == 'Roblox' or msg.content == 'roblox':
                    embed = discord.Embed(title='What is your Roblox username?', color=0xCC071F)
                    await user.send(embed=embed)

                    def check(message):
                        return (message.author == user)

                    try:
                        answer = await self.bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await user.send('You didnt respond... Cancelling setup.')
                    else:
                        await UserProfiles.location(self.bot,user)
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        await user.send(embed=embed)
                        rbx.insert_one({'user': user.id, 'name': f'{answer.content}'})
                elif msg.content == 'MC' or msg.content == 'mc' or msg.content == 'Mc':
                    embed = discord.Embed(title='Do you play Minecraft Java or Bedrock?', color=0xCC071F)
                    await user.send(embed=embed)
                    platform = ['Java', 'java', 'Bedrock', 'bedrock']

                    def check(message):
                        return (message.content in platform) and (
                                    message.author == user)

                    try:
                        platform = await self.bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await user.send('You didnt respond... Cancelling setup.')
                    else:
                        platform = platform.content.lower()
                        if platform == 'java':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
                                                  description='Survival \n PVP: ex.Hypixel Network \n Modded: ex. FeedTheBeast minecraft modpacks',
                                                  color=0xCC071F)
                            embed.set_footer(
                                text='To change this you are going to have to delete and readd this to your profile')
                            await user.send(embed=embed)
                            gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp', 'Modded', 'modded']

                            def check(message):
                                return (message.content in gamemode) and (
                                            message.author == user)

                            try:
                                mode = await self.bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await user.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
                                await user.send(embed=embed)

                                def check(message):
                                    return (message.author == user)

                                try:
                                    IGN = await self.bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await user.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    if mode == 'pvp':
                                        embed = discord.Embed(
                                            title='What are your current stars. In Hypixel (the only current supported server)',
                                            description='Choose any pvp mod you want', color=0xCC071F)
                                        await user.send(embed=embed)
                                        def check(message):
                                            return (message.author == user)

                                        try:
                                            stars = await self.bot.wait_for('message', timeout=30, check=check)
                                        except asyncio.TimeoutError:
                                            await user.send('You didnt respond... Cancelling setup.')
                                        else:
                                            await UserProfiles.location(self.bot,user)
                                            stars = int(stars.content)
                                            embed = discord.Embed(title='Succesfully set up your account',
                                                                  description='If you want to find a partner right away then try my `TM!search` command.',
                                                                  color=0xCC071F)
                                            info = {'user': user.id, 'platform': f'{platform}', 'mode': 'pvp',
                                                    'IGN': f'{IGN}', 'stars': stars}
                                            MC.insert_one(info)
                                            await user.send(embed=embed)
                                    elif mode == 'survival':
                                        await UserProfiles.location(self.bot,user)
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                                              color=0xCC071F)
                                        info = {'user': user.id, 'platform': f'{platform}',
                                                'mode': 'survival', 'IGN': f'{IGN}'}
                                        MC.insert_one(info)
                                        await user.send(embed=embed)


                                    elif mode == 'modded':
                                        await UserProfiles.location(self.bot,user)
                                        embed = discord.Embed(title='Succesfully set up your account',
                                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                                              color=0xCC071F)

                                        info = {'user': user.id, 'platform': f'{platform}', 'mode': 'modded',
                                                'IGN': f'{IGN}'}
                                        MC.insert_one(info)
                                        await user.send(embed=embed)
                        elif platform == 'bedrock':
                            embed = discord.Embed(title='What gamemode do you wish to find a partner for.',
                                                  description='Survival \n PVP: ex.Cubed Network',
                                                  color=0xCC071F)
                            embed.set_footer(
                                text='To change this you are going to have to delete and read this to your profile')
                            await user.send(embed=embed)
                            gamemode = ['Survival', 'survival', 'PVP', 'pvp', 'Pvp']

                            def check(message):
                                return (message.content in gamemode) and (
                                        message.author == user)

                            try:
                                mode = await self.bot.wait_for('message', timeout=30, check=check)
                            except asyncio.TimeoutError:
                                await user.send('You didnt respond... Cancelling setup.')
                            else:
                                embed = discord.Embed(title='What is your IGN?', color=0xCC071F)
                                await user.send(embed=embed)

                                def check(message):
                                    return (message.author == user)

                                try:
                                    IGN = await self.bot.wait_for('message', timeout=30, check=check)
                                except asyncio.TimeoutError:
                                    await user.send('You didnt respond... Cancelling setup.')
                                else:
                                    IGN = IGN.content.lower()
                                    mode = mode.content.lower()
                                    await UserProfiles.location(self.bot,user)
                                    embed = discord.Embed(title='Succesfully set up your account',
                                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                                          color=0xCC071F)
                                    MC.insert_one({'user': user.id, 'platform': 'bedrock', 'mode': f'{mode}',
                                                   'IGN': f'{IGN}'})
                                    await user.send(embed=embed)
                elif msg.content == 'Val' or msg.content == 'val':
                    embed = discord.Embed(title='What is your Valorant rank?',
                                          description='The ranks are from lowest to highest:**bronze, iron, silver, gold, platinum, diamond, immortal, radiant**',
                                          color=0xCC071F)
                    embed.add_field(name='Please be Truthful when inserting your rank.',
                                    value='If found and reported inserting a incorrect rank you can and will be blacklisted from our services.')
                    await user.send(embed=embed)
                    rank = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'immortal', 'radiant',
                            'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Immortal', 'Radiant']

                    def check(message):
                        return message.content in rank and message.author == user

                    try:
                        rank = await self.bot.wait_for('message', timeout=45, check=check)
                    except asyncio.TimeoutError:
                        await user.send('Error: You didnt respond in time... Cancelling setup.')
                    else:
                        await UserProfiles.location(self.bot,user)
                        rank = rank.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        val.insert_one({'user': user.id, 'rank': f'{rank}'})
                        await user.send(embed=embed)


                elif msg.content == 'Fortnite' or msg.content == 'fortnite':
                    embed = discord.Embed(title='What League are you currently in?',
                                          description='The leagues are from lowest to highest:**Open, Contender, Champion**',
                                          color=0xCC071F)
                    await user.send(embed=embed)
                    rank = ['open', 'Open', 'Contender', 'contender', 'Champion', 'champion']

                    def check(message):
                        return message.content in rank and message.author == user

                    try:
                        rank = await self.bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await user.send('Error: You didnt respond in time... Cancelling setup.')
                    else:
                        await UserProfiles.location(self.bot,user)
                        rank = rank.content.lower()
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        fort.insert_one({'user': user.id, 'rank': f'{rank}'})
                        await user.send(embed=embed)
                elif (msg.content == 'CSGO' or msg.content == 'Csgo' or msg.content == 'csgo'):
                    embed = discord.Embed(title='What is your current rank for CSGO?',
                                          description='Your options are: Silver, Silver elite, silver elite master: SEM, gold nova, gold nova master: GNM, master guardian: MG, master guardian elite: MGE, distinguished master guardian: DMG, legendary eagle: LE, legendary eagle master: LEM, supreme master first class: SMFC, the global elite: TGE.',
                                          color=0xCC071F)
                    embed.add_field(name='Please Note.',
                                    value="If you want to insert a rank with tiers Only put the rank name. ex: Silver 2 would just be Silver.")
                    embed.set_footer(
                        text='If a rank name has a : beside it please put the abbreviated version as the answer ex: Distinguished master guardian would just be "DMG".')
                    await user.send(embed=embed)
                    ze_rank = ['silver', 'silver elite', 'sem', 'gold nova', 'gnm', 'mg', 'mge', 'dmg', 'le', 'lem',
                               'smfc', 'tge']

                    def check(message):
                        return (message.author == user and message.content.lower() in ze_rank)

                    try:
                        rank = await self.bot.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await user.send('You didnt respond... Cancelling setup.')
                    else:
                        rank = rank.content.lower()
                        await UserProfiles.location(self.bot,user)
                        rank_info = {'user': user.id, 'rank': f'{rank}'}
                        CSGO.insert_one(rank_info)
                        embed = discord.Embed(title='Succesfully set up your account',
                                              description='If you want to find a partner right away then try my `TM!search` command.',
                                              color=0xCC071F)
                        await user.send(embed=embed)