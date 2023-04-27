import html
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

import sqlite3
import requests

TEXTAGE_ARCADE_TRACK_TABLE = "https://www.textage.cc/score/actbl.js"
TEXTAGE_METADATA_TABLE = "https://www.textage.cc/score/datatbl.js"
TEXTAGE_VERSION_NAME_TABLE = "https://www.textage.cc/score/datatbl.js"
TEXTAGE_TRACK_TITLE_TABLE = "https://www.textage.cc/score/titletbl.js"

rebuildDatabase = on_fullmatch("iidx-rebuild-database")
iidxSearch = on_command("/iidx查歌", aliases={"查寺","查二寺"})
iidxhelp = on_fullmatch("/iidx help")
iidxInfo = on_regex(r"/iidx查谱\s+([0-9]{1,4}?)\s*([S,D,s,d][p,P][B,b,N,n,H,h,a,AL,l])?")
vertbl = ["Consumer only", "1st style", "2nd style", "3rd style", "4th style",
          "5th style", "6th style", "7th style", "8th style", "9th style", "10th style",
          "IIDX RED", "HAPPY SKY", "DistorteD", "GOLD", "DJ TROOPERS", "EMPRESS",
          "SIRIUS", "Resort Anthem", "Lincle", "tricoro", "SPADA", "PENDUAL",
          "copula", "SINOBUZ", "CANNON BALLERS", "Rootage", "HEROIC VERSE",
          "BISTROVER", "CastHour", "RESIDENT"]


@rebuildDatabase.handle()
async def _(event: Event, message: Message = EventMessage()):
    start = time.time()

    # -------------------------------------------------主表-------------------------------------------------
    #  ID           name       title    genre   artist   version
    #  （数字Id，主键） (texage的内部字串)
    if os.path.exists("res/iidxdb.db"):
        os.remove("res/iidxdb.db")
    db = sqlite3.connect("res/iidxdb.db")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE main
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INT NOT NULL ,
    name    TEXT NOT NULL,
    title   TEXT NOT NULL,
    genre   TEXT NOT NULL,
    artist  TEXT NOT NULL,
    version INT  NOT NULL);''')
    db.commit()
    #   --------------网页数据过滤------------------------
    mainPlainText = requests.get(TEXTAGE_TRACK_TITLE_TABLE).content.decode("shift-jis").encode("utf-8").decode("utf-8")
    mainPlainText = mainPlainText.replace("[SS", "[-1")  # SubStream换成-1
    mainPlainText = re.sub(r"(<.+?>)", " ", mainPlainText)  # 滤去标题中的格式控制标签
    mainPlainText = re.sub(r"\.fontcolor\(.+?\)", " ", mainPlainText)  # 滤去标题中的格式控制标签
    mainPlainText = html.unescape(mainPlainText)  # 去除HTML转义字符
    # name
    datas = re.findall(r"'(.+)'.*:\[(\w+),(\w+),(\w+),\"(.+?)\",\"(.+?)\",\"(.+?)\"(,\"(.+?)\")?\]", mainPlainText)
    # 每一行 0-name 1-version 2-id 3-status 4-genre 5-artist 6-title 7废止 8可能是remix
    count = 0
    for line in datas:
        count += 1
        if count > 200:
            db.commit()
            count = 0
        if line[8] != '':
            cursor.execute("INSERT  INTO main (number,name,title,genre,artist,version) VALUES(?,?,?,?,?,?)",
                           (int(line[2]), line[0], line[6] + "  " + line[8], line[4], line[5], int(line[1])))
        else:
            cursor.execute("INSERT  INTO main (number,name,title,genre,artist,version) VALUES(?,?,?,?,?,?)",
                           (int(line[2]), line[0], line[6], line[4], line[5], int(line[1])))
    db.commit()

    # -------------------------------------------------难度表-------------------------------------------------
    cursor.execute('''CREATE TABLE chart
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INT NOT NULL ,
    status  INT NOT NULL ,
    SPB INT NOT NULL ,
    SPN INT NOT NULL ,
    SPH INT NOT NULL ,
    SPA INT NOT NULL ,
    SPL INT NOT NULL ,
    DPN INT NOT NULL ,
    DPH INT NOT NULL ,
    DPA INT NOT NULL ,
    DPL INT NOT NULL 
    )
    ''')
    db.commit()
    chartPlainText = requests.get(TEXTAGE_ARCADE_TRACK_TABLE).content.decode("shift-jis").encode("utf-8").decode(
        "utf-8")
    # 去除十六进制
    # 懒得写了 就这样吧
    chartPlainText = chartPlainText.replace(",A", ",10")
    chartPlainText = chartPlainText.replace(",B", ",11")
    chartPlainText = chartPlainText.replace(",C", ",12")
    chartPlainText = chartPlainText.replace(",D", ",13")
    chartPlainText = chartPlainText.replace(",E", ",14")
    chartPlainText = chartPlainText.replace(",F", ",15")
    datas = re.findall(
        r"'(\w+?)'	:\[(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),"
        r"(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(\w+?)(.+?)?\]", chartPlainText)
    # 'a_amuro'	:[3,0,0,3,1,6,7,A,7, C, 7, 0, 0, 0, 0, 8, 7, B, 7, C, 7, 0, 0],
    #   0         1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24(版本表示）
    # 'absolute'	:[3,3,1,3,1,6,7,8,7,A,7,B,F,0,0,6,7,8,7,B,7,B,F,""],
    # 'eroica'	:[1,0,0,0,0,7,F,A,F, C, F, 0, 0, 0, 0, 7, F, A, F, C, F, 0, 0, ""],
    #   0         1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

    # 0-name 1-status 2-? 3-? 4-spb 5-? 6-spn 7-？8-sph 9-? 10-spa 11-? 12-spl 13-?
    # 14-dpb 15-? 16-dpn 17-? 18-dph 19-? 20-dpa 21-? 22-dpl 23-?
    count = 0
    trackID = 0
    for line in datas:
        count += 1
        if count > 200:
            db.commit()
            count = 0
        cursor.execute("SELECT number from main where name=?", (line[0],))
        for result in cursor:
            trackID = result[0]
        cursor.execute("INSERT INTO chart (number,status,spb,spn,sph,spa,spl,dpn,dph,dpa,dpl)"
                       "Values(?,?,?,?,?,?,?,?,?,?,?)",
                       (trackID, int(line[1]), int(line[4]), int(line[6]), int(line[8]), int(line[10]),
                        int(line[12]), int(line[16]), int(line[18]), int(line[20]), int(line[22])
                        ))
    db.commit()

    db.close()
    await rebuildDatabase.send(f"IIDX歌曲数据库已成功重建。消耗时间：{(time.time() - start):.4}秒。")


@iidxSearch.handle()
async def _(event: Event, message: Message = EventMessage()):
    strs = event.get_plaintext().split(" ", maxsplit=1)
    db = sqlite3.connect("res/iidxdb.db")
    cursor = db.cursor()
    # cursor.execute("SELECT number,title FROM main WHERE title like '%'+?+'%' ORDER BY title LIMIT 20;", (strs[1],))
    cursor.execute("SELECT number,title FROM main WHERE title like ? ORDER BY title LIMIT 20;", ("%" + strs[1] + "%",))
    output = "查询结果\n"
    for row in cursor:
        output += f"id{row[0]} {row[1]}\n"
    await iidxSearch.send(output)
    db.close()


@iidxInfo.handle()
async def _(event: Event, message: Message = EventMessage()):
    text = re.sub(r" +", r" ", event.get_plaintext())
    strs = text.split(" ", maxsplit=2)
    db = sqlite3.connect("res/iidxdb.db")
    cursor = db.cursor()
    output = ""

    cursor.execute("SELECT title,artist,version FROM main WHERE number=?", (int(strs[1]),))
    if cursor.arraysize == 0:
        await iidxInfo.send("没有这样的乐曲。")
        return

    for line in cursor:
        output += f"曲名：{line[0]}\n艺术家：{line[1]}\n版本：{getVersion(line[2])}\n难度：\n"

    # 无指定难度，显示信息。
    if len(strs) <= 2:
        cursor.execute("SELECT * FROM chart WHERE number=?", (int(strs[1]),))
        for line in cursor:
            # 0     id INTEGER PRIMARY KEY AUTOINCREMENT,
            # 1     number INT NOT NULL ,
            # 2     status  INT NOT NULL ,
            # 3     SPB INT NOT NULL ,
            # 4     SPN INT NOT NULL ,
            # 5     SPH INT NOT NULL ,
            # 6     SPA INT NOT NULL ,
            # 7     SPL INT NOT NULL ,
            # 8     DPN INT NOT NULL ,
            # 9     DPH INT NOT NULL ,
            # 10     DPA INT NOT NULL ,
            # 11     DPL INT NOT NULL
            output += f"SP: B:{'无' if line[3] == 0 else line[3]} N:{line[4]} H:{line[5]} A:{'无' if line[6] == 0 else line[6]} L:{'无' if line[7] == 0 else line[7]}\n"
            output += f"DP: N:{line[8]} H:{line[9]} A:{'无' if line[10] == 0 else line[10]} L:{'无' if line[11] == 0 else line[11]}\n"

    else:  # 指定难度。给出链接

        if strs[2].lower() == "dpb":
            await iidxInfo.send("没有此难度谱面")
            return

        diff = 0
        side = 1 if strs[2].lower()[0] == "s" else 2
        chart = strs[2].upper()[2]
        version = 0
        name = ""
        # 获取playstyle及难度。
        cursor.execute("SELECT * FROM chart WHERE number=?", (int(strs[1]),))
        for line in cursor:
            offset = 4 + (4 if strs[2].lower()[0] == 'd' else 0)
            if chart == "B":
                offset -= 1
            elif chart == "N":
                offset += 0
            elif chart == "H":
                offset += 1
            elif chart == "A":
                offset += 2
            elif chart == "L":
                offset += 3

            if line[0] == 0:
                await iidxInfo.send("没有此难度谱面")
                return
            diff = int(line[offset])
        cursor.execute("SELECT name,version FROM main WHERE number=?", (int(strs[1]),))
        for line in cursor:
            name = line[0]
            version = line[1]
        output += strs[2].upper() + str(diff) + '\n' + "谱面链接" + getChartURL(version, side, name, diff, chart)

    await iidxInfo.send(output)
    db.close()

def getVersion(num: int) -> str:
    return "SubStream" if num == -1 else vertbl[num]


# Substream = -1
# side sp=1 dp=2
def getChartURL(version: int, side: int, name: str, diff: int, chart: str) -> str:
    if diff >= 10:
        diff = str(hex(diff)).upper()[2]
    return f"https://www.textage.cc/score/{'s' if version == -1 else version}/{name}.html?" \
           f"{1 if side == 1 else 'D'}{chart}{diff}00"


@iidxhelp.handle()
async def _(event: Event, message: Message = EventMessage()):
    await iidxhelp.send(
        '''/iidx查歌 <str> 查询曲目（当结果过多时，只取前20条）
/iidx查谱 <id> [(S/D)P(B/N/H/A/L)]查询指定谱面。当不指定难度时，给出曲目信息。
/iidx help查看帮助
'''
    )