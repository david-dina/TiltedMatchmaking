import discord
from discord.ext import commands
import pymongo
from TMclassv2 import Reaction

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='beta',intents=intents,status=discord.Status.dnd,activity=discord.Activity(name='down for maintenence',type=discord.ActivityType.watching))
client = pymongo.MongoClient("mongodb+srv://starlord:Adeoluwa.05@playerinfo.t5g9l.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
dbv3 = client.Profile
profiling = dbv3.User
Reaction = Reaction()
@bot.event
async def on_ready():
    print(f'{bot.user} is online')


@bot.command()
@commands.has_permissions(manage_channels=True)
async def panel(ctx,channel:discord.TextChannel = None):
    if channel == None:
        channel = ctx.channel
    embed = discord.Embed(title='Account Setup',description='React to this embed to setup your account.',color=0xCC071F)
    embed.set_footer(text='If you react to this embed you will be sent a DM by the bot to set up your account.')
    x = await channel.send(embed = embed)
    emoji = bot.get_emoji(838234937743245382)
    await x.add_reaction(emoji)
    emoji = bot.get_emoji(817866981418991687)
    await ctx.message.add_reaction(emoji)


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
                await y.remove_reaction(emoji,user)
                z = profiling.find_one({'user':user.id})
                if z == None:
                    await Reaction.setup(payload.member.id)
                else:
                    await user.send('Error you already have your profile setup. If you wish to add more games try the `TM!addgame` command.')




bot.run('ODIyNjM3OTU0NzY5ODc5MTAw.YFVLTA.heIliLdUJYanfdNbf6iObYIxtLU')