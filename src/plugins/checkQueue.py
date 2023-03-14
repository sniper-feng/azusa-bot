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

shop_name = ["超星", "香坊", "哈西", "百盛", "阿城", "江一", "江二"]
shop_queue = [-1, -1, -1, -1, -1, -1, -1]
report_time = [0, 0, 0, 0, 0, 0, 0]
shop_regex = r"(超星|香坊|阿城|哈西|百盛|江一|江二)[0-9]{1,}"
register = on_regex(shop_regex)


# format of data csv:
# month,mday,wday,location,queue


@register.handle()
async def _(event: Event, message: Message = EventMessage()):
    queue = int(re.search("[0-9]+", event.get_plaintext()).group(0))
    if queue >= 30:
        await register.send("再乱搞我要生气了喵! ")
        return
    shop = event.get_plaintext()[0:2]
    shopid = shop_name.index(shop)
    shop_queue[shopid] = queue
    report_time[shopid] = event.time
    localtime = time.localtime(time.time())
    with open("/home/sniperpigeon/bot/azusa-bot/res/statis.csv", "a+") as csvFile:
        csvFile.write(f"{localtime.tm_mon},{localtime.tm_mday},{localtime.tm_wday},{localtime.tm_hour},{localtime.tm_min},{shopid},{queue}\n")


check_regex = r"(超星|香坊|阿城|哈西|百盛|江一|江二)几"
checkOut = on_regex(check_regex)


@checkOut.handle()
async def _(event: Event, message: Message = EventMessage()):
    shop = event.get_plaintext()[0:2]
    shopid = shop_name.index(shop)
    queue = shop_queue[shopid]
    reportedLocalTime = time.localtime(report_time[shopid])
    if time.localtime(time.time()).tm_yday - reportedLocalTime.tm_yday >= 1:
        await checkOut.send("呀, 上次有人报人数还是昨天喵...已经清空了喵!")
        shop_queue[shopid] = -1
        report_time[shopid] = time.time()
    if queue == -1:
        await checkOut.send("没有人报人数喵...")
    else:
        await checkOut.send(f"{reportedLocalTime.tm_hour}点{reportedLocalTime.tm_min}分的时候{shop}有{queue}人喵...")
        sendTime = time.localtime(time.time())
        with open("/home/sniperpigeon/bot/azusa-bot/res/statis.csv", "a+") as csvFile:
            csvFile.write(f"{reportedLocalTime.tm_mon},{reportedLocalTime.tm_mday},{reportedLocalTime.tm_wday},{reportedLocalTime.tm_hour},{reportedLocalTime.tm_min},{shopid},{queue}\n")



sendAll = on_fullmatch("魅力冰城")
@sendAll.handle()
async def _(event: Event, message: Message = EventMessage()):
    string = "冰!! 城 夏↓↓ 都~ 哈尔滨大逼队欢迎您...喵?\n"
    for index in range(0,len(shop_name)):
        if shop_queue[index] == -1:
            string += f"{shop_name[index]}没有数据\n"
        elif shop_queue[index] >=8 :
            reportedLocalTime = time.localtime(report_time[index])
            string += f"{shop_name[index]}有{shop_queue[index]}人({reportedLocalTime.tm_hour}:{reportedLocalTime.tm_min})!卧槽 大逼队!\n"
        else:
            reportedLocalTime = time.localtime(report_time[index])
            string += f"{shop_name[index]}有{shop_queue[index]}人({reportedLocalTime.tm_hour}:{reportedLocalTime.tm_min}).\n"
    await sendAll.send(string)