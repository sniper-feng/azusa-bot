from platform import system

from nonebot import on_command, on_regex
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

if system() == "Windows":
    dinePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\dine.json"
else:
    dinePath = "/home/sniperpigeon/bot/azusa-bot/prop/dine.json"

with open(dinePath, 'r', encoding="utf-8") as f:
    dineList = json.load(f)
dine = on_regex(r"(一|二)区吃什么")


@dine.handle()
async def _(event: Event, message: Message = EventMessage()):
    campus = 0 if message[0].data['text'][0] == '一' else 1
    dineInCampus = dineList['campus'][campus]
    index = random.randint(0, len(dineInCampus))
    if index == 0:
        await dine.send("吃锤子!")
    else:
        await dine.send("吃 " + dineInCampus[index - 1] + " 怎么样喵?")
    return

shop_name = ["超星", "香坊", "哈西", "百盛", "阿城", "江一", "江二"]
shopDine = on_regex(r"(超星|香坊|阿城|哈西|百盛|江一|江二)吃什么")

@shopDine.handle()
async def _(event: Event, message: Message = EventMessage()):
    shopName = event.get_plaintext()[0:2]
    shopid = shop_name.index(shopName)
    dineInShop = dineList['shop'][shopid]
    index = random.randint(0, len(dineInShop))
    if index == 0:
        await dine.send("吃锤子!")
    else:
        await dine.send("吃 " + dineInShop[index - 1] + " 怎么样喵?")
    return

