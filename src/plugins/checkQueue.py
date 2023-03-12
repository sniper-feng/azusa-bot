import json
import time
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

shop_name = ["超星", "香坊", "哈西", "百盛", "阿城","江一","江二"]
shop_queue = [-1, -1, -1, -1, -1,-1,-1]
report_time = [0, 0, 0, 0, 0,0,0]
shop_regex = r"(超星|香坊|阿城|哈西|百盛|江一|江二)[0-9]{1,}"
register = on_regex(shop_regex)


@register.handle()
async def _(event: Event, message: Message = EventMessage()):
    queue = int(re.search("[0-9]+", event.get_plaintext()).group(0))
    shop = event.get_plaintext()[0:2]
    shopid = shop_name.index(shop)
    shop_queue[shopid] = queue
    report_time[shopid] = event.time
check_regex = r"(超星|香坊|阿城|哈西|百盛|江一|江二)几"
checkOut = on_regex(check_regex)

@checkOut.handle()
async def _(event: Event, message: Message = EventMessage()):
    shop = event.get_plaintext()[0:2]
    shopid = shop_name.index(shop)
    queue = shop_queue[shopid]
    if queue == -1:
        await checkOut.send("没有人报人数喵...")
    else:
        localtime = time.localtime(report_time[shopid])
        await checkOut.send(f"{localtime.tm_hour}点{localtime.tm_min}分的时候{shop}有{queue}人喵...")

