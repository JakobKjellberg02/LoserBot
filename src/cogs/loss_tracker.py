import discord, json, os
from discord.ext import commands
from datetime import datetime

class LossTracker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        os.makedirs('data', exist_ok=True)
        self.losses_json = 'data/losses.json'
        self.load_losses()
    
    def load_losses(self):
        try:
            with open(self.losses_json, 'r') as f:
                self.losses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.losses = {}
            self.save_losses()
    
    def save_losses(self):
        with open(self.losses_json, 'w') as f:
            json.dump(self.losses, f, indent=4)
    
    @commands.command(name="loss")
    async def record_loss(self, ctx, member: discord.Member):
        member_id = str(member.id)
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if member_id not in self.losses:
            self.losses[member_id] = {
                "name": member.name,
                "total_losses": 0,
                "loss_dates": []
            }
        
        self.losses[member_id]["total_losses"] += 1
        self.losses[member_id]["loss_dates"].append(timestamp)
        self.save_losses()

        loss_count = self.losses[member_id]["total_losses"]
        
        embed = discord.Embed(
            title="RAGEQUIT ALERT!", 
            description=f"{member.mention} HAS LEFT ON A LOSS!\nHas been a pussy: {loss_count} times\n(Recorded on {timestamp})",
            color=discord.Color.red()
        )
        file = discord.File('resources/200w.gif', filename="200w.gif")
        embed.set_image(url="attachment://200w.gif")

        await ctx.send(file=file, embed=embed)
        
    @commands.command(name="losses")
    async def show_losses(self, ctx, member: discord.Member):
        member_id = str(member.id)

        if member_id not in self.losses:
            await ctx.send(f"{member.name} is not a loser...")
            return

        loss_record = self.losses[member_id]

        embed = discord.Embed(
            title=f"WALL OF SHAME FOR {member.name}",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Total Ragequits:",
            value=str(loss_record["total_losses"]),
            inline=False
        )

        recent_losses = loss_record["loss_dates"][-5:]  
        if recent_losses:
            embed.add_field(
                name="Timestamp for Ragequits:",
                value="\n".join(f"• {date}" for date in recent_losses),
                inline=False
            )

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(LossTracker(bot))