import json
import os
from platform import system
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

require('maimaidx')
if system() == "Windows":
    missionPath = os.getcwd()+"\\prop\\mission.json"
else:
    missionPath = os.getcwd()+"/prop/mission.json"

with open(missionPath, 'r', encoding="utf-8") as f:
    missionList = json.load(f)

getMissionList = on_command('课题列表', aliases={'今日课题'})


@getMissionList.handle()
async def putMissionList():
    num = len(missionList["missions"])
    listStr = f"目前共有{num}组课题可供游玩。\n"
    for mission in missionList["missions"]:
        listStr += (f"课题id: {mission['id']} , 课题名称：" + mission['name'] + '\n')
    await getMissionList.send(listStr)
    # do something


sendSonglist = on_regex(r"课题id([0-9]+)")


@sendSonglist.handle()
async def _(event: Event, message: Message = EventMessage()):
    global msgString
    found = False
    for mission in missionList["missions"]:
        regex = "([0-9]+)"
        missionID = int(re.search(regex, str(message)).group(0))
        if missionID == mission['id']:
            found = True
            msgString = ''
            for index in range(4):
                if index != 0:
                    msgString += '\n\n'
                trackID = mission['songlist'][index]
                music = total_list.by_id(str(trackID))
                msgString += f"Track {index+1} : \n "
                msgString += str(trackID) + '.'
                msgString += music.title
                level_name = ['Expert', 'Master', 'Re: MASTER']
                msgString += "   " + level_name[mission['diff'][index]]
                msgString += f'\n目标: {mission["target"][index]}'

    if found:
        await sendSonglist.send(msgString)
    else:
        await sendSonglist.send(f"并未找到这样的段位组。{missionID}")
    return


if __name__ == "__main__":
    print(missionList)
    print(len(missionList["missions"]))
    mission1 = missionList["missions"][0]
    num = len(missionList["missions"])
    listStr = f"目前共有{num}组课题可供游玩。\n"
    for mission in missionList["missions"]:
        listStr += (f"课题id: {mission['id']} , 课题名称：" + mission['name'] + '\n')
    print(listStr)
