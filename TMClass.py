import pymongo
import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import Greedy
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
dbv5 = client.server
da_matches = dbv5.match

client = pymongo.MongoClient('mongodb+srv://starlord:Adeoluwa.05@cluster0.52enc.mongodb.net/myFirstDatabase&retryWrites=true&w=majority?ssl=true&ssl_cert_reqs=CERT_NONE',connect=False)
db = client.server
connected = db.matches

class Profiles:

    def rocket(self,user):
        playa = RL.find_one({'user': user})
        return playa

    def profiles(self,user):
        playa = profiling.find_one({'user': user})
        return playa

    def blacklisted(self,user):
        x = BL.find_one({'user': user})
        return x

    def MC_ranks(self,lvl: int):
        if lvl <= 100:
            return 'stone'
        else:
            if lvl <= 200:
                return 'bronze'
            else:
                if lvl <= 300:
                    return 'iron'
                else:
                    if lvl <= 400:
                        return 'gold'
                    else:
                        if lvl <= 500:
                            return 'diamond'
                        else:
                            if lvl <= 600:
                                return 'emerald'
                            else:
                                if lvl > 600:
                                    return 'godly'

    def deletion(self,user):
        RL.delete_one({'user': user})
        match.delete_one({'user': user})
        profiling.delete_one({'user': user})
        rbx.delete_one({'user': user})
        MC.delete_one({'user': user})
        val.delete_one({'user':user})
        fort.delete_one({'user':user})

class UserProfiles:
    def __init__(self,bot):
        self.bot = bot


    async def location(self,user:discord.User,channel: Greedy[int] = None):
        if channel == None:
            ctx = user
        else:
            ctx = self.bot.get_channel(channel)
        region = ['NA', 'na', 'EU', 'eu', 'SA', 'sa', 'Asia', 'asia', 'Australia', 'australia']
        embed = discord.Embed(title='Where are you from?',
                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                              color=0xCC071F)
        embed.add_field(name='The supported locations are as followed.',
                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
        embed.set_footer(
            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
        await ctx.send(embed=embed)
        try:
            x = self.bot.get_channel(channel)
        except:
            x = None
            pass
        if x == None:
            def check(message):
                return message.content in region and message.author == user
        else:
            def check(message):
                return message.content in region and message.author == user and message.channel == ctx.channel
        if isinstance(self,commands.Bot):
            try:
                location = await self.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didnt respond... Cancelling setup.')
            else:
                location = location.content.lower()
                Profile = {'user': user.id, 'region': f'{location}'}
                profiling.insert_one(Profile)
        else:
            try:
                location = await self.bot.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didnt respond... Cancelling setup.')
            else:
                location = location.content.lower()
                Profile = {'user': user.id, 'region': f'{location}'}
                profiling.insert_one(Profile)



    async def teammateyes(self,ctx,user) -> bool:
        embed = discord.Embed(title=f'Succesfully found you a teammate. His name is {ctx.author.name}',
                              description=f'Inviting you to their server which is: {ctx.guild.name}.',
                              color=0xCC071F)
        embed.add_field(name='Are you ready to be invited?',
                        value='Yes or No?: if no your spot in the queue will be deleted.')
        await user.send(embed=embed)
        namesters = ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'n', 'N']

        def check(message):
            return message.content in namesters and message.author == user
        gottem = await ctx.bot.wait_for('message', timeout=120, check=check)
        if gottem.content == 'yes' or gottem.content == 'Yes' or gottem.content == 'y' or gottem.content == 'Y':
            await user.send(f'Ok, getting you your invite. Remember to look out for {ctx.author.mention}')
            embed = discord.Embed(title=f'Successfully found you a teammate. His name is {user.name}',
                                  description=f'Inviting you both to the TM Matchmaking server.',
                                  color=0xCC071F)
            await ctx.author.send(embed=embed)
            #guild = ctx.bot.get_guild(864014262234251304)
            #category = discord.utils.get(guild.categories, id=864014262234251307)
            #channel = ctx.bot.get_channel(864015076552998933)
            #x = await channel.create_invite(reason='Successful Match Made.', max_age=3600, max_usage=5)
            x = ctx.channel.create_invite(reason='Successful Match Made.', max_age=3600, max_usage=5)

            await user.send(f'{x}')
            await ctx.author.send(f'Here is your invite: {x}')
            await ctx.author.send(f'Remember to look out for {user.mention}')
            match.delete_one({"user": user.id})
            match.delete_one({"user": ctx.author.id})
            # overwritestxt = {
            #     guild.default_role: discord.PermissionOverwrite(read_messages=False)
            # }
            # overwritesvc = {
            #     guild.default_role: discord.PermissionOverwrite(view_channel=False)
            # }
            # created = await guild.create_text_channel(f'{ctx.author.id}', category=category,overwrites=overwritestxt)
            # voice = await guild.create_voice_channel(f'{user.id}', category=category,overwrites=overwritesvc)
            # perms = discord.PermissionOverwrite()
            # perms.speak = True
            # perms.connect = True
            # perms.view_channel = True
            # voices = ctx.bot.get_channel(voice.id)
            # author = guild.get_member(ctx.author.id)
            # this_guy = guild.get_member(user.id)
            # try:
            #     await voices.set_permissions(author, overwrite=perms)
            #     await created.set_permissions(author, overwrite=discord.PermissionOverwrite(read_messages=False))
            # except:
            #     pass
            # try:
            #     await voices.set_permissions(this_guy, overwrite=perms)
            #     await created.set_permissions(this_guy, overwrite=discord.PermissionOverwrite(read_messages=False))
            # except:
            #     pass
            # try:
            #     connected.insert_one({f'{ctx.author.id}':f'{user.id}'})
            #     connected.insert_one({f'{user.id}':f'{ctx.author.id}'})
            #except Exception as e:
            #    print(e)
            await ctx.author.send('Thank you for using our services.')
            await user.send('Thank you for using our services.')
            embed = discord.Embed(title='A Match was successfully made', color=0xCC071F)
            embed.add_field(name='The couple in question:', value=f'{ctx.author} and {user}', inline=False)
            embed.add_field(name='The guild:', value=f'{ctx.guild.name} [here]({x})')
            channel = self.bot.get_channel(826334789169578015)
            await channel.send(embed=embed)
            return True
        elif gottem.content == 'N' or gottem.content == 'No' or gottem.content == 'no' or gottem.content == 'n':
            return False