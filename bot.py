import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import db

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

class VolunteerBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self.initial_cogs = ["cogs.task_cog"]
        self.guild = discord.Object(id=GUILD_ID) if GUILD_ID else None

    async def setup_hook(self):
        for cog in self.initial_cogs:
            await self.load_extension(cog)
        
        if self.guild:
            self.tree.copy_global_to(guild=self.guild)
            await self.tree.sync(guild=self.guild)
        else:
            await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("Bot is operational.")

def main():
    if not DISCORD_TOKEN or not GUILD_ID:
        print("Error: DISCORD_TOKEN or GUILD_ID is not defined in the .env file.")
        return

    db.initialize_database()
    bot = VolunteerBot()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
