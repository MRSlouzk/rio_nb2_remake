# Python Script Created by MRS
from nonebot import on_command
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event

import random, datetime
from nonebot.typing import T_State

guess = on_command("猜数字", priority=10, block=False)

@guess.handle()
async def _(state: T_State, args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    global num
    state.update({"times": 0})
    if(len(arg) == 0):
        num = random.randint(0, 100)
    elif(len(arg) == 1):
        if(arg[0].isdigit()):
            if(int(arg[0])<=10):
                await guess.finish(Message("参数过小,请重新输入!"))
            elif(int(arg[0])>=100000):
                await guess.finish(Message("参数过大,请重新输入!"))
            else:
                num = random.randint(0, int(arg[0]))
        else:
            if(arg[0] == "帮助"):
                await guess.finish(Message("猜数字插件使用说明\n1./猜数字 数字1 :生成0~数字1内任意整数\n2./猜数字 数字1 数字2 :生成数字1~数字2内任意整数\n注意!限时100s,超时则游戏自动结束"))
            else:
                await guess.finish(Message("参数错误!"))
    elif(len(arg) == 2):
        if(arg[0].isdigit() and arg[1].isdigit()):
            if(int(arg[0]) >= (int(arg[1]) - 10) or int(arg[0]) < 0 or int(arg[1]) >= 100000):
                await guess.finish(Message("参数越界,请重新输入!"))
            else:
                num = random.randint(int(arg[0]), int(arg[1]))
        else:
            await guess.finish(Message("参数错误!"))
    else:
        await guess.finish(Message("参数错误!"))
    guess.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=100)

@guess.got("num", prompt=f"请输入猜的数字")
async def _(state: T_State, event: Event, key: str = ArgStr("num")):
    if(not key.isdigit()):
        if(key == "exit"):
            await guess.finish(Message("已结束猜数字~"))
        else:
            now = state.get("times") + 1
            state.update({"times": now})
            await guess.reject(prompt="非法字符!请输入数字!")
    else:
        if(state.get("times") >= 8):
            await guess.finish(Message("机会用完了,很遗憾没答对,请再接再厉!"))
        else:
            if(int(key) == num):
                await guess.finish(Message("恭喜你答对了!\n(PS:后续引入金币系统等后再加入奖励)"))
            elif(int(key) < num):
                now = state.get("times") + 1
                state.update({"times": now})
                msg = MessageSegment.at(event.get_user_id()) + Message(f"数字太小了!还剩{9 - now}次机会")
                await guess.reject(prompt=msg)
            elif (int(key) > num):
                now = state.get("times") + 1
                state.update({"times": now})
                msg = MessageSegment.at(event.get_user_id()) + Message(f"数字太小了!还剩{9 - now}次机会")
                await guess.reject(prompt=msg)