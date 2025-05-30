from discord.ext import commands
import discord
from data_process import *
from random import *
import asyncio
import requests
from bs4 import BeautifulSoup
from pprint import pprint

gif_list = ["https://c.tenor.com/c3ks1DYnyr4AAAAC/anime-anime-girl.gif",
            "https://c.tenor.com/czmwFLhXJQ0AAAAC/anime-i-dont-know.gif",
            "https://c.tenor.com/ZINgFAwKh1QAAAAC/anime-love.gif",
            "https://c.tenor.com/Am61DGzxpGoAAAAC/anime-laughing.gif",
            "https://c.tenor.com/mkunLNebofwAAAAC/anime-headbang.gif",
            "https://c.tenor.com/H63Kb7qg8HoAAAAC/anime-chainsaw.gif",
            "https://c.tenor.com/0XNOlxxAFvcAAAAC/chuunibyou-anime.gif",
            "https://c.tenor.com/MyhZzxE8vsQAAAAC/cute-eat.gif",
            "https://c.tenor.com/FwQaJEGLhskAAAAC/cute-cat.gif",
            "https://c.tenor.com/io_R8mA_oUgAAAAC/satania-anime.gif",
            "https://c.tenor.com/jgFVzr3YeJwAAAAC/date-a-live-rage.gif",
            "https://c.tenor.com/rnhV3fu39f8AAAAC/eating-anime.gif",
            "https://c.tenor.com/UShPTojhFIkAAAAi/french-france-gun.gif",
            "https://c.tenor.com/wOCOTBGZJyEAAAAC/chikku-neesan-girl-hit-wall.gif",
            "https://c.tenor.com/FGLllO3BGxMAAAAC/baseball-body.gif",
            "https://c.tenor.com/TPaJW2RZyIYAAAAC/anime-dodge.gif"]


def get_anime_name(specify):
  possible = []
  if not specify:
    return choice(animes)

  specify_list = specify.lower().split()
  for g in genre:
    if all(ele in g for ele in specify_list):
      possible.append(animes[genre.index(g)])

  return choice(possible)


class utilities(commands.Cog):

  def __init__(self, client):
      self.client = client       

  @commands.command(aliases=['a'])  # random anime [optional genre]
  # @commands.cooldown(5, 30, commands.BucketType.user)
  async def anime(self, ctx, *, specify=""):
    anime = get_anime_name(specify)

    title = anime
    if(':' in anime and len(anime) > 30):
      title = anime[:anime.index(":")] + '\n' + ">" + anime[anime.index(":") + 1:]
    
    embed = discord.Embed(title=title, colour=discord.Colour.random())

    g_list = genre[animes.index(anime)]
    g_list.insert(4, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
    
    episode = "`Movie`" if ep[anime] == '0' else f"`{ep[anime]}`" + " episodes"
    ss = "not specified" if episode == "The movie" else season[anime]
    image = pic[anime]
    ranked = rank[anime]
    url = link[anime]

    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    embed.add_field(name="Genre", value=g_value, inline=False)
    embed.add_field(name="Season", value=f"`{ss}`", inline=True)
    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name=f"Ranked: #`{ranked}`", value=f"[Check it out!]({url})", inline=False)
    embed.set_image(url=image)
    
    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "📬")

    r_possible = []
    reaction_dict = {"Magic": "✨", "Action": "⚔", "Romance": "💗", "Supernatural": "🌪️", "Comedy": "😝",
                    "Drama": "🎭", "Kids": "🧒", "School": "🏫", "Fantasy": "🐉", "Cars": "🏎", "Sports": "🏀",
                    "Sci-fi": "🧪", "Game": "🎮", "Music": "🎶", "Superpower": "🦸", "Military": "🪖"}
    for g, r in reaction_dict.items():
      if g in g_value:
        r_possible.append(r)
    
    await discord.Message.add_reaction(msg, choice(r_possible)) if r_possible else await discord.Message.add_reaction(msg, "🔥")


  @commands.command(aliases=["ha"])
  @commands.is_nsfw()
  async def hentaianime(self, ctx):
    anime = choice(nsfw)
    embed = discord.Embed(title=f"{anime}", url=link[anime], colour=discord.Colour.random())

    episode = "`1` ep" if ep[anime] == '1' else f"`{ep[anime]}`" + " eps"
    ss = "not specified" if episode == "The movie" else season[anime]
    image = pic[anime]
    ranked = rank[anime]
    g_list = nsfw_genre[nsfw.index(anime)]
    g_list.insert(3, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

    embed.add_field(name="Genre", value=g_value, inline=False)
    embed.add_field(name="Season", value=f"`{ss}`", inline=True)
    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name=f"`{ranked}`", value="-" * 39, inline=False)

    embed.set_image(url=image)

    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "📬")
    await discord.Message.add_reaction(msg, "💪")
  

  @commands.command(aliases=['d'])  # random doujin [optional code]
  @commands.is_nsfw()
  async def doujin(self, ctx, code=""):
    code = code.strip()
    url = 'https://nhentai.net/g/' + code if code else "https://nhentai.net/random/"
    async with ctx.typing():
      request = requests.get(url).text
      soup = BeautifulSoup(request, 'html.parser')
      await asyncio.sleep(0.1)
    error = soup.find("div", class_="container error")
    if error:
      green = randint(0, 150)
      embed = discord.Embed(title="What's that sauce", 
                            description="> Fake sauce!", 
                            color=discord.Colour.from_rgb(224, green, 0))
      await ctx.send(embed=embed)
    else:
      pic = soup.find("img", class_="lazyload")['data-src']
      name_list = soup.find("h1", class_="title")
      name = [i.text for i in name_list]
      id = soup.find("h3", id="gallery_id").text
      embed = discord.Embed(title=name[0] + name[1] + name[2], 
                            url=f"https://nhentai.net/g/{id[1:]}",
                            color=discord.Colour.random())
      
      if code:
        embed.add_field(name=f"Sauce # `{code}` delivered!", value="Verified Sauce! Here you go.")
      else:
        embed.add_field(name=f"Random sauce => # `{id}` delivered!", value="`There you go!`")

      embed.set_image(url=pic)
      msg = await ctx.send(embed=embed)
      await discord.Message.add_reaction(msg, "📬")
      await discord.Message.add_reaction(msg, "👍🏻")


  @commands.command(aliases=['pf'])
  async def profile(self, ctx):
    profile = discord.Embed(color=discord.Colour.from_rgb(0, 255, 255))
    profile.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    await ctx.send(embed=profile)


  @commands.command()
  async def help(self, ctx): # show help menu
    client = self.client
    page= "Page"
    invite = "https://discord.com/oauth2/authorize?client_id=877425384864501760"
    me = "Naxocist#2982"

    p1 = discord.Embed(title="Just to mention the `SYMBOLS`...", color=discord.Colour.green())
    p1.set_thumbnail(url=choice(gif_list))
    p1.add_field(name="You can keep this anime in DM!", value="> 📬", inline=True)
    p1.add_field(name="Contact", value=f"[Invite!]({invite})\n`{me}` ", inline=False)
    p1.set_footer(text=page + f" 1/2")

    p2 = discord.Embed(title="Commands", color=discord.Colour.green())
    p2.set_thumbnail(url=choice(gif_list))
    p2.add_field(name=f"`.anime | .a [genre(s)]`", value="> Pick a random anime... \uD83D\uDCEC", inline=False)
    p2.set_footer(text=page + f" 2/2")

    async with ctx.typing():
      await asyncio.sleep(0.25)

    msg = await ctx.send(embed=p1)
    await discord.Message.add_reaction(msg, "◀")
    await discord.Message.add_reaction(msg, "▶")
    pages = [p1, p2]
    i = 0

    while True:
      tasks = [
        asyncio.create_task(client.wait_for("reaction_add", timeout=60, 
        check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["◀", "▶"])),
        
        asyncio.create_task(client.wait_for("raw_reaction_remove", timeout=60,
        check=lambda payload:payload.user_id == ctx.author.id and str(payload.emoji) in ["◀", "▶"]))
      ]

      # trigger if any completed
      done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

      finished = list(done)[0]

      for task in pending: # cancel untriggered task
        try:
          task.cancel()
        except asyncio.CancelError:
          pass
      try:
        react = finished.result()

      except asyncio.TimeoutError:  # TimeOut
        await msg.delete()
        await ctx.message.delete()
        break

      react = str(react[0]) if isinstance(react, tuple) else str(react.emoji)

      if react == "▶" and i != 1:
        i += 1
        await msg.edit(embed=pages[i])

      elif react == "◀" and i > 0:
        i -= 1
        await msg.edit(embed=pages[i])


            
async def setup(client):
  await client.add_cog(utilities(client))