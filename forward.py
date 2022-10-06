# Python Script Created by MRS
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, Message
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg, ArgPlainText

import asyncio

SU = {3237231778, 3569965096}

#TODO 读取SU列表并判断
def isPrivateSU(event: Event):
    # return isinstance(event, PrivateMessageEvent) and (event.user_id in SU)
    return event.get_user_id in SU

forward = on_command("转发", priority=49, block=False)

@forward.handle()
async def _(args: Message = CommandArg()):
    global message_lst
    arg = args.extract_plain_text().split()
    length = len(arg)
    if(length==0):
        await forward.finish(Message("无消息可转发!"))
    elif(length > 0 and length <= 8):
        message_lst = arg.copy()
    else:
        await forward.finish(Message("消息内容过多，容易风控，已取消发送"))
    #TODO 添加图片转发适配

@forward.got("replyKey", prompt="请输入\"消息类型 群号/QQ号\",消息类型有group与private")
async def _(bot: Bot, key: Message = ArgPlainText("replyKey")):
    strList = key.split(" ")
    leng = len(strList)
    if(leng == 2):
        if(strList[0] == "private"):
            for i in message_lst:
                try:
                    await bot.send_private_msg(user_id=int(strList[1]), message=Message(i))
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(e)
            await forward.finish()
        elif(strList[0] == "group"):
            for i in message_lst:
                try:
                    await bot.send_group_msg(group_id=int(strList[1]), message=Message(i))
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(e)
            await forward.finish()
        elif(strList[0] == "global"):
            await bot.get_group_list() #TODO 群广播
    elif(leng == 1):
        if(strList[0] == 'n'):
            await forward.finish()
    await forward.reject(prompt="参数错误,请重新输入(n以退出)")