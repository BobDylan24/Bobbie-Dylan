import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import config

intents = nextcord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready for use!")
    print("-----------------------")

testServerId = 1054368865628459079

@client.slash_command(name = "test", description = "Introduction to Slash Commands", guild_ids=[testServerId])
async def test(interaction: Interaction):
    await interaction.response.send_message("Testing!")

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(config.token)