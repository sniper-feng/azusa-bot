import json

import string
import time

import nonebot
from nonebot import on_command, on_regex
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PrivateMessageEvent

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
import re

from nonebot import require
from nonebot.plugin.on import on_fullmatch, on_regex, on_command
import os
SELF_ID = 2284891492

if system() == "Windows":
    quotePath = os.getcwd() + "\\prop\\quote.json"
else:
    quotePath = os.getcwd() + "/prop/quote.json"
if system() == "Windows":
    aliasPath = os.getcwd() + "\\prop\\alias.json"
else:
    aliasPath = os.getcwd() + "/prop/alias.json"
if system() == "Windows":
    idPath = os.getcwd() + "\\prop\\QQID.json"
else:
    idPath = os.getcwd() + "/prop/QQID.json"

addQuote = on_command("入典")


@addQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        quoteList[name].append(strs[2])
        with open(quotePath, 'w', encoding="utf-8") as f:
            jsonStr = json.dumps(quoteList)
            jsonStr.encode('unicode_escape').decode("unicode-escape")
            f.write(jsonStr)
    else:
        await addQuote.send("这个人不在名人堂呢")


# 加入名人堂 车乃 alias=何大东
addPerson = on_command("加入名人堂")


@addPerson.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 2)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    # 普通添加
    if len(strs) == 2:
        if strs[1] in quoteList.keys():
            await addQuote.send("此人已在名人堂")
        else:
            quoteList[strs[1]] = []
            with open(quotePath, 'w', encoding="utf-8") as f:
                jsonStr = json.dumps(quoteList)
                jsonStr.encode('unicode_escape').decode("unicode-escape")
                f.write(jsonStr)
    else:
        # 添加别名
        alias = strs[2][6:]  # 别名
        if getNameFromList(strs[1], quoteList.keys()) is None:
            await addQuote.send("此人不在名人堂")
        else:
            trueName = getNameFromList(strs[1], quoteList.keys())
            with open(aliasPath, 'r', encoding="utf-8") as f:
                aliasList = json.load(f)
            aliasList[alias] = trueName
            with open(aliasPath, 'w', encoding="utf-8") as f:
                jsonStr = json.dumps(aliasList)
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
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        personSuffix = list(quoteList.keys()).index(strs[1])
        quotes = quoteList[name]
        if len(quotes) == 0:
            await addQuote.send("这个人没有典呢")
        else:
            index = random.randint(0, len(quotes) - 1)
            quote = quotes[index]
            await sendQuote.send(f"{personSuffix+1}.{index+1}  \"{quote}\"\n\n      ————{name}")
    else:
        await addQuote.send("此人不在名人堂")


sendQuoteGroup = on_command("十连爆典")


@sendQuoteGroup.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        personSuffix = list(quoteList.keys()).index(strs[1])
        quotes = quoteList[name]

        if len(quotes) == 0:
            await sendQuoteGroup.send("这个人没有典呢")
        else:
            with open(idPath, 'r', encoding="utf-8") as f:
                idList = json.load(f)
            segments = []
            for i in range(0, 10):
                index = random.randint(0, len(quotes) - 1)
                if name in idList:
                    qqid = idList[name]
                else:
                    qqid = event.self_id
                quote = quotes[index]
                quoteStr = f"{personSuffix+1}.{index+1}  \"{quote}\"\n\n      ————{name}"
                segments.append(MessageSegment(
                    "node",
                    {
                        "uin": str(qqid),
                        "name": "听" + name + "说：",
                        "content": quoteStr
                    }
                )
                )
            bot = nonebot.get_bot()
            is_private = isinstance(event, PrivateMessageEvent)
            if (is_private):
                await bot.call_api(
                    "send_private_forward_msg", user_id=event.user_id, messages=segments
                )
            else:
                await bot.call_api(
                    "send_group_forward_msg", group_id=event.group_id, messages=segments
                )
    else:
        await sendQuoteGroup.send("此人不在名人堂")


sendAllQuote = on_command("allin爆典")


@sendAllQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)

    if not getNameFromList(strs[1], quoteList.keys()) is None:
        name = getNameFromList(strs[1], quoteList.keys())
        personSuffix = list(quoteList.keys()).index(strs[1])
        quotes = quoteList[name]
        if len(quotes) == 0:
            await sendQuoteGroup.send("这个人没有典呢")
        else:
            with open(idPath, 'r', encoding="utf-8") as f:
                idList = json.load(f)
            segments = []

            for index in range(0, len(quotes)):

                if name in idList:
                    qqid = idList[name]
                else:
                    qqid = event.self_id
                quote = quotes[index]
                quoteStr = f"{personSuffix+1}.{index+1}  \"{quote}\"\n\n      ————{name}"
                segments.append(MessageSegment(
                    "node",
                    {
                        "uin": str(qqid),
                        "name": "听" + name + "说：",
                        "content": quoteStr
                    }
                )
                )
            bot = nonebot.get_bot()
            is_private = isinstance(event, PrivateMessageEvent)
            if (is_private):
                await bot.call_api(
                    "send_private_forward_msg", user_id=event.user_id, messages=segments
                )
            else:
                await bot.call_api(
                    "send_group_forward_msg", group_id=event.group_id, messages=segments
                )
    else:
        await sendAllQuote.send("此人不在名人堂")


# 如果不存在返回None
def getNameFromList(inputName: string, nameList: Any) -> string:
    if inputName in nameList:
        return inputName
    else:
        with open(aliasPath, 'r', encoding="utf-8") as f:
            aliasList = json.load(f)
        if inputName in aliasList:
            return aliasList[inputName]
        else:
            return None


strangeQuotes = [
    "今天是xx瘾发作最严重的一次， 躺在床上，拼命喊着xx的名字，难受的一直抓自己眼睛，以为刷b站没事，发现全b站都在推xx的视频，"
    "眼睛越来越大都要炸开了一样，拼命扇自己眼睛，越扇越用力，扇到自己眼泪流出来，真的不知道该怎么办，我真的想xx想得要发疯了。"
    "我躺在床上会想xx，我洗澡会想xx，我出门会想xx，我走路会想xx，我坐车会想xx，我工作会想xx，我玩手机会想xx，我盯着路边的xx看，"
    "我盯着马路对面的xx看，我盯着地铁里的xx看，我盯着网上的xx看，我盯着朋友圈别人合照里的xx看，我每时每刻眼睛都直直地盯着xx看，"
    "像一台雷达一样扫视经过我身边的每一只xx， 我真的觉得自己像中邪了一样，我对xx的念想似乎都是病态的了，我好孤独啊！真的好孤独啊！"
    "xx xx 没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx "
    "没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx 没有你我可怎么活啊 xx xx "
    "没有你我可怎么活啊 xx xx 没有你我可怎么活啊",
    "在没有看到xx之前，我脖子上戴着佛珠左手拿十字架✝️右手拿符纸，请了六十个老和尚 ‍在我旁边打坐念经。看见xx后，"
    "我靠，这就是我的命中注定，这就是我的人生唯一，我扯下我的佛珠，扔掉我的十字架，撒光我的符纸，赶跑六十个老和尚，"
    "我不再需要这些了，此时此刻我满心满眼都是你，我整个人都在地板上打滚，我亲吻我的地板，我捶烂我的墙壁，"
    "我喝了十八碗二锅头，我为你而醉，我惊声尖叫       xx我没有你该怎么办",
    "xx！xx！xx！(尖叫) (扭曲) (阴暗地爬行)(尖叫) (扭曲) (阴暗地爬行)(尖叫) (扭曲) (阴暗地爬行)(尖叫) (扭曲) "
    "(阴暗地爬行)(尖叫) (扭曲) (阴暗地爬行)(尖叫) (扭曲) (阴暗地爬行)"
    "(尖叫) (扭曲) (阴暗地爬行)（最后变成弯弯曲曲在里世界散发怨念）",
    "xx，我稍微问一句，绝对没有冒犯的意思，也可能是我搞错了，又或者其实我是出现了幻觉，"
    "不管怎么样，我都希望我们能秉持着友好理性的相处原则，不要因为一些可能的误会伤害了我们之间的友谊，"
    "最后再说一句，我绝对没有冒犯的意思，只是本着对于宇宙本质的伟大探究精神以及求真务实精神发问:\n\n“我能和您结婚吗？”",
    "我在电梯间里“偶遇”了xx。\nxx按一层，我想，他在暗示我他家里只有他一个人诶。\nxx按二层，我想，他是想邀请我一起共进二人的晚餐吗。"
    "\nxx按三层，我想，他一定想说我们这辈子永不散场，泪目。\nxx按四层，我想，他想说他一见到我内心里就四海潮生。"
    "\nxx按五层，我想，他居然挑了五层，他是不是真的暗恋我。\nxx按六层，我想，看来他很崇拜我嘛。xx按七层，"
    "我想，他今年一定想跟我过七夕吧。\nxx按八层，我想，八层，他八成是喜欢我。\nxx按九层，我想，他一定是想跟我长久地走下去……"
    "\nxx按十层，我想，他一定是在纪念我们快要十年的(单方面)爱情。\nxx不按，我想，他见到我就紧张得不敢动了。"
    "\nxx刚进电梯又转身离开，我想，好，xx害臊的故意躲着我。他就是暗恋我。正好，我也喜欢你。",
    "xx，我被队长炒鱿鱼了 我重新找了份电焊工的工作 今天是我第一天当电焊工 "
    "天气很暖和 我站在树下点了一根烟 我不想再做电焊工了 我不是一个称职的电焊工 我电不到你 也焊不牢你的心"


]
sendLove = on_command("发癫")


@sendLove.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    name = strs[1]
    editedQuote = strangeQuotes[random.randint(0, len(strangeQuotes) - 1)].replace("xx",name)
    seg = MessageSegment(
        "node",
        {
            "uin": str(event.get_user_id()),
            "name": "听" + name + "说：",
            "content": editedQuote
        }
    )
    bot = nonebot.get_bot()
    is_private = isinstance(event, PrivateMessageEvent)
    if (is_private):
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = seg)
    else:
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = seg)



toDeleteList = {}
deleteQuote = on_regex(r"删典\s+[0-9]+.[0-9]+")
UPPER_LIMIT = 3
@deleteQuote.handle()
async def _(event: Event, message: Message = EventMessage()):
    matchobj = re.findall(r"[0-9]+", event.get_plaintext())
    personSuffix = int(matchobj[0]) - 1
    quoteSuffix = int(matchobj[1]) - 1
    with open(quotePath, 'r', encoding="utf-8") as f:
        quoteList = json.load(f)
    keys = list(quoteList.keys())
    if len(keys) > personSuffix:
        quotes = quoteList[keys[personSuffix]]

        if len(quotes) > quoteSuffix:
            # 提供的下标无误，开始检查待删除列表
            if not (personSuffix, quoteSuffix) in toDeleteList: #没有人投过这个删除票
                toDeleteList[(personSuffix, quoteSuffix)] = [event.get_user_id()] #将发起删除的用户加入列表
                await deleteQuote.send(f"现在有1个人决定投票删除这个典，若满{UPPER_LIMIT}人则可以直接删除")
            else:
                if not event.get_user_id() in toDeleteList[(personSuffix, quoteSuffix)]: #不在就加入，多一票。
                    toDeleteList[(personSuffix, quoteSuffix)].append(event.get_user_id())
                await deleteQuote.send(f"现在有{len(toDeleteList[(personSuffix, quoteSuffix)])}个人决定投票删除这个典，若满{UPPER_LIMIT}人则可以直接删除")
                if len(toDeleteList[(personSuffix, quoteSuffix)]) >= UPPER_LIMIT:
                    await deleteQuote.send("现在开删喵！")# 有足够的人投票决定删除
                    toDeleteList.pop((personSuffix, quoteSuffix))
                    del quoteList[keys[personSuffix]][quoteSuffix]
                    with open(quotePath, 'w', encoding="utf-8") as f:
                        jsonStr = json.dumps(quoteList)
                        jsonStr.encode('unicode_escape').decode("unicode-escape")
                        f.write(jsonStr)
                    # 删！
            return
    await deleteQuote.send("你提供的编号似乎不太对呢")