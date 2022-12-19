import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import config
from utils.mongo import Document
import motor.motor_asyncio
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)

intents = nextcord.Intents.all()
intents.members = True

client = commands.client(command_prefix = '!', intents=intents)

client.connection_url = config.mongo
client.DEFAULTPREFIX = "!"
client.blacklisted_users = []
client.muted_users = []

@client.event
async def on_ready():
    print("The client is now ready for use!")
    print("-----------------------")
    await client.change_presence(activity=nextcord.Game(name="with people."))
    for document in await client.config.get_all():
        print(document)

    currentMutes = await client.mutes.get_all()
    for mute in currentMutes:
        client.muted_users[mute["_id"]] = mute

    print(client.muted_users)

    print("Initialized Database\n-----")

@client.event
async def on_message(message):
    if message.author.client:
        return

    if message.author.id in client.blacklisted_users:
        return
    
    if message.content.startswith(f"<@!{client.user.id}>") and len(message.content) == len(
        f"<@!{client.user.id}>"
    ):
        await message.channel.send(f"My prefix here is `!`", delete_after=15)

    await client.process_commands(message)

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
    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(client.connection.url))
    client.db = client.mongo["database"]
    client.config = Document(client.db, "config")
    client.mutes = Document(client.db, "mutes")
    client.warns = Document(client.db, "warns")
    client.invites = Document(client.db, "invites")
    client.command_usage = Document(client.db, "command_usage")
    client.reaction_roles = Document(client.db, "reaction_roles")

client.run(config.token)