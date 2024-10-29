import os
import tempfile
from typing import IO
import urllib
from urllib.request import urlretrieve

import discord
from dotenv import load_dotenv
from petpetgif import petpet

load_dotenv()

bot_token = os.environ.get("bot_token")
owner_id = int(os.environ.get("owner_id", "0"))

bot = discord.Bot(owner_id=owner_id)

opener = urllib.request.build_opener()
opener.addheaders = [("User-agent", "curl/8.10.1")]
urllib.request.install_opener(opener)


async def pohladit(ctx: discord.ApplicationContext, file: IO[bytes]):
    with tempfile.NamedTemporaryFile(suffix=".gif") as petGif:
        petpet.make(file, petGif.file)
        petGif.flush()
        file = discord.File(petGif.name, "hladihladi.gif")
        await ctx.respond(file=file)


async def pohladit_uzivatele(
    ctx: discord.ApplicationContext, user: discord.User = None
):
    if user is None:
        user = ctx.user

    if user.avatar is None:
        await ctx.respond(
            "Tento uživatel nemá profilovku, takže nemám koho hladit :(", ephemeral=True
        )
        return

    with tempfile.NamedTemporaryFile(suffix=".png") as pfp:
        await user.avatar.save(pfp.file)
        pfp.flush()
        await pohladit(ctx, pfp)


async def pohladit_obrazek(ctx: discord.ApplicationContext, url: str):
    with tempfile.NamedTemporaryFile() as pfp:
        urlretrieve(url, pfp.name)
        await pohladit(ctx, pfp)


@bot.slash_command()
async def hladihladi(
    ctx: discord.ApplicationContext,
    user: discord.Option(
        discord.User, description="Koho chceš pohladit, šupáku?"
    ) = None,
    image: discord.Option(str, description="Nebo je libo obrázek?") = None,
):
    if image:
        await pohladit_obrazek(ctx, image)
    else:
        await pohladit_uzivatele(ctx, user)


@bot.user_command(name="Chci ho poňuňat.")
async def hladihladi_uzivatele(ctx: discord.ApplicationContext, user: discord.User):
    await pohladit_uzivatele(ctx, user)


bot.run(bot_token)
