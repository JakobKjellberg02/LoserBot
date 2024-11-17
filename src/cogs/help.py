import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(name="help")
    async def help(self,ctx):
        embed = discord.Embed(
            title="LoserBot Commands",
            description="All Commands:",
            color=discord.Color.dark_gold()
        )

        embed.add_field(
            name="🚨 Loss Tracker 🚨",
            value="""
            `!loss @user` - Record a rage quit loss e.g. Mini aram
            `!losses @user` - WALL OF SHAME (note: minikillerj might have bugged it)
            """,
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))