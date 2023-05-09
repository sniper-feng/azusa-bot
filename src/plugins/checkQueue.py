import json

import time
from typing import re

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
import os
from nonebot import require
from nonebot.plugin.on import on_fullmatch, on_regex, on_command

from src.plugins.public import TEST_GROUP_ID

if system() == "Windows":
    shopPath = os.getcwd() + "\\prop\\shop.json"
else:
    shopPath = os.getcwd() + "/prop/shop.json"
with open(shopPath, "r", encoding="utf-8") as f:
    shopList = json.load(f)

shop_name = list(shopList.keys())
shop_capacity = []
for it in shopList.items():
    shop_capacity.append(it[1])
shop_queue = [-1 for i in range(len(shop_capacity))]
report_time = [0 for i in range(len(shop_capacity))]

shop_regex = r"^("
count = 0
for it in shop_name:
    if count != 0:
        shop_regex += "|"
    shop_regex += it
    count += 1
shop_regex += r")([0-9]{1,})$"

register = on_regex(shop_regex)

check_regex = r"^("
count = 0
for it in shop_name:
    if count != 0:
        check_regex += "|"
    check_regex += it
    count += 1
check_regex += r")几$"
checkOut = on_regex(check_regex)

# 黑名单
if system() == "Windows":
    blacklistPath = os.getcwd() + "\\prop\\blacklist.json"
else:
    blacklistPath = os.getcwd() + "/prop/blacklist.json"
riskList = {}

# format of data csv:
# month,mday,wday,location,queue
SHOP_QUEUE_MAXIMUM = 30
SHOP_QUEUE_DELTA_MAXIUM = 8
SHOP_QUEUE_DELTA_TIME = 2 * 60 * 60  # 允许两个小时之后的大幅度修改


@register.handle()
async def _(event: Event, message: Message = EventMessage()):
    with open(blacklistPath, "r", encoding="utf-8") as f:
        blackList = json.load(f)
    qqid = int(event.get_user_id())
    if qqid in blackList:
        await register.send("宝宝，你也配用？")
        return
    queue = int(re.match(shop_regex, event.get_plaintext()).group(2))
    shop = re.match(shop_regex, event.get_plaintext()).group(1)
    shopid = shop_name.index(shop)
    if queue >= SHOP_QUEUE_MAXIMUM or \
            (not shop_queue[shopid] == -1 and queue - shop_queue[shopid] >= SHOP_QUEUE_DELTA_MAXIUM
             and not event.time - report_time[shopid] > SHOP_QUEUE_DELTA_TIME):
        if qqid in riskList:
            if riskList[qqid] >= 3:
                blackList.append(qqid)
                with open(blacklistPath, "w", encoding="utf-8") as bf:
                    blstr = json.dumps(blackList)
                    bf.write(blstr)
                    await register.send("宝宝，你也配用？")
                    return
            else:
                riskList[qqid] += 1
        else:
            riskList[qqid] = 1
        await register.send(f"你搞尼玛呢.....\n神秘计数器：{riskList[qqid]}")
        return

    shop_queue[shopid] = queue
    report_time[shopid] = event.time
    localtime = time.localtime(time.time())
    with open(os.getcwd() + "/res/statis.csv", "a+") as csvFile:
        csvFile.write(
            f"{localtime.tm_mon},{localtime.tm_mday},{localtime.tm_wday},{localtime.tm_hour},"
            f"{localtime.tm_min},{shopid},{queue}\n")


@checkOut.handle()
async def _(event: Event, message: Message = EventMessage()):
    with open(blacklistPath, "r", encoding="utf-8") as f:
        blackList = json.load(f)
    qqid = int(event.get_user_id())
    if qqid in blackList:
        await checkOut.send("宝宝，你也配用？")
        return
    shop = re.match(check_regex,event.get_plaintext()).group(1)
    shopid = shop_name.index(shop)
    queue = shop_queue[shopid]
    reportedLocalTime = time.localtime(report_time[shopid])
    reportString = f"{reportedLocalTime.tm_hour}点" + ("0" if reportedLocalTime.tm_min < 10 else "") + \
                   f"{reportedLocalTime.tm_min}分的时候{shop}有{queue}人喵..."
    if time.localtime(time.time()).tm_yday - reportedLocalTime.tm_yday >= 1:  # 清空过期数据
        shop_queue[shopid] = -1
        report_time[shopid] = time.time()
    if queue == -1:
        await checkOut.send("没有人报人数喵...")
    else:

        if shop_queue[shopid] >= 2 * shop_capacity[shopid]:
            reportString += f"这家店有{shop_capacity[shopid]}台机器，现在去的话预估一轮的等待时间为" \
                            f"{int(shop_queue[shopid] / shop_capacity[shopid] / 2) * 15}分钟喵！\n"
        else:
            reportString += f"这家店有{shop_capacity[shopid]}台机器，现在去的话也许可以爽霸喵...\n"
        sendTime = time.localtime(time.time())
        await checkOut.send(reportString)
        with open(os.getcwd() + "/res/statis.csv", "a+") as csvFile:
            csvFile.write(
                f"{reportedLocalTime.tm_mon},{reportedLocalTime.tm_mday},{reportedLocalTime.tm_wday},"
                f"{reportedLocalTime.tm_hour},{reportedLocalTime.tm_min},{shopid},{queue}\n")


sendAll = on_fullmatch("魅力冰城")


@sendAll.handle()
async def _(event: Event, message: Message = EventMessage()):
    with open(blacklistPath, "r", encoding="utf-8") as f:
        blackList = json.load(f)
    qqid = int(event.get_user_id())
    if qqid in blackList:
        await sendAll.send("宝宝，你也配用？")
        return
    string = "冰!! 城 夏↓↓ 都~ 哈尔滨大逼队欢迎您...喵?\n"
    for index in range(0, len(shop_name)):
        if time.localtime(time.time()).tm_yday - time.localtime(report_time[index]).tm_yday >= 1:  # 清空过期数据
            shop_queue[index] = -1
            report_time[index] = time.time()

        if shop_queue[index] == -1:
            string += f"{shop_name[index]}没有数据\n"
        else:
            reportedLocalTime = time.localtime(report_time[index])
            string += f"{shop_name[index]}有{shop_queue[index]}人({reportedLocalTime.tm_hour}:" \
                      + ("0" if reportedLocalTime.tm_min < 10 else "") + f"{reportedLocalTime.tm_min}).\n "
            # if shop_queue[index] >= 2 * shop_capacity[index]:
            #     string += f"这家店有{shop_capacity[index]}台机器，现在去的话预估一轮的等待时间为" \
            #               f"{int(shop_queue[index] / shop_capacity[index] / 2) * 15}分钟喵！\n"
            # else:
            #     string += f"这家店有{shop_capacity[index]}台机器，现在去的话也许可以爽霸喵...\n"
            # 避免刷屏，已弃用。
    await sendAll.send(string)


# -------------------------------------牡丹江暂用----------------------------------
MUDANJIANG_GROUP_ID = 995682103
shop_name_ = ["万达"]
shop_capacity_ = [1]
shop_queue_ = [-1]
report_time_ = [0]
shop_regex_ = r"^(万达)[0-9]{1,}$"
register_mudanjiang = on_regex(shop_regex_)


@register_mudanjiang.handle()
async def _(event: Event, message: Message = EventMessage()):
    if event.group_id == MUDANJIANG_GROUP_ID or event.group_id == TEST_GROUP_ID:
        queue = int(re.search("[0-9]+", event.get_plaintext()).group(0))
        shop = event.get_plaintext()[0:2]
        shopid = shop_name_.index(shop)
        if queue >= SHOP_QUEUE_MAXIMUM or \
                (not shop_queue_[shopid] == -1 and queue - shop_queue_[shopid] >= SHOP_QUEUE_DELTA_MAXIUM
                 and not event.time - report_time_[shopid] > SHOP_QUEUE_DELTA_TIME):
            await register.send(f"别乱报唷...")
            return

        shop_queue_[shopid] = queue
        report_time_[shopid] = event.time


check_regex_ = r"(万达)几"
checkOut_ = on_regex(check_regex_)


@checkOut_.handle()
async def _(event: Event, message: Message = EventMessage()):
    if event.group_id == MUDANJIANG_GROUP_ID or event.group_id == TEST_GROUP_ID:
        shop = event.get_plaintext()[0:2]
        shopid = shop_name_.index(shop)
        queue = shop_queue_[shopid]
        reportedLocalTime = time.localtime(report_time_[shopid])
        reportString = f"{reportedLocalTime.tm_hour}点" + ("0" if reportedLocalTime.tm_min < 10 else "") + \
                       f"{reportedLocalTime.tm_min}分的时候{shop}有{queue}人喵..."
        if time.localtime(time.time()).tm_yday - reportedLocalTime.tm_yday >= 1:  # 清空过期数据
            shop_queue_[shopid] = -1
            report_time_[shopid] = time.time()
        if queue == -1:
            await checkOut.send("没有人报人数喵...")
        else:

            if shop_queue_[shopid] >= 2 * shop_capacity_[shopid]:
                reportString += f"这家店有{shop_capacity_[shopid]}台机器，现在去的话预估一轮的等待时间为" \
                                f"{int(shop_queue_[shopid] / shop_capacity_[shopid] / 2) * 15}分钟喵！\n"
            else:
                reportString += f"这家店有{shop_capacity_[shopid]}台机器，现在去的话也许可以爽霸喵...\n"
            sendTime = time.localtime(time.time())
            await checkOut.send(reportString)
