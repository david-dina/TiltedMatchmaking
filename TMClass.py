import pymongo
import discord
from discord.ext.commands import Greedy
from discord import Embed as Embed
from discord.ext import commands,tasks
from discord.ui import Button,View
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

    def rocket(self,user) -> dict:
        playa = RL.find_one({'user': user})
        return playa

    def profiles(self,user) -> dict:
        playa = profiling.find_one({'user': user})
        return playa

    def blacklisted(self,user) -> dict:
        x = BL.find_one({'user': user})
        return x

    def MC_ranks(self,lvl: int) -> str:
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

    def deletion(self,user) -> None:
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

    async def location(self,user:discord.User,channel: Greedy[int] = None) -> None:
        if channel == None:
            ctx = user
        else:
            ctx = self.bot.get_channel(channel)
        async def button_callback(interaction: discord.Interaction):
            if interaction.user.id == user.id:
                if interaction.data.get('custom_id') != 'Cancel':
                    region = interaction.data.get('custom_id')
                    Profile = {'user': user.id, 'region': f'{region}'}
                    if profiling.find_one(Profile):
                        return
                    profiling.insert_one(Profile)
                    await interaction.delete_original_message()
                    embed = discord.Embed(title='Successfully set up your account',
                                          description='If you want to find a partner right away then try my `TM!search` command.',
                                          color=0xCC071F)
                    await interaction.response.send_message(embed=embed)
        button1 = Button(label="North America", style=discord.ButtonStyle.primary, custom_id='na')
        button2 = Button(label="Europe", style=discord.ButtonStyle.primary, custom_id='eu')
        button3 = Button(label="South America", style=discord.ButtonStyle.primary, custom_id='sa')
        button4 = Button(label="Asia", style=discord.ButtonStyle.primary, custom_id='asia')
        button5 = Button(label="Australia", style=discord.ButtonStyle.primary, custom_id='australia')
        button1.callback = button_callback
        button2.callback = button_callback
        button3.callback = button_callback
        button4.callback = button_callback
        button5.callback = button_callback
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)

        embed = discord.Embed(title='Where are you from?',
                              description='We need this information in order to find people who are nearest to you. so you wont have to worry about latency.(for games that require it.)',
                              color=0xCC071F)
        embed.add_field(name='The supported locations are as followed.',
                        value='North America: NA \n South America: SA \n Europe: EU \n Asia \n Australia')
        embed.set_footer(
            text='If there is a location that is not currently supported that you would like Suggest it using TM!suggest.')
        await ctx.send(embed=embed,view=view)



    async def teammateyes(self,ctx,user) -> bool:
        embed = Embed(title=f'Succesfully found you a teammate. His name is {ctx.user.name}',description=f'Inviting to the Official Tilted Matchmaking server for interaction.',color=0xCC071F)
        embed.add_field(name='Are you ready to be invited?',value='if no your spot in the queue will be deleted.')
        await user.send(embed=embed)
        async def button_callback(interaction: discord.Interaction):
            if interaction.user.id == user.id:
                if interaction.data.get('custom_id') != 'No':
                    #if said no go into database and take user out of it.
                    await interaction.response.send_message(embed=embed)
        #timeout=300
        button1 = Button(label="North America", style=discord.ButtonStyle.primary, custom_id='na')
        button2 = Button(label="Europe", style=discord.ButtonStyle.primary, custom_id='eu')
        namesters = ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'n', 'N']
        def check(message):
            return message.content in namesters and message.user == user
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
            channel = self.bot.get_channel(1002096611108851794)
            await channel.send(embed=embed)
            return True
        elif gottem.content == 'N' or gottem.content == 'No' or gottem.content == 'no' or gottem.content == 'n':
            return False