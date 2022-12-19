import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import Member
from nextcord import SlashOption
from typing import Optional
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.ext import tasks
from datetime import datetime
import re
from copy import deepcopy
import asyncio
from dateutil.relativedelta import relativedelta
import utils.json_loader

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

date = datetime.today()

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f"{value} is an invalid time key h|m|s|d are valid arguments")
            except ValueError:
                raise commands.BadArgument(f"{key} is no a number!")
        return round(time)

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mute_task = self.check_current_mutes.start()

    def cog_unload(self):
        self.mute_task.cancel()
    
    @tasks.loop(minutes=5)
    async def check_current_mutes(self):
        currentTime = datetime.now()
        mutes = deepcopy(self.client.muted_users)
        for key, value in mutes.items():
            if value['muteDuration'] is None:
                continue
            
            unmuteTime = value['mutedAt'] + relativedelta(seconds=value['muteDuration'])
            if currentTime >= unmuteTime:
                guild = self.client.get_guild(value['guildId'])
                member = guild.get_member(value['_id'])

                role = nextcord.utils.get(guild.roles, name="Muted")
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"Unmuted: {member.display_name}")
                
                await self.client.mutes.delete(member.id)
                try:
                    self.client.muted_users.pop(member.id)
                except KeyError:
                    pass
    
    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.bot.wait_until_ready()

    
    testServerId = 1054368865628459079
    
    @nextcord.slash_command(name = "kick", description="Kicks a member from the server.", guild_ids=[testServerId])
    async def kick(self, interaction : Interaction, member: Optional[Member] = SlashOption(description="Put the username of the user you are trying to kick.", required=True), reason: Optional[str] = SlashOption(description="Put the reason why you are kicking the user.", required=True)):
        embed = nextcord.Embed(title = "Member Kicked", description="Successfully kicked the member from the server!", color=nextcord.Color.green())
        embed.add_field(name = "Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}")
        await interaction.response.send_message(embed = embed)
        embed = nextcord.Embed(title = "Kicked", description=f"You have been kicked from {interaction.guild.name}", color=nextcord.Color.red())
        embed.add_field(name = "Moderator Name", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}", inline=False)
        embed.add_field(name = "Date", value=f"{date}", inline=False)
        await member.send(embed = embed)
        await member.kick()


    @nextcord.slash_command(name = "ban", description="Bans a member from the server.", guild_ids=[testServerId])
    async def ban(self, interaction : Interaction, member: Optional[Member] = SlashOption(description="Put the username of the user you are trying to ban.", required=True), reason: Optional[str] = SlashOption(description="Put the reason why you are banning the user.", required=True)):
        embed = nextcord.Embed(title = "Member Banned", description="Successfully banned the member from the server!", color=nextcord.Color.green())
        embed.add_field(name = "Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}")
        await interaction.response.send_message(embed = embed)
        embed = nextcord.Embed(title = "Banned", description=f"You have been banned from {interaction.guild.name}", color=nextcord.Color.red())
        embed.add_field(name = "Moderator Name", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}", inline=False)
        embed.add_field(name = "Date", value=f"{date}", inline=False)
        await member.send(embed = embed)
        await member.ban(reason = reason)

    @nextcord.slash_command(name = "unban", description="Unbans a member from the server.", guild_ids=[testServerId])
    async def unban(self, interaction: Interaction, member: Optional[str] = SlashOption(description="Put the username and the discriminator of the user you are trying to unban.", required=True)):
        banned_users = interaction.guild.bans()
        member_name, member_discriminator = member.split("#")

        async for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                embed = nextcord.Embed(title="Unbanned Member", description="Successfully unbanned the member from the server!", color=nextcord.Color.green())
                embed.add_field(name="Member Unbanned", value=f"{member}", inline=False)
                embed.add_field(name = "Moderator Name", value=f"{interaction.user.mention}", inline=False)
                await interaction.response.send_message(embed = embed)
    
    #@nextcord.slash_command(name = "mute", description="Mutes a member from the server.", guild_ids=[testServerId])
    #async def mute(self, interaction : Interaction, time: Optional[str] = SlashOption(description="Put in the time that you want to mute the user.", required=True), member: Optional[Member] = SlashOption(description="Put the username of the user you are trying to mute", required=True), reason: Optional[str] = SlashOption(description="Put the reason why you are muting the user.", required=True)):
        #role = interaction.guild.get_role(1054423231026708661)
        #if not role:
            #await interaction.response.send_message("No muted rolew as found! Please create one called `Muted`")
            #return
        
        #try:
            #if self.client.muted_users[member.id]:
                #await interaction.response.send_message("This user is already muted.")
                #return
        #except KeyError:
            #pass

        #data = {
            #'_id': member.id,
            #'mutedAt': datetime.now(),
            #'muteDuration': time or None,
            #'mutedBy': interaction.user.id,
            #'guildId': interaction.guild.id
        #}
        #await self.client.mutes.upsert(data)
        #self.client.muted_users[member.id] = data

        #await member.add_roles(role)

        #if not time:
            #await interaction.response.send_message(f"Muted {member.display_name}")
        #else:
            #minutes, seconds = divmod(time, 60)
            #hours, minutes = divmod(minutes, 60)
            #if int(hours):
                #await interaction.response.send_message(f"Muted {member.display_name} for {hours} hours, {minutes} minutes and {seconds} seconds.")
            #elif int(minutes):
                #await interaction.response.send_message(f"Muted {member.display_name} for {minutes} minutes and {seconds} seconds")
            #elif int(seconds):
                #await interaction.response.send_message(f"Muted {member.display_name} for {seconds} seconds")
        #if time and time < 300:
            #await asyncio.sleep(time)

            #if role in member.roles:
                #await member.remove_roles(role)
                #await interaction.response.send_message(f"Unmuted `{member.display_name}")
            
            #await self.client.mutes.delete(member.id)
            #try:
                #self.client.muted_users.pop(member.id)
            #except KeyError:
                #pass

    @nextcord.slash_command(name = "blacklist", description="Blacklists a user from the bot. OWNER ONLY COMMAND", guild_ids=[testServerId])
    async def blacklist(self, interaction : Interaction, member: Optional[Member] = SlashOption(description="Put the username that you want to blacklist.", required=True)):
        if interaction.user.id == "866285734808780812":
            await interaction.response.send_message("You are not the owner of the bot. So you may not run this command.")
            return
        
        self.client.blacklisted_users.append(member.id)
        data = utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].append(member.id)
        utils.json_loader.write_json(data, "blacklist")
        await interaction.response.send_message(f"Hey, I have blacklisted {member.name} for you.")
    
    @commands.command(name = "kick", description="Kicks a member from the server")
    async def kick_prefix(self, ctx, member : nextcord.Member=None, *, reason=None):
        embed = nextcord.Embed(title = "Member Kicked", description="Successfully kicked the member from the server!", color=nextcord.Color.green())
        embed.add_field(name = "Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}")
        await ctx.send(embed = embed)
        embed = nextcord.Embed(title = "Kicked", description=f"You have been kicked from {ctx.guild.name}", color=nextcord.Color.red())
        embed.add_field(name = "Moderator Name", value=f"{ctx.author.name}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}", inline=False)
        embed.add_field(name = "Date", value=f"{date}", inline=False)
        await member.send(embed = embed)
        await member.kick()

    @commands.command(name = "ban", description="Bans a member from the server.")
    async def ban_prefix(self, ctx, member: nextcord.Member=None, *, reason=None):
        embed = nextcord.Embed(title = "Member Banned", description="Successfully banned the member from the server!", color=nextcord.Color.green())
        embed.add_field(name = "Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}")
        await ctx.send(embed = embed)
        embed = nextcord.Embed(title = "Banned", description=f"You have been banned from {ctx.guild.name}", color=nextcord.Color.red())
        embed.add_field(name = "Moderator Name", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name = "Reason", value=f"{reason}", inline=False)
        embed.add_field(name = "Date", value=f"{date}", inline=False)
        await member.send(embed = embed)
        await member.ban(reason = reason)

    @commands.command(name = "unban", description="Unbans a member from the server.")
    async def unban_prefix(self, ctx, member : nextcord.Member=None, *, reason=None):
        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        async for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = nextcord.Embed(title="Unbanned Member", description="Successfully unbanned the member from the server!", color=nextcord.Color.green())
                embed.add_field(name="Member Unbanned", value=f"{member}", inline=False)
                embed.add_field(name = "Moderator Name", value=f"{ctx.user.mention}", inline=False)
                await ctx.response.send_message(embed = embed)

def setup(client):
    client.add_cog(Admin(client))