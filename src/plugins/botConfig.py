import json
import string
import time
from platform import system
from typing import re

from nonebot import on_command, on_regex
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re

from nonebot import require
from nonebot.plugin.on import on_fullmatch, on_regex, on_command

cfg = on_command("botconfig")


@cfg.handle()
async def _(event: Event, message: Message = EventMessage()):
    strings = event.get_plaintext().split(" ")
    # 格式 botconfig addmeal 一区/二区    吃什么
    #       0           1       2       3
    if strings[1] == "addmeal":
        if strings[2] == "一区":
            await addmeal(strings[3],0)
        if strings[2] == "二区":
            await addmeal(strings[3], 1)
    if strings[1] == "removemeal":
        if strings[2] == "一区":
            await removemeal(strings[3],0)
        if strings[2] == "二区":
            await removemeal(strings[3], 1)


async def addmeal(meal: string,campus:int):
    if system() == "Windows":
        dinePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\dine.json"
    else:
        dinePath = "/home/sniperpigeon/bot/azusa-bot/prop/dine.json"

    with open(dinePath, 'r',encoding='utf-8') as f:
        data = json.load(f)

    if data['campus'][campus].count(meal) > 0:
        await cfg.send("添加失败,这个菜已经存在了喵")
    else:
        data['campus'][campus].append(meal)
        await cfg.send(f"{meal}已经加到{'一区' if campus ==0 else '二区'}了喵!")
    with open(dinePath, 'r+',encoding='utf-8') as f:
        jsonStr = json.dumps(data)
        jsonStr.encode('unicode_escape').decode("unicode-escape")
        f.write(jsonStr)

async def removemeal(meal: string,campus:int):
    if system() == "Windows":
        dinePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\dine.json"
    else:
        dinePath = "/home/sniperpigeon/bot/azusa-bot/prop/dine.json"

    with open(dinePath, 'r',encoding='utf-8') as f:
        data = json.load(f)

    if data['campus'][campus].count(meal) == 0:
        await cfg.send("删除失败,菜单没有这个菜喵")
    else:
        data['campus'][campus].remove(meal)
        await cfg.send(f"{meal}已经从{'一区' if campus ==0 else '二区'}删掉了喵!")

    with open(dinePath, 'r+',encoding='utf-8') as f:
        jsonStr = json.dumps(data)
        jsonStr.encode('unicode_escape').decode("unicode-escape")
        f.write(jsonStr)

