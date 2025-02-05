import os

import discord
from discord import AppCommandType, app_commands
from discord.ext import commands
from dotenv import load_dotenv

from server import MinecraftServer

TOKEN = ""
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Create a single instance of MinecraftServer
mc_server = MinecraftServer()


async def sync_commands() -> list[AppCommandType]:
    """Syncs slash commands

    Returns:
        list[AppCommandType]: the list of all commands synced
    """
    sync_commands = await tree.sync()
    return sync_commands


@client.event
async def on_ready():
    # when commands need to be synced
    # await print(sync_commands())
    print(f"Logged in as {client.user}")


@tree.command(
    name="start",
    description="Start the minecraft server",
)
async def start(interaction: discord.Interaction):
    """Start the Minecraft server"""
    response = mc_server.start_server()
    await interaction.response.send_message(response)


@tree.command(name="stop", description="Stops the minecraft server")
async def stop(interaction: discord.Interaction):
    """Stop the Minecraft server"""
    response = mc_server.stop_server()
    await interaction.response.send_message(response)


@tree.command(name="status", description="Display the server's CPU and RAM usage")
async def status(interaction: discord.Interaction):
    """Check the server's CPU and RAM usage"""
    response = mc_server.get_server_status()
    await interaction.response.send_message(response)


@tree.command(name="shutdown", description="Shutdown the bot")
@commands.is_owner()
async def shutdown(interaction: discord.Interaction):
    """Handles safe shutdown when bot is interrupted"""
    print("\nShutting down bot...")
    if mc_server.is_running():
        print("Stopping Minecraft server before exit...")
        mc_server.stop_server()
    await client.close()
    print("Bot shut down successfully.")


def handle_exit():
    """Stops the bot and server on Ctrl+C"""
    mc_server.stop_server()
    client.close()


def main() -> None:
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    client.run(TOKEN)


# Run the bot
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Shutting down safely.")
        handle_exit()
        exit()
