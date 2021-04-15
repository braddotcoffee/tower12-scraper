import json
from discord import User
from discord.ext import commands, tasks
from discord.ext.commands import Context
from lib.grabber import grab_floorplans
from lib.parser import parse_apartments
from typing import List
from lib.apartment import Apartment

client = commands.Bot(description="Tower12 Scraper Bot", command_prefix="!")
user_id = ""
SECONDS_IN_DAY = 86400
existing_apartments = set()
no_new_apartments_message = "The Tower isn't ready for your Bonanno yet."


def chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def build_messages(apartments: List[Apartment], no_fit_msg: str) -> str:
    if len(apartments) > 0:
        for apt_chunk in chunk(apartments, 5):
            msg = ""
            for apt in apt_chunk:
                msg += apt.to_message()
            yield msg
    else:
        yield no_fit_msg


def get_new_apartments() -> List[Apartment]:
    global existing_apartments
    print("I'll scrape the Tower for you, Code Daddy")
    apartments = parse_apartments(grab_floorplans())
    new_apartments = list(
        filter(lambda apt: apt not in existing_apartments, apartments)
    )
    existing_apartments.update(new_apartments)
    return new_apartments


@tasks.loop(hours=24)
async def check_loop(user: User):
    global existing_apartments
    new_apartments = get_new_apartments()
    for msg in build_messages(new_apartments, no_new_apartments_message):
        await user.send(msg)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    user = await client.fetch_user(user_id)
    check_loop.start(user)


@client.command(name="check")
async def check_apts(ctx: Context):
    global existing_apartments
    new_apartments = get_new_apartments()
    for msg in build_messages(new_apartments, no_new_apartments_message):
        await ctx.send(msg)


@client.command(name="fit")
async def apartments_fit_criteria(ctx: Context):
    apartments = parse_apartments(grab_floorplans())
    apt_fit = list()
    for apt in apartments:
        if apt.floor < 20:
            continue
        if "F" not in apt.floorplan:
            continue
        apt_fit.append(apt)
    for msg in build_messages(apt_fit, "These beans don't fit your standards, Mr. Lord Coffee, Sir"):
        await ctx.send(msg)


def main():
    global user_id
    with open("secrets/discord.json") as f:
        json_data = json.load(f)
    user_id = json_data["userId"]
    client.run(json_data["botToken"])


if __name__ == "__main__":
    main()
