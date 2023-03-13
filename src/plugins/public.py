from nonebot import on_command, on_notice
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot, MessageSegment
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor
from src.libraries.image import *


@event_preprocessor
async def preprocessor(bot, event, state):
    if hasattr(event, 'message_type') and event.message_type == "private" and event.sub_type != "friend":
        raise IgnoredException("not reply group temp message")


help = on_command('help')


@help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_str = '''可用命令如下：
help | 查看帮助文档(别看 还没改 看了也没用)
课题列表    | 查看当前课题
课题id<id>    | 查看课题细节
魅力冰城    | 查看哈尔滨机厅的人数(由群聊汇报)
<机厅>几   | 查看该机厅人数
<机厅><人数>    | 上报该机厅人数
[一/二]区吃什么   |  在哈工大找吃的
<机厅>吃什么 |  在机厅找吃的
<机厅>菜单  |  查看这个地方所有的吃的
botconfig addmeal/removemeal 一区/二区 <食物> | 给工大菜单加菜/删菜
botconfig addmeal/removemeal <机厅> <食物> | 给机厅菜单加菜/删菜
梓喵可爱 | 你猜
'''
    await help.send(Message([
        MessageSegment("image", {
            "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
        })
    ]))


async def _group_poke(bot: Bot, event: Event) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke")
    # value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


poke = on_notice(rule=_group_poke, priority=3, block=True)


# @poke.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     if event.__getattribute__('group_id') is None:
#         event.__delattr__('group_id')
#     await poke.send(Message([
#         MessageSegment("at", {"qq": f"{event.user_id}"}),
#         MessageSegment("text", {"qq": "6"})
#     ]))

async def _group_mention(bot: Bot, event: Event) -> bool:
    id = bot.self_id
    if event.post_type == "message":
        value = f"CQ:at,qq={id}" in event.raw_message
    else:
        value = False
    return value

mention = on_notice(rule=_group_mention, priority=3,block=True)


@mention.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
        await poke.send(
            Message([
                MessageSegment("at", {
                    "qq": f"{event.sender_id}"
                })
            ]))


@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
        if event.target_id == event.self_id:
            await poke.send(
                Message([
                    MessageSegment("at", {
                        "qq": f"{event.sender_id}"
                    })
                ]))
        else:
            await poke.send(
                Message([
                    MessageSegment("at", {
                        "qq": f"{event.sender_id}"
                    }, ),
                    MessageSegment("at", {
                        "qq": f"{event.target_id}"
                    }, )
                ]))
