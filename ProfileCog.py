import discord
from discord.ext import commands

class ProfileCog:
	def __init__(self, bot):
		self.bot = bot
		self.theProfiles = {}
    
	def debugShowProfiles(self):
		for key in self.theProfiles:
			print("{}".format(key))
			for skey, val in self.theProfiles[key].items():
				print("{}: {}".format(skey, val))
				
	async def showProfile(self, primarykey):
		em = discord.Embed(title="Profile", colour=discord.Colour.blue())
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
		
	@commands.group(pass_context=True)
	async def profile(self, ctx):
		if ctx.invoked_subcommand is None:
			# Display my own profile
			print("profile with no subcommand")
			#await showProfile(ctx.message.author)
			await self.showProfiles()

	@profile.command(pass_context=True, name="create")
	async def profile_create(self, ctx, name):
		# Currently this will overwrite any existing profile information! 
		newProfile = {}
		newProfile["Name"] = name
		newProfile["Nickname"] = "unknown"
		newProfile["Gender"] = "unknown"
		newProfile["Timezone"] = "unknown"
		newProfile["Rank"] = "unknown"
		newProfile["Role"] = "unknown"
		self.theProfiles[name] = newProfile

# This is called from load_extension in main bot client on_ready() event		
def setup(bot):
    bot.add_cog(ProfileCog(bot))
	
