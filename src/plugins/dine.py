
import time
from platform import system

from nonebot import on_command, on_regex, Bot, on_fullmatch
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
import os
if system() == "Windows":
    blacklistPath = os.getcwd()+"\\prop\\blacklist.json"
else:
    blacklistPath = os.getcwd()+"/prop/blacklist.json"

if system() == "Windows":
    dinePath = os.getcwd()+"\\prop\\dine.json"
else:
    dinePath = os.getcwd()+"/prop/dine.json"

with open(dinePath, 'r', encoding="utf-8") as f:
    dineList = json.load(f)

dine = on_regex(r"^.{2}吃什么$")
sendDineList = on_regex(r"^.{2}菜单$")

list_name = list(dineList.keys())


@sendDineList.handle()
async def _(event: Event, message: Message = EventMessage()):
    if system() == "Windows":
        dinePath = os.getcwd()+"\\prop\\dine.json"
    else:
        dinePath = os.getcwd()+"/prop/dine.json"
    with open(dinePath, 'r', encoding="utf-8") as f:
        dineList = json.load(f)
    name = event.get_plaintext()[0:2]
    if list_name.count(name) == 0:
        await sendDineList.send(f"根本没有{name}这家店喵...这边建议您吃\n锤子\n锤子\n锤子\n喵!")
    else:
        listStr = f"群友在{name}登录过的吃的有:\n"
        for dish in dineList[name]:
            listStr += dish + "           "
        listStr += "喵!"
        await sendDineList.send(listStr)


@dine.handle()
async def _(event: Event, message: Message = EventMessage()):
    if system() == "Windows":
        dinePath = os.getcwd()+"\\prop\\dine.json"
    else:
        dinePath = os.getcwd()+"/prop/dine.json"

    with open(dinePath, 'r', encoding="utf-8") as f:
        dineList = json.load(f)
    name = event.get_plaintext()[0:2]
    dineNames = dineList[name]
    index = random.randint(0, len(dineNames))
    if index == 0:
        await dine.send("吃锤子!")
    else:
        await dine.send("吃 " + dineNames[index - 1] + " 怎么样喵?")
    return

#  哪个傻逼写的废品
# shop_name = ["超星", "香坊", "哈西", "百盛", "阿城", "江一", "江二"]
# shopDine = on_regex(r"(超星|香坊|阿城|哈西|百盛|江一|江二)吃什么")
#
#
# @shopDine.handle()
# async def _(event: Event, message: Message = EventMessage()):
#     with open(blacklistPath, "r", encoding="utf-8") as f:
#         blackList = json.load(f)
#     qqid = int(event.get_user_id())
#     if qqid in blackList:
#         await shopDine.send("宝宝，你也配用？")
#         return
#     if system() == "Windows":
#         dinePath = os.getcwd()+"\\prop\\dine.json"
#     else:
#         dinePath = os.getcwd()+"/prop/dine.json"
#
#     with open(dinePath, 'r', encoding="utf-8") as f:
#         dineList = json.load(f)
#     shopName = event.get_plaintext()[0:2]
#     shopid = shop_name.index(shopName)
#     dineInShop = dineList['shop'][shopid]
#     index = random.randint(0, len(dineInShop))
#     if index == 0:
#         await dine.send("吃锤子!")
#     else:
#         await dine.send("吃 " + dineInShop[index - 1] + " 怎么样喵?")
#     return


# 约饭事件格式为:
# time:int,为月天数
# location:int 0=一区 1=二区
# meal:0=午饭 1=晚饭
# dine:str 吃什么
# member:list[str]:成员昵称
class DineEvent:
    id: int
    day: int
    location: int
    meal: int
    dine: str
    member: Any

    def __init__(self, id, day, location, meal, dine, member):
        self.id = id
        self.day = day
        self.location = location
        self.meal = meal
        self.dine = dine
        self.member = member


dines = []
dineIDs = []
DANGSHIYAN_GROUP_ID = 362333805
TEST_GROUP_ID = 547862267


async def dateRule(bot: Bot, event: Event) -> bool:
    segments = event.get_plaintext().split(" ", 4)
    if len(segments) < 4:
        return False
    value = (segments[1] == "一区" or segments[1] == "二区") and (segments[2] == "午饭" or segments[2] == "晚饭") and \
            (event.group_id == DANGSHIYAN_GROUP_ID or event.group_id == TEST_GROUP_ID)
    return value


# 新建约饭 一区/二区 午饭/晚饭 吃什么
newDateDine = on_command("新建约饭", dateRule)


@newDateDine.handle()
async def _(event: Event, message: Message = EventMessage()):
    segments = event.get_plaintext().split(" ", 4)
    dineID = random.randint(10, 40)
    while dineIDs.count(dineID) != 0:
        dineID = random.randint(10, 40)
    dineIDs.append(dineID)
    dineEvent = DineEvent(
        dineID,
        time.localtime(time.time()).tm_mday,
        0 if segments[1] == "一区" else 1,
        0 if segments[2] == "午饭" else 1,
        segments[3],
        [event.sender.nickname]
    )
    dines.append(dineEvent)
    await newDateDine.send("约饭成功喵!")


checkDine = on_fullmatch("查看约饭")


@checkDine.handle()
async def _(event: Event, message: Message = EventMessage()):
    if len(dines) == 0:
        await checkDine.send("目前没有人约饭喵..")
        return
    else:
        today = time.localtime(time.time()).tm_mday
        # 把不是今天的删了
        for index in range(0, len(dines)):
            if dines[index].day != today:
                dineIDs.remove(dines[index].id)
                dines.remove(dines[index])

    # 只显示今天的
    if len(dines) == 0:
        await checkDine.send("目前没有人约饭喵..")
        return
    else:
        dineString = f"查找到了{len(dines)}个约饭请求喵!\n\n"
        for index in range(0, len(dines)):
            dineString += f"约饭id{dines[index].id}: {'一区' if dines[index].location == 0 else '二区'}{'午饭' if dines[index].meal == 0 else '晚饭'}吃" \
                          f"{dines[index].dine},参与者有:"
            for indexMember in range(0, len(dines[index].member)):
                dineString += "" if indexMember == 0 else "," + dines[index].member[indexMember]

            dineString += '\n\n'
        await checkDine.send(dineString)


joinDine = on_regex("^加入约饭 id[0-9]{1,2}$")


@joinDine.handle()
async def _(event: Event, message: Message = EventMessage()):
    dineID = int(event.get_plaintext()[-2:])
    try:
        dineIndex = dineIDs.index(dineID)
        dines[dineIndex].member.append(event.sender.nickname)
        dineString = f"添加成功喵!现在{'一区' if dines[dineIndex].location == 0 else '二区'}{'午饭' if dines[dineIndex].meal == 0 else '晚饭'}吃" + \
                     f"{dines[dineIndex].dine},参与者有:"
        for indexMember in range(0, len(dines[dineIndex].member)):
            dineString += "" if indexMember == 0 else "," + dines[dineIndex].member[indexMember]

    except ValueError:
        await checkDine.send("没有这个约饭id喵..")
    else:
        await checkDine.send(dineString)
