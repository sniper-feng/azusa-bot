import json
import string
import time
from platform import system
from typing import re

from nonebot import on_command, on_regex
from nonebot.internal.adapter import event
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re
import os
from nonebot import require
from nonebot.plugin.on import on_fullmatch, on_regex, on_command

if system() == "Windows":
    blacklistPath = os.getcwd()+"\\prop\\blacklist.json"
else:
    blacklistPath = os.getcwd()+"/prop/blacklist.json"
cfg = on_command("botconfig")
if system() == "Windows":
    dinePath = os.getcwd()+"\\prop\\dine.json"
else:
    dinePath = os.getcwd()+"/prop/dine.json"

with open(dinePath, 'r', encoding="utf-8") as f:
    dineList = json.load(f)
shop_name = list(dineList.keys())
block_admin = [1332019406, 824889294, 2530342608]
super_admin = [1332019406]


@cfg.handle()
async def _(event: Event, message: Message = EventMessage()):
    with open(blacklistPath, "r", encoding="utf-8") as f:
        blackList = json.load(f)
    strings = event.get_plaintext().split(" ")
    # 格式 botconfig addmeal 一区/二区/机厅    吃什么
    #       0           1       2       3
    if strings[1] == "addmeal":
        qqid = int(event.get_user_id())
        if qqid in blackList:
            await cfg.send("宝宝，你也配用？")
            return
        if shop_name.count(strings[2]) == 1:
            await addmeal(strings[3], strings[2])
    if strings[1] == "removemeal":
        qqid = int(event.get_user_id())
        if qqid in blackList:
            await cfg.send("宝宝，你也配用？")
            return
        if shop_name.count(strings[2]) == 1:
            await removemeal(strings[3], strings[2])
    if strings[1] == "removeBlock":
        if int(event.get_user_id()) in block_admin:
            with open(blacklistPath, "r", encoding="utf-8") as f:
                blackList = json.load(f)
            blackList.remove(int(strings[2]))
            with open(blacklistPath, "w", encoding="utf-8") as bf:
                blstr = json.dumps(blackList)
                bf.write(blstr)
                return


# async def addmeal(meal: string, campus: int):
#     if system() == "Windows":
#         dinePath = os.getcwd()+"\\prop\\dine.json"
#     else:
#         dinePath = os.getcwd()+"/prop/dine.json"
#
#     with open(dinePath, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     if data['campus'][campus].count(meal) > 0:
#         await cfg.send("添加失败,这个菜已经存在了喵")
#     else:
#         data['campus'][campus].append(meal)
#         await cfg.send(f"{meal}已经加到{'一区' if campus == 0 else '二区'}了喵!")
#     with open(dinePath, 'w', encoding='utf-8') as f:
#         jsonStr = json.dumps(data)
#         jsonStr.encode('unicode_escape').decode("unicode-escape")
#         f.write(jsonStr)
#
#
# async def removemeal(meal: string, campus: int):
#     if system() == "Windows":
#         dinePath = os.getcwd()+"\\prop\\dine.json"
#     else:
#         dinePath = os.getcwd()+"/prop/dine.json"
#
#     with open(dinePath, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     if data['campus'][campus].count(meal) == 0:
#         await cfg.send("删除失败,菜单没有这个菜喵")
#     else:
#         data['campus'][campus].remove(meal)
#         await cfg.send(f"{meal}已经从{'一区' if campus == 0 else '二区'}删掉了喵!")
#
#     with open(dinePath, 'w', encoding='utf-8') as f:
#         jsonStr = json.dumps(data)
#         jsonStr.encode('unicode_escape').decode("unicode-escape")
#         f.write(jsonStr)
#

async def addmeal(meal: string, shopname: string):
    # do
    if system() == "Windows":
        dinePath = os.getcwd()+"\\prop\\dine.json"
    else:
        dinePath = os.getcwd()+"/prop/dine.json"

    with open(dinePath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data[shopname].count(meal) > 0:
        await cfg.send("添加失败,这个菜已经存在了喵")
    else:
        data[shopname].append(meal)
        await cfg.send(f"{meal}已经加到{shopname}了喵!")
    with open(dinePath, 'w', encoding='utf-8') as f:
        jsonStr = json.dumps(data)
        jsonStr.encode('unicode_escape').decode("unicode-escape")
        f.write(jsonStr)


async def removemeal(meal: string, shopname: string):
    # do
    if system() == "Windows":
        dinePath = os.getcwd()+"\\prop\\dine.json"
    else:
        dinePath = os.getcwd()+"/prop/dine.json"

    with open(dinePath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data[shopname].count(meal) == 0:
        await cfg.send("删除失败,菜单没有这个菜喵")
    else:
        data[shopname].remove(meal)
        await cfg.send(f"{meal}已经从{shopname}删掉了喵!")

    with open(dinePath, 'w', encoding='utf-8') as f:
        jsonStr = json.dumps(data)
        jsonStr.encode('unicode_escape').decode("unicode-escape")
        f.write(jsonStr)


block = on_command("拉黑")


@block.handle()
async def _(event: Event, message: Message = EventMessage()):
    if int(event.get_user_id()) in block_admin:
        msg = event.raw_message
        reg = r"^拉黑.*\[CQ:at,qq=([0-9]{1,})\].*"
        searchResult = re.search(reg, msg)

        if searchResult:
            qqid = int(searchResult.group(1))
            with open(blacklistPath, "r", encoding="utf-8") as f:
                blackList = json.load(f)
            blackList.append(qqid)
            blstr = json.dumps(blackList)
            with open(blacklistPath, "w", encoding="utf-8") as f:
                f.write(blstr)
            await block.send(f"恭喜QQ号为{qqid}的朋友获得至尊权限捏")
