import json
import string
import time

import nonebot
from nonebot import on_command, on_regex
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PrivateMessageEvent

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re

from nonebot import require
from nonebot.plugin.on import on_fullmatch, on_regex, on_command

SELF_ID = 2284891492

if system() == "Windows":
    quotePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\quote.json"
else:
    quotePath = "/home/sniperpigeon/bot/azusa-bot/prop/quote.json"
if system() == "Windows":
    aliasPath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\alias.json"
else:
    aliasPath = "/home/sniperpigeon/bot/azusa-bot/prop/alias.json"
if system() == "Windows":
    idPath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\QQID.json"
else:
    idPath = "/home/sniperpigeon/bot/azusa-bot/prop/QQID.json"

addQuote = on_command("入典")


@addQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        quoteList[name].append(strs[2])
        with open(quotePath, 'w', encoding="utf-8") as f:
            jsonStr = json.dumps(quoteList)
            jsonStr.encode('unicode_escape').decode("unicode-escape")
            f.write(jsonStr)
    else:
        await addQuote.send("这个人不在名人堂呢")


# 加入名人堂 车乃 alias=何大东
addPerson = on_command("加入名人堂")


@addPerson.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    # 普通添加
    if len(strs) == 2:
        if strs[1] in quoteList.keys():
            await addQuote.send("此人已在名人堂")
        else:
            quoteList[strs[1]] = []
            with open(quotePath, 'w', encoding="utf-8") as f:
                jsonStr = json.dumps(quoteList)
                jsonStr.encode('unicode_escape').decode("unicode-escape")
                f.write(jsonStr)
    else:
        # 添加别名
        alias = strs[2][6:]  # 别名
        if getNameFromList(strs[1], quoteList.keys()) is None:
            await addQuote.send("此人不在名人堂")
        else:
            trueName = getNameFromList(strs[1], quoteList.keys())
            with open(aliasPath, 'r', encoding="utf-8") as f:
                aliasList = json.load(f)
            aliasList[alias] = trueName
            with open(aliasPath, 'w', encoding="utf-8") as f:
                jsonStr = json.dumps(aliasList)
                jsonStr.encode('unicode_escape').decode("unicode-escape")
                f.write(jsonStr)


checkPerson = on_fullmatch("查看名人堂")


@checkPerson.handle()
async def _(event: Event, message: Message = EventMessage()):
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    sendstring = "目前的名人堂内有以下人士:\n"
    for key in quoteList.keys():
        sendstring += key + "\n"
    await checkPerson.send(sendstring)


sendQuote = on_command("爆典")


@sendQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        quotes = quoteList[name]
        if len(quotes) == 0:
            await addQuote.send("这个人没有典呢")
        else:
            index = random.randint(0, len(quotes) - 1)
            quote = quotes[index]
            await sendQuote.send(f"\"{quote}\"\n\n      ————{name}")
    else:
        await addQuote.send("此人不在名人堂")


sendQuoteGroup = on_command("十连爆典")


@sendQuoteGroup.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        quotes = quoteList[name]

        if len(quotes) == 0:
            await sendQuoteGroup.send("这个人没有典呢")
        else:
            with open(idPath, 'r', encoding="utf-8") as f:
                idList = json.load(f)
            segments = []
            for i in range(0, 10):
                index = random.randint(0, len(quotes) - 1)
                if name in idList:
                    qqid = idList[name]
                else:
                    qqid = event.self_id
                quote = quotes[index]
                quoteStr = f"\"{quote}\"\n\n      ————{name}"
                segments.append(MessageSegment(
                    "node",
                    {
                        "uin": str(qqid),
                        "name": "听"+name+"说：",
                        "content": quoteStr
                    }
                )
                )
            bot = nonebot.get_bot()
            is_private = isinstance(event, PrivateMessageEvent)
            if (is_private):
                await bot.call_api(
                    "send_private_forward_msg", user_id=event.user_id, messages=segments
                )
            else:
                await bot.call_api(
                    "send_group_forward_msg", group_id=event.group_id, messages=segments
                )
    else:
        await sendQuoteGroup.send("此人不在名人堂")

sendAllQuote = on_command("allin爆典")


@sendAllQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        quotes = quoteList[name]
        if len(quotes) == 0:
            await sendQuoteGroup.send("这个人没有典呢")
        else:
            with open(idPath, 'r', encoding="utf-8") as f:
                idList = json.load(f)
            segments = []

            for i in quotes:
                index = random.randint(0, len(quotes) - 1)
                if name in idList:
                    qqid = idList[name]
                else:
                    qqid = event.self_id
                quote = quotes[index]
                quoteStr = f"\"{quote}\"\n\n      ————{name}"
                segments.append(MessageSegment(
                    "node",
                    {
                        "uin": str(qqid),
                        "name": "听"+name+"说：",
                        "content": quoteStr
                    }
                )
                )
            bot = nonebot.get_bot()
            is_private = isinstance(event, PrivateMessageEvent)
            if (is_private):
                await bot.call_api(
                    "send_private_forward_msg", user_id=event.user_id, messages=segments
                )
            else:
                await bot.call_api(
                    "send_group_forward_msg", group_id=event.group_id, messages=segments
                )
    else:
        await sendAllQuote.send("此人不在名人堂")

# 如果不存在返回None
def getNameFromList(inputName: string, nameList: Any) -> string:
    if inputName in nameList:
        return inputName
    else:
        with open(aliasPath, 'r', encoding="utf-8") as f:
            aliasList = json.load(f)
        if inputName in aliasList:
            return aliasList[inputName]
        else:
            return None
