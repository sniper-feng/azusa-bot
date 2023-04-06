import os
import time
from platform import system

from nonebot import on_fullmatch, on_message
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re

# lastSentTime = -1
sendAzusa = on_fullmatch("梓喵可爱")
if system() == "Windows":
    picsPath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\res\\azusa\\"
else:
    picsPath = "/home/sniperpigeon/bot/azusa-bot/res/azusa/"

pics = os.listdir(picsPath)
picNum = len(pics)


@sendAzusa.handle()
async def _(event: Event, message: Message = EventMessage()):
    # global lastSentTime
    # if time.time() - lastSentTime >= 1000 * 60 * 1:  # 一分钟内发过图
    index = random.randint(1, picNum)
    await sendAzusa.send(Message([
        MessageSegment("image", {
            "file": f"{'file:///' + picsPath + str(index) + '.png'}"
        })
    ])
    )
    lastSentTime = time.time()
    # else:
    # await sendAzusa.send("知道你夸我可爱了,刚刚才发了,不要再要了喵")


sendRabbit = on_fullmatch("行走生活")


@sendRabbit.handle()
async def _(event: Event, message: Message = EventMessage()):
    if system() == "Windows":
        rabbitPath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\res\\rabbit\\"
    else:
        rabbitPath = "/home/sniperpigeon/bot/azusa-bot/res/rabbit/"
    files = os.listdir(rabbitPath)
    fileNum = len(files)
    index = random.randint(1, fileNum)
    await sendRabbit.send(Message([
        MessageSegment("image", {
            "file": f"{'file:///' + rabbitPath + str(index) + '.png'}"
        })
    ])
    )

#
# async def cardRequest(event: Event) -> bool:
#     msg = event.get_message()
#     return msg[0]["type"] == "text" and msg[0]["data"]["text"] == "制作卡面" and msg[1]["type"] == "image"
#
#
# makeCardRule = Rule(cardRequest)
# makeCard = on_message(rule=makeCardRule)
# @makeCard.handle()
# async def _(event: Event, message: Message = EventMessage()):
#     if system() == "Windows":
#         templatePath = "D:\\maimai-bot\\mai-bot-sniper-main\\mai-bot-sniper-main\\res\\cardtemplate.png"
#     else:
#         templatePath = "/home/sniperpigeon/bot/azusa-bot/res/cardtemplate.png"
#     template = Image.open(templatePath)
#     img = Image.open(message[1]["data"]["file"])
#     await makeCard.send(message[1]["data"]["file"])
