import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(name="help")
    async def help(self,ctx):
        """ Help command to display commands """
        embed = discord.Embed( 
            title="LoserBot Commands",
            description="All Commands:",
            color=discord.Color.dark_gold()
        ) # Start an embed message

        embed.add_field(
            name="🚨 Loss Tracker 🚨",
            value="""
            `!loss @user` - Record a rage quit loss for specific user e.g. Mini aram
            `!losses @user` - WALL OF SHAME for specific user (note: minikillerj might have bugged it)
            `!losses ` - WALL OF SHAME for the server
            """,
            inline=False
        ) # Can maybe be written better later on 

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))