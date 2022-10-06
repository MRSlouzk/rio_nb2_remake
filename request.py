# Python Script Created by MRS
"""
    好友申请插件
"""
from nonebot import on_request, on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, Bot, Event, FriendRequestEvent
from nonebot.log import logger
from nonebot.permission import SUPERUSER

import json

def _checker(event: Event):
    return isinstance(event, FriendRequestEvent)

friend = on_request(rule = _checker, priority=1, block=False)
@friend.handle()
async def _(event: Event):
    data = json.loads(event.json())
    flag = data["flag"]
    qq = data["user_id"]
    comment = data["comment"]

    with open("./data/request/friend_request.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    dic = dict()
    dic[str(qq)] = {"flag": flag, "comment": comment}
    content.update(dic)
    with open("./data/request/friend_request.json", "w", encoding="utf-8") as f2:
        json.dump(content, f2, indent=4)

    logger.info(Message("写入成功!"))

read_all_request = on_command("查看好友请求", permission=SUPERUSER, priority=19, block=False)
@read_all_request.handle()
async def _(bot: Bot):
    with open("./data/request/friend_request.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    count = 0
    for i in content.keys():
        qq = i
        comment = content[i]["comment"]
        count += 1

        info = await bot.get_stranger_info(user_id = qq)
        name = info["nickname"]
        await read_all_request.send(Message(f"好友请求{count}\nqq:{qq}\n昵称:{name}\n备注:{comment}\n"))
    await read_all_request.finish()

clear_all_request = on_command("清空好友请求", permission=SUPERUSER, priority=19, block=False)
@clear_all_request.handle()
async def _():
    with open("./data/request/friend_request.json", "w", encoding="utf-8") as f:
        content = {}
        json.dump(content, f, indent=4)
    await clear_all_request.finish("清理完成!")

handle_request = on_command("处理好友请求", permission=SUPERUSER, priority=19, block=False)
@handle_request.handle()
async def _(event: Event, bot: Bot, args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    if(len(arg) != 2):
        await handle_request.finish("参数数量错误!格式:/处理好友请求 qq 1/0(1同意0拒绝)")
    with open("./data/request/friend_request.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    try:
        data = content[arg[0]]
    except KeyError:
        await handle_request.finish(Message("不存在该qq的请求消息!"))
    flag = data["flag"]
    if(arg[1] == "1"):
        await bot.set_friend_add_request(flag=flag, approve=True, remark="")
        await handle_request.finish("已同意申请")
    elif(arg[1] == "0"):
        await bot.set_friend_add_request(flag=flag, approve=False, remark="管理员拒绝了你的申请")
        await handle_request.finish("已拒绝申请")
    else:
        await handle_request.finish("未选择是否同意!")