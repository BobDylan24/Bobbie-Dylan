import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import Member
from nextcord import SlashOption
from typing import Optional
from nextcord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime

date = datetime.today()

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    
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

def setup(client):
    client.add_cog(Admin(client))