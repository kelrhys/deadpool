import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
client = commands.Bot(description="Custom profile creation and lookup", command_prefix="d/", pm_help = False)

# This is what happens every time the bot launches. 
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0x2000'.format(client.user.id))
	print('--------')
	client.load_extension("ProfileCog")

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command(pass_context=True)
async def ping(ctx):
	await client.say(":ping_pong: Pong!")
	print ("user has pinged")

@client.command(aliases=["fg", "fingergun"], pass_context=True)
async def fingerguns(ctx, member:discord.Member):
	await client.say('{0.mention} :point_right: :point_right: {1.mention}'.format(ctx.message.author, member))
	print ("sent point_right from {} to {}".format(ctx.message.author, member))

	try:
		await client.delete_message(ctx.message)
		print ("deleted message")
	except Exception:
		await client.say('I do not have permission to delete the message.')

@client.command(aliases=["fgback", "fingergunback"], pass_context=True)
async def fingergunsback(ctx, member:discord.Member):
	await client.say('{0.mention} :point_left: :point_left: {1.mention}'.format(ctx.message.author, member))
	print ("sent point_left from {} to {}".format(ctx.message.author, member))
	
	try:
		await client.delete_message(ctx.message)
		print ("deleted message")
	except Exception:
		await client.say('I do not have permission to delete the message.')
	
client.run("NDE4ODk4ODc2MTU4NzA1NjY3.DXoRog.Zf1mfmKndvxrUKwI-wSbaSF3OWk")

