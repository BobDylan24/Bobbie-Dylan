import nextcord
from nextcord.ext import commands
from datetime import datetime
date = datetime.today()
class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member : nextcord.Member):
        channel = self.client.get_channel(1054368866689617990)
        embed = nextcord.Embed(title="New Member!", description="A new member has joined the server!", color=nextcord.Color.green())
        embed.add_field(name="Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name="Member Creation Date", value=f"{member.created_at}", inline=False)
        embed.add_field(name="Join Date", value=f"{date}", inline=False)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member : nextcord.Member):
        channel = self.client.get_channel(1054368866689617990)
        embed = nextcord.Embed(title="Member Left", description="A member hsa left the server", color=nextcord.Color.red())
        embed.add_field(name="Member Name", value=f"{member.name}", inline=False)
        embed.add_field(name="Member Creation Date", value=f"{member.created_at}", inline=False)
        embed.add_field(name="Join Date", value=f"{member.joined_at}", inline=False)
        await channel.send(embed = embed)

def setup(client):
    client.add_cog(Events(client))