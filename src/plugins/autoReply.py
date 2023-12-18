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
import os

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

spMsgWithRule = [
    "不要断章取义"
    "zaquva"
]

logFile = open("log.txt", "w")

pairParentheses = on_regex(r"^(（|）|\(|\)|【|】|\{|\}|《|》|\<|\>|&#91;|&#93;)+$")


async def message_checker(event: Event) -> bool:
    if event.get_plaintext() in spMsg or event.get_plaintext() in spMsgWithRule \
            or "zaquva" in event.get_plaintext().lower():
        return True

    return False


replyRule = Rule(message_checker)
replySp = on_message(rule=replyRule)


@replySp.handle()
async def _(event: Event, message: Message = EventMessage()):
    if event.get_plaintext() == "不要断章取义":
        await replySp.send(f"\"要断章取义。\"\n\n      ————{event.sender.nickname}")
    elif event.get_plaintext().lower().find("zaquva") >= 0:
        await replySp.send("诘绥祉緑麻祥匈肱ZAQUVA壬怦，玉晢丙繍効芯舣沃赁殄艀并■効芯舣沃赁殄舍藕凬秽薜舸鬘悳页匈儿，慢蛸持匈箆恼BOSSA "
                           "GABBA挫伎怦氏箆DUANGDAUNGDAUNG咏弋埓仆突蛸咏峺芙咏亥恍悳页压匈儿慢积蛸持匈XCXC Crackpot "
                           "Evangelist阻伎怦压恐儿蛸芙纽蚋藓议瀑巾薜舸鬘序型寂鲶夕屠穉，F壌伉诘咏恋袖袖遭压想，匈儿页竃蛸持匈昨顿咏亥恍巷诘羮卫QQ1.25竜椒淅毅汇狛蛸匈寔挥低椣膸H"
                           "啜猷AHQUASE祉罢BIUBIUBIU淅毅汇咄嗄坊贞沥狡苔芙侵桃萄，F刊顿怦某漂侵桃暇蝶恂疎诘磬咄磬鹩栉咏旺c诘因舌粉compressor3耙specuation"
                           "汇蛸柄咳怦祉箆因舌因咏匈侏旺")

    else:
        for msg in spMsg:
            if event.get_plaintext() == msg:
                await replySp.send(spMsgReply[msg])


async def at_self(bot: Bot, event: Event) -> bool:
    id = bot.self_id
    if event.post_type == "message":
        value = f"[CQ:at,qq={id}]" in event.raw_message
    else:
        value = False
    return value


stopAtMe = on_message(rule=at_self, priority=3, block=True)


@stopAtMe.handle()
async def _(event: Event, message: Message = EventMessage()):
    await stopAtMe.send(Message(
        [MessageSegment("at",
                        {
                            "qq": str(event.get_user_id())
                        }
                        ),
         MessageSegment("at",
                        {
                            "qq": str(event.get_user_id())
                        }
                        ),
         MessageSegment("at",
                        {
                            "qq": str(event.get_user_id())
                        }
                        )
         ]
    ))


@pairParentheses.handle()
async def _(event: Event, message: Message = EventMessage()):
    s = event.get_plaintext().replace("&#93;", "]").replace("&#91;", "[")
    stack = []
    for ch in s:
        if ch == "（":
            stack.insert(0, "）")
        elif ch == "(":
            stack.insert(0, ")")
        elif ch == "【":
            stack.insert(0, "】")
        elif ch == "[":
            stack.insert(0, "]")
        elif ch == "{":
            stack.insert(0, "}")
        elif ch == "《":
            stack.insert(0, "》")
        elif ch == "<":
            stack.insert(0, ">")
        elif ch in ["）", ")", "】", "]", "}", "》", ">"]:
            if len(stack) > 0 and stack[0] == ch:
                stack.pop(0)

    if len(stack) > 0:
        output = ""
        for ch in stack:
            output += ch
        await pairParentheses.send(output)


mentionDict = {}


async def at_someone(bot: Bot, event: Event) -> bool:
    if event.post_type == "message":
        return "[CQ:at,qq=" in event.raw_message


mentionSb = on_message(rule=at_someone, priority=3, block=True)


@mentionSb.handle()
async def _(event: Event, message: Message = EventMessage()):
    target = re.findall(r"\[CQ:at,qq={[0-9]+}\]")[0][0]
    mentionDict[target] = event.get_user_id()


# bark.....
barkList = []
if system() == "Windows":
    barkpath = os.getcwd() + "\\prop\\bark.json"
else:
    barkpath = os.getcwd() + "/prop/bark.json"
with open(barkpath, "r", encoding="utf-8") as f:
    barkList = json.load(f)


async def bark_checker(event: Event) -> bool:
    txt = event.get_plaintext()
    for word in barkList:
        if word in txt:
            return True
    return False


bark = on_message(rule=bark_checker, priority=3, block=True)

barkDict = {}


@bark.handle()
async def _(event: Event, message: Message = EventMessage()):
    if event.group_id in barkDict:
        if event.get_user_id() in barkDict[event.group_id]:
            barkDict[event.group_id][event.get_user_id()] += 1
        else:
            barkDict[event.group_id] = {event.get_user_id(): 1}
    else:
        barkDict[event.group_id] = {event.get_user_id(): 1}
    await bark.send("检测到狗叫声")


checkBark = on_command("狗叫王")


@checkBark.handle()
async def _(event: Event, message: Message = EventMessage()):
    if event.group_id not in barkDict:
        await checkBark.send("本群暂时无人狗叫")
        return
    lis = barkDict[event.group_id]

    length = max(5, len(lis))
    msg = [{
        "type": "text",
        "data": {
            "text": "狗叫榜\n"
        }
    }]
    i = 1
    for qqid in list(lis.keys()):
        if i > 5:
            break
        s1 = f"第{i}名:"
        s2 = f"  共狗叫{lis[qqid]}次\n"

        msg.append({
            "type": "text",
            "data": {
                "text": s1
            }

        })
        msg.append({
            "type": "at",
            "data": {
                "qq": qqid
            }
        })
        msg.append({
            "type": "text",
            "data": {
                "text": s2
            }
        }
        )
    await checkBark.send(Message(msg))

addBark = on_command("添加狗叫")


@addBark.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", 1)
    barkList.append(strs[1])
    with open(barkpath, "w", encoding="utf-8") as f:
        json.dump(barkList, f)
