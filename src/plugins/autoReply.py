from nonebot import on_command, on_regex, Bot, on_notice, on_message
from nonebot import on_command, on_regex
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

spMsg = [
    "你说得对",
    "努",
    "9+15",
    "谢谢",
    "唐"
]
spMsgReply = {
    "你说得对": "但是轻音少女是一部由京都动画制作的音乐日常动画,下面忘了",
    "努": "努!!努!!!呢呢呢呢男男女女扭扭捏rrrrrrrr哼个6!kJj!!么的么的嫩模摸摸美女呢呢妈!66!",
    "9+15": "26",
    "谢谢": "学到许多",
    "唐": "类排序南瑞，今年什么套变成什么，南瑞结束初中生活一旦在课堂上我发现让你淹没的声音大声，啊啊啊啊啊啊啊啊啊啊啊啊啊！！！"
          "机管局，唐泽孝弘坤等，放出来大声突然我是铜 ，我什么，Euriburi Euriburi~羽劉某Ryuryu Ryuryu!!! "
          "啄集集集集eububu百合秩父助Eububuoooo~津市~津市~津市！！"
}

logFile = open("log.txt", "w")


async def message_checker(event: Event) -> bool:
    for msg in spMsg:
        if event.get_plaintext() == msg:
            logFile.writelines(msg)
            return True

    return False


replyRule = Rule(message_checker)
replySp = on_message(rule=replyRule)


@replySp.handle()
async def _(event: Event, message: Message = EventMessage()):
    for msg in spMsg:
        if event.get_plaintext() == msg:
            await replySp.send(spMsgReply[msg])
