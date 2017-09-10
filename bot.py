#!/usr/bin/python3
import sys
import asyncio
import discord
import importlib
import raidbot
from os.path import getmtime
import time
import tokens

client = discord.Client()
stime = time.time()

@client.event
@asyncio.coroutine
def on_ready():
    print("Logged in!")

@client.event
@asyncio.coroutine
def on_message(message):
    global stime
    if (getmtime("./raidbot.py") > stime):
        importlib.reload(raidbot)
        stime = time.time()
    yield from raidbot.parse(client, message)
    sys.stdout.flush()

if __name__ == "__main__":
    @asyncio.coroutine
    def main_task():
        yield from client.login(tokens.TOKEN) 
        yield from client.connect()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_task())
    except:
        loop.run_until_complete(client.logout())
        sys.stdout.flush()
    finally:
        loop.close()
