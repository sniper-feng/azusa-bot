import os
import time
from platform import system

from nonebot import on_fullmatch
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re

lastSentTime = -1
sendAzusa = on_fullmatch("梓喵可爱")
if system() == "Windows":
    picsPath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\res\\"
else:
    picsPath = "~/bot/azusa-bot/res/"

pics = os.listdir(picsPath)
picNum = len(pics)



@sendAzusa.handle()
async def _(event: Event, message: Message = EventMessage()):
    global lastSentTime
    if time.time() - lastSentTime >= 1000 * 60 * 2:  # 两分钟内发过图
        index = random.randint(1, picNum)
        await sendAzusa.send(Message([
            MessageSegment("image", {
                "file": f"{'file:///' + picsPath + str(index) + '.png'}"
            })
        ])
        )
        lastSentTime = time.time()
    else:
        await sendAzusa.send("知道你夸我可爱了,刚刚才发了,不要再要了喵")
