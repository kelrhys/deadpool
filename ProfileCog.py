import discord
from discord.ext import commands

class ProfileCog:
	def __init__(self, bot):
		self.bot = bot
		self.theProfiles = {}
		self.adminSettings = {}    
				
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

	async def showSettings(self, dict, server):
		em = discord.Embed(title="{} Configuration Settings".format(server.name), colour=discord.Colour.blue())
		for key,val in dict.items():
			print("{}: {}".format(key, val))
			em.add_field(name=key, value=val)
		await self.bot.say(embed=em)
		
	def checkAdmin(ctx):
		print("checkAdmin - admin: ", ctx.message.author.top_role.permissions.administrator)
		return ctx.message.author.top_role.permissions.administrator
		
	@commands.check(checkAdmin)
	@commands.group(pass_context=True)
	async def admin(self, ctx):
		if ctx.invoked_subcommand is None:
			server = ctx.message.author.server
			server_id = server.id
			print("admin with no subcommand, display admin settings for: {}".format(server))

			# Display admin settings for server
			await self.showSettings(self.adminSettings[server_id], server)

	@admin.command(pass_context=True, name="create")
	async def admin_create(self, ctx):
		admin = ctx.message.author
		server = ctx.message.author.server
		server_id = server.id
		
		await self.bot.send_message(admin, 'Verified Administrator status, commencing creation of organization configuration settings. Please note that the current settings will be overwritten. Type yes to continue, or no to cancel.')
		response = await self.bot.wait_for_message(timeout=20, author=admin)
		if response is None or "no" in response.content.lower():
			return
		
		self.adminSettings[server_id] = {}
		serverSettings = self.adminSettings[server_id]

		def setKey(msg, key):
			if msg is None:
				serverSettings[key] = "None"
			else:
				serverSettings[key] = msg.content
					
		await self.bot.send_message(admin, 'What is your organization type? For example: clan, city, guild, house?')
		orgType = await self.bot.wait_for_message(timeout=20,author=admin)
		setKey(orgType,"OrgType")
		if "None" in serverSettings["OrgType"]:
			serverSettings["OrgType"] = "organization"
			
		await self.bot.send_message(admin, 'I have set your OrgType to {}. What is the default Role for new members?'.format(serverSettings["OrgType"]))
		role = await self.bot.wait_for_message(timeout=20,author=admin)
		setKey(role,"DefaultRole")
		await self.bot.send_message(admin, 'Great, I have set the default role for new members to {}. What channel should new users be referred to for help getting started?'.format(serverSettings["DefaultRole"]))
		channel = await self.bot.wait_for_message(timeout=20,author=admin)
		setKey(channel,"HelpChannel")
		await self.bot.send_message(admin, 'HelpChannel has been set to {}.'.format(serverSettings["HelpChannel"]))
		await self.bot.send_message(admin, 'Finally, who should new members contact for help if needed?')
		helpContact = await self.bot.wait_for_message(timeout=20,author=admin)
		setKey(helpContact,"HelpContact")
		await self.bot.send_message(admin, 'HelpContact has been set to {}. Configuration complete!'.format(serverSettings["HelpContact"]))
		
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
		server = member.server
		server_id = member.server.id
		serverSettings = self.adminSettings[server_id]
		
		newProfile = {}
		newProfile["Name"] = member.name
		newProfile["Nickname"] = member.nick
		newProfile["role"] = member.top_role
		newProfile["IsAdmin"] = member.top_role.permissions.administrator
		newProfile["Server"] = server.name
		newProfile["ServerID"] = server_id
		
		def setProfileKey(msg, key):
			if msg is None:
				newProfile[key] = "no response"
			else:
				newProfile[key] = msg.content
				
		await self.bot.send_message(member, 'Let\'s get you setup with the {}! First, what is your geographical timezone?'.format(serverSettings["OrgType"]))
		timezone = await self.bot.wait_for_message(timeout=20,author=member)
		setProfileKey(timezone,"Timezone")
		await self.bot.send_message(member, 'I have set your Timezone to {}. What is your current might/level/rank in the game?'.format(newProfile["Timezone"]))
		rank = await self.bot.wait_for_message(timeout=20,author=member)
		setProfileKey(rank,"Rank")
		await self.bot.send_message(member, 'Great, I have set your Rank to {}. Finally, as what gender would you prefer to be known?'.format(newProfile["Rank"]))
		gender = await self.bot.wait_for_message(timeout=20,author=member)
		setProfileKey(gender,"Gender")
		await self.bot.send_message(member, 'Your gender has been set to {}. The Inquisition is over!'.format(newProfile["Gender"]))

		role = discord.utils.find(lambda r: r.name == serverSettings["DefaultRole"], server.roles)
		if role is None:
			await self.bot.send_message(member, 'Could not set your Discord Role to {} because it does not exist. Contact {} for help setting your role.'.format(serverSettings["DefaultRole"], serverSettings["HelpContact"]))
		else:
			await self.bot.add_roles(member, role)
			newProfile["Role"] = serverSettings["DefaultRole"]

			await self.bot.send_message(member, 'I have set your Discord Role to {} according to the {}\'s leaders.'.format(newProfile["Role"], serverSettings["OrgType"]))

		self.theProfiles[member] = newProfile
		await self.bot.send_message(member, 'Please read channel {} for help getting started. Good luck, my friend!'.format(serverSettings["HelpChannel"]))
		
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
			await self.bot.send_message(member, 'Welcome to {0.server.name}, {0.mention}!'.format(member))
			await self.setupNewProfile(member)
		
	async def on_member_join(self, member):
		await self.bot.send_message(member, 'Welcome to {0.server.name}, {0.mention}!'.format(member))
		await self.setupNewProfile(member)
		
	async def on_member_remove(self, member):
		# await self.bot.send_message(member.server.default_channel, "Goodbye {0.mention}, we'll miss you!".format(member))
		await self.bot.say("Goodbye {0.mention}, we'll miss you!".format(member))

# This is called from load_extension in main bot client on_ready() event		
def setup(bot):
    bot.add_cog(ProfileCog(bot))
	
