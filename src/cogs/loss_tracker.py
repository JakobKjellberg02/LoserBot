import discord, json, os
from discord.ext import commands
from datetime import datetime

from opgg.scraper import OPGGScraper

class LossTracker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        os.makedirs('data', exist_ok=True)
        self.losses_json = 'data/losses.json' # To save the data locally
        self.load_losses()
        self.scraper = OPGGScraper(headless=True)
    
    def __del__(self):
        # Ensure the scraper is closed when the cog is unloaded
        if hasattr(self, 'scraper'):
            self.scraper.close_driver()
    
    def load_losses(self):
        """ Load the losses from JSON """
        try:
            with open(self.losses_json, 'r') as f:
                self.losses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): # Create a new JSON if it doesn't exist
            self.losses = {}
            self.save_losses()
    
    def save_losses(self):
        """ le save le cool """
        with open(self.losses_json, 'w') as f:
            json.dump(self.losses, f, indent=4)
    
    @commands.command(name="loss")
    async def record_loss(self, ctx, member: discord.Member, *, summoner_name: str = None):
        """ Loss command from @user """
        member_id = str(member.id)
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if member_id not in self.losses:
            self.losses[member_id] = {
                "name": member.name,
                "total_losses": 0,
                "loss_dates": []
            } # Create the loser 
        
        kda_info = None
        kda_picture = None
        if summoner_name:
            print(summoner_name)
            kda_info = self.scraper.get_kda(summoner_name)
            kda_picture = self.scraper.get_picture(summoner_name)


        self.losses[member_id]["total_losses"] += 1
        self.losses[member_id]["loss_dates"].append(timestamp)
        self.save_losses()

        loss_count = self.losses[member_id]["total_losses"] # Gets user's losses
        
        embed = discord.Embed(
            title="RAGEQUIT ALERT!", 
            description=f"{member.mention} HAS LEFT ON A LOSS!\nHas been a pussy: {loss_count} times\n(Recorded on {timestamp})",
            color=discord.Color.red()
        ) # Embed message telling the whole server that @user is a pussy
        if kda_info:
            embed.add_field(
                name="Last Match Stats",
                value=f"KDA: {kda_info}\n",
                inline=False
            )
        if kda_picture:
            embed.set_image(url=kda_picture)
            await ctx.send(embed=embed)
        else:
            file = discord.File('resources/200w.gif', filename="200w.gif")  
            embed.set_image(url="attachment://200w.gif")    
            await ctx.send(file=file, embed=embed)
        
    @commands.command(name="losses")
    async def show_losses(self, ctx, *, member: discord.Member = None):
        """ WALL OF SHAME """ 
        if member: # If user @ an user
            member_id = str(member.id)

            if member_id not in self.losses: # You Either Die A Hero, Or You Live Long Enough To See Yourself Become The Villain
                await ctx.send(f"{member.name} is not a loser...")
                return

            loss_record = self.losses[member_id]

            embed = discord.Embed(
                title=f"WALL OF SHAME FOR {member.name}",
                color=discord.Color.red()
            ) # BEGIN THE SHAMING
            
            embed.add_field(
                name="Total Ragequits:",
                value=str(loss_record["total_losses"]),
                inline=False
            )

            recent_losses = loss_record["loss_dates"][-5:]  # 5 recent losses
            if recent_losses:
                embed.add_field(
                    name="Timestamp for Ragequits:",
                    value="\n".join(f"• {date}" for date in recent_losses),
                    inline=False
                )

            await ctx.send(embed=embed)
        else: 
            """ WALL OF SHAME FOR EVERYONE """
            sorted_losers = sorted(
                [(user_id, data) for user_id, data in self.losses.items()],
                key = lambda x: x[1]["total_losses"],
                reverse=True 
            ) # Sort by losers in descending order
            if not sorted_losers: # Impossible. Perhaps the Archives Are Incomplete.
                await ctx.send("No losers on this server...")
                return
            
            embed = discord.Embed(
                title="🏆 SERVER WALL OF SHAME 🏆",
                description=f"Ranking of the biggest noobs on {ctx.message.guild.name}",
                color=discord.Color.red()
            ) # BEGIN THE SHAMING

            medal_emojis = {
                1: "🥇",  
                2: "🥈",  
                3: "🥉"   
            } # Medal of honor

            # Iterate through the sorted losers and display them in the embed
            for rank, (user_id, data) in enumerate(sorted_losers, 1):
                try:
                    member = await ctx.guild.fetch_member(int(user_id))
                    name = member.mention
                except:
                    name = data["name"]  
                
                rank_display = medal_emojis.get(rank, f"#{rank}")
                embed.add_field(
                    name=f"#{rank_display}: {data['total_losses']} Ragequits",
                    value=f"{name}\nLast ragequit: {data['loss_dates'][-1]}",
                    inline=False
                )
            

            total_ragequits = sum(data["total_losses"] for _, data in sorted_losers)
            embed.set_footer(text=f"Total Server Ragequits: {total_ragequits}")
            
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LossTracker(bot))