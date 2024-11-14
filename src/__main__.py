import discord, os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
DISCORD_BOT_API_KEY = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')
    await bot.change_presence(activity=discord.CustomActivity("!help for commands"))

if __name__ == "__main__":
    bot.run(DISCORD_BOT_API_KEY) 
