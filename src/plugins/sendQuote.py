import json
import time

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
if system() == "Windows":
    quotePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\quote.json"
else:
    quotePath = "/home/sniperpigeon/bot/azusa-bot/prop/quote.json"


addQuote = on_command("入典")
@addQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 3)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    if strs[1] in quoteList.keys():
        quoteList[strs[1]].append(strs[2])
        with open(quotePath, 'w', encoding="utf-8") as f:
            jsonStr = json.dumps(quoteList)
            jsonStr.encode('unicode_escape').decode("unicode-escape")
            f.write(jsonStr)
    else:
        await addQuote.send("这个人不在名人堂呢")


addPerson = on_command("加入名人堂")
@addPerson.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    if strs[1] in quoteList.keys():
        await addQuote.send("此人已在名人堂")
    else:
        quoteList[strs[1]] = []
        with open(quotePath, 'w', encoding="utf-8") as f:
            jsonStr = json.dumps(quoteList)
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
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if strs[1] in quoteList.keys():
        quotes = quoteList[strs[1]]
        if len(quotes) == 0:
            await addQuote.send("这个人没有典呢")
        else:
            index = random.randint(0, len(quotes)-1)
            quote = quotes[index]
            await sendQuote.send(f"\"{quote}\"\n\n      ————{strs[1]}")
    else:
        await addQuote.send("此人不在名人堂")
