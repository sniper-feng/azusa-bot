import time

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
import os
# lastSentTime = -1
sendAzusa = on_fullmatch("梓喵可爱")
if system() == "Windows":
    picsPath = os.getcwd()+"\\res\\azusa\\"
else:
    picsPath = os.getcwd()+"/res/azusa/"

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
        rabbitPath = os.getcwd()+"\\res\\rabbit\\"
    else:
        rabbitPath = os.getcwd()+"/res/rabbit/"
    files = os.listdir(rabbitPath)
    fileNum = len(files)
    index = random.randint(1, fileNum)
    await sendRabbit.send(Message([
        MessageSegment("image", {
            "file": f"{'file:///' + rabbitPath + str(index) + '.png'}"
        })
    ])
    )

donate = on_fullmatch("资助梓喵")
@donate.handle()
async def _(event: Event, message: Message = EventMessage()):
    if system() == "Windows":
        picPath = os.getcwd()+"\\res\\donate.png"
    else:
        picPath = os.getcwd()+"/res/donate.png"
    await donate.send(Message([
        MessageSegment("text", {
            "text": "你好捏，因为bot目前运行在云服务器上，每个月需要一定的服务器费用，"
                    "如果你感觉bot的功能给你带来了便利的话，可以考虑酌情赞助一点捏！可以打几块钱赞助我去打一pc，或者十几块钱包了我的出勤午饭捏"
        }),
        MessageSegment("image", {
            "file": "file:///" + picPath
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
#         templatePath = os.getcwd()+"\\res\\cardtemplate.png"
#     else:
#         templatePath = os.getcwd()+"/res/cardtemplate.png"
#     template = Image.open(templatePath)
#     img = Image.open(message[1]["data"]["file"])
#     await makeCard.send(message[1]["data"]["file"])
