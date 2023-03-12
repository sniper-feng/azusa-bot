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

with open("D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\prop\\dine.json", 'r', encoding="utf-8") as f:
    dineList = json.load(f)
dine = on_regex(r"(一|二)区吃什么")

@dine.handle()
async def _(event: Event, message: Message = EventMessage()):
    campus = 0 if message[0].data['text'][0] == '一' else 1
    dineInCampus = dineList['campus'][campus]
    index = random.randint(0,len(dineInCampus))
    if index == 0:
        await dine.send("吃锤子!")
    else:
        await dine.send("吃 " + dineInCampus[index-1] +" 怎么样喵?")
    return

