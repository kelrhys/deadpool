import discord
from discord.ext import commands

class ProfileCog:
	def __init__(self, bot):
		self.bot = bot
		self.theProfiles = {}
    
				
	async def showProfile(self, primarykey:discord.Member):
		em = discord.Embed(title="", colour=discord.Colour.blue())
		em.set_author(name=primarykey, icon_url=primarykey.avatar_url)
		for key,val in self.theProfiles[primarykey].items():
			print("{}: {}".format(key, val))
			em.add_field(name=key, value=val)
		await self.bot.say(embed=em)
	
	async def showProfiles(self):
		em = discord.Embed(title="All Profiles", colour=discord.Colour.green())
		await self.bot.say(embed=em)
		for key in self.theProfiles:
			print("{}".format(key))
			await self.showProfile(key)
		
	@commands.command(pass_context=True)
	async def hello(self, ctx):
		await self.bot.say("Hello")
		
	@commands.command(pass_context=True)
	async def profiles(self, ctx):
		# Display all profiles
		await self.showProfiles()

	@commands.group(pass_context=True)
	async def profile(self, ctx):
		if ctx.invoked_subcommand is None:
			print("profile with no subcommand, display profile for: {}".format(ctx.message.author))

			# Display my own profile
			await self.showProfile(ctx.message.author)

	@profile.command(pass_context=True, name="create")
	async def profile_create(self, ctx, member:discord.Member):
		# Currently this will overwrite any existing profile information! 
		newProfile = {}
		newProfile["Name"] = member.name
		newProfile["Nickname"] = member.nick
		newProfile["Gender"] = "unknown"
		newProfile["Timezone"] = "unknown"
		newProfile["Rank"] = "unknown"
		newProfile["Role"] = member.top_role
		newProfile["IsAdmin"] = member.top_role.permissions.administrator
		newProfile["Server"] = member.server.name
		newProfile["ServerID"] = member.server.id
		self.theProfiles[member] = newProfile

	@commands.command(pass_context=True)
	async def debugShowProfiles(self):
		for key in self.theProfiles:
			print("{}".format(key))
			for skey, val in self.theProfiles[key].items():
				print("{}: {}".format(skey, val))

# Get duplicate commands when this is enabled.				
#	async def on_message(self, message):
#		if message.content.startswith('d/test'):
#			member = message.author
#			await self.bot.send_message(message.channel, '{0.mention} sent message'.format(member))
#		await self.bot.process_commands(message)

	async def setupNewProfile(self, member:discord.Member):
		newProfile = {}
		newProfile["Name"] = member.name
		newProfile["Nickname"] = member.nick
		newProfile["Role"] = member.top_role
		newProfile["IsAdmin"] = member.top_role.permissions.administrator
		newProfile["Server"] = member.server.name
		newProfile["ServerID"] = member.server.id
		
		await self.bot.send_message(member, 'Please state your current role within this organization.')
		role = await self.bot.wait_for_message(timeout=20, author=member)
		if role is None:
			newProfile["Role"] = "no response"
		else:
			newProfile["Role"] = role.content
		await self.bot.send_message(member, 'Very well, you have been assigned the {} role. What is your geographical timezone?'.format(newProfile["Role"]))
		timezone = await self.bot.wait_for_message(timeout=20,author=member)
		if timezone is None:
			newProfile["Timezone"] = "no response"
		else:
			newProfile["Timezone"] = timezone.content
		await self.bot.send_message(member, 'I have set your Timezone to {}. What is your might/level/rank in the game?'.format(newProfile["Timezone"]))
		rank = await self.bot.wait_for_message(timeout=20,author=member)
		if rank is None:
			newProfile["Rank"] = "no response"
		else:
			newProfile["Rank"] = rank.content
		await self.bot.send_message(member, 'Great, I have set your Rank to {}. Finally, as what gender would you prefer to be known?'.format(newProfile["Rank"]))
		gender = await self.bot.wait_for_message(timeout=20,author=member)
		if gender is None:
			newProfile["Gender"] = "no response"
		else:
			newProfile["Gender"] = gender.content
		await self.bot.send_message(member, 'Your gender has been set to {}. The Inquisition is over!'.format(newProfile["Gender"]))

		self.theProfiles[member] = newProfile
		await self.bot.send_message(member, 'I have set your Discord Role to {} according to this organization\'s leaders.'.format(newProfile["Role"]))
		await self.bot.send_message(member, 'Please read channel XYZ for help getting started. Good luck, my friend!')
		
	async def on_message(self, message):
		if message.content.startswith('$cool'):
			await self.bot.send_message(message.channel, 'Who is cool? Type $name namehere')

			def check(msg):
				return msg.content.startswith('$name')

			message2 = await self.bot.wait_for_message(author=message.author, check=check(message))
			name = message2.content[len('$name'):].strip()
			await self.bot.send_message(message2.channel, '{} is cool indeed'.format(name))
			
		if message.content.startswith('t/testjoin'):
			member = message.author
			await self.bot.send_message(member, 'Welcome {0.mention}!'.format(member))
			await self.setupNewProfile(member)
		
	async def on_member_join(self, member):
		await self.bot.send_message(member, 'Welcome {0.mention}!'.format(member))
		await self.setupNewProfile(member)
		
	async def on_member_remove(self, member):
		# await self.bot.send_message(member.server.default_channel, "Goodbye {0.mention}, we'll miss you!".format(member))
		await self.bot.say("Goodbye {0.mention}, we'll miss you!".format(member))

# This is called from load_extension in main bot client on_ready() event		
def setup(bot):
    bot.add_cog(ProfileCog(bot))
	
