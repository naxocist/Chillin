import discord
from discord.ext import commands


class events(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("Bot is ready!")

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):  # check reaction
    if user == self.client.user:
      return
    if reaction.emoji == "📬":
      await reaction.message.add_reaction("✅")
      await user.send(embed=reaction.message.embeds[0])

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
      return
        
    elif isinstance(error, commands.MissingPermissions):
      permission_warn = "You're not allowed to do that!"
      await ctx.send(embed=discord.Embed(title=permission_warn, color=discord.Colour.red()))

    elif isinstance(error, commands.errors.CommandOnCooldown):
      cooldown_warn = f"`Cooling down! try again in {int(error.retry_after)}s.`"
      await ctx.send(cooldown_warn)
        
    else:
      raise error.original


async def setup(client):
  await client.add_cog(events(client))