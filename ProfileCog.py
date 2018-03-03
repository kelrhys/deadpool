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
		
	async def on_member_join(self, member):
		await self.bot.send_message(member.server, "Welcome {0.mention}, would you like to introduce yourself?".format(member))
	
	async def joined_at(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.message.author

		await self.bot.say('{0} joined at {0.joined_at}'.format(member))
		
# This is called from load_extension in main bot client on_ready() event		
def setup(bot):
    bot.add_cog(ProfileCog(bot))
	
