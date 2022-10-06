# Python Script Created by MRS
from nonebot.params import CommandArg, Arg, ArgStr
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event, Bot
from nonebot import on_command, on_regex, get_driver, Config
from nonebot.permission import SUPERUSER
from nonebot.exception import ActionFailed

import json, re, requests

from .data_handle import Handle
from .utils import *

config = Config.parse_obj(get_driver().config.dict())
relative_url = "./data/cave/"
abstract_url = "file:///home/ubuntu/NewRio/newRio/data/cave/"

cave_add = on_regex(r"#cave-add$", priority=19, block=True)
cave = on_command("cave", priority=20, block=False)
cave_del = on_command("cave-del", priority=20, block=False, permission=SUPERUSER)
cave_show = on_command("cave-show", priority=20, block=False, permission=SUPERUSER)

@cave_show.handle()
async def _(args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    if(len(arg) == 0):
        await cave_show.finish("请输入参数哦~")
    elif(len(arg) == 1):
        try:
            info = Handle.read_cave(int(arg[0]))
        except KeyError:
            await cave_show.finish("不存在该cave!")
        if (info[0] == "text"):
            msg = Message(info[2] + f"\n\n----作者:{info[1]}")
            await cave_show.finish(msg)
        elif (info[0] == "image"):
            msg = MessageSegment.image(info[2]) + Message(f"\n\n----作者:{info[1]}")
            await cave_show.finish(msg)
        else:
            await cave_show.finish("Json文件错误,请检查文件")
    else:
        await cave_show.finish("暂时不支持多参数查看~")

@cave_del.handle()
async def _(args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    if(len(arg) == 0):
        await cave_del.finish("请输入要删除的cave序号!")
    else:
        for i in arg:
            try:
                Handle.del_cave(int(i))
            except KeyError:
                await cave_del.send("序号: "+str(i)+" 不存在!")
                continue
            except FileNotFoundError:
                await cave_del.send("删除序号:" + str(i) + "时不存在图片文件!")
                continue
        await cave_del.finish("删除成功!")

@cave_add.handle()
async def _(event: Event, bot: Bot):
    data = json.loads(event.json())
    isReply = False
    for i in data["original_message"]:
        if(i["type"] == "reply"):
            isReply = True
    if(isReply):
        msg_id = data["original_message"][0]["data"]["id"]
        msg = await bot.get_msg(message_id = msg_id)
        content = msg["message"]
        qq = int(event.get_user_id())
        res = Handle.checkMsg(qq, content)
        if(res == -1):
            await cave_add.finish("无法加入cave,请检查图片是否有效")
        await cave_add.finish(res)
        # if (content.count("CQ") >= 2):
        #     await cave_add.finish("目前暂不支持同一个消息添加两张以上的图片!")
        # elif (content.count("CQ") == 1):
        #     pattern = re.compile(r"CQ:image(.+?)url=(?P<url>.*?)]")
        #     match = re.search(pattern, content)
        #     if (match is None):
        #         await cave_add.finish("不支持的消息类型!应当为图片/纯文字")
        #     url = match.group("url")
        #     try:
        #         Handle.add_image(int(event.get_user_id()), url)
        #         await cave_add.finish("添加成功!")
        #     except ConnectionError:
        #         await cave_add.send("连接超时!无法保存图片...")
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         await cave_add.finish()
        # else:
        #     try:
        #         Handle.add_text(int(event.get_user_id()), content)
        #         await cave_add.finish("添加成功!")
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         await cave_add.finish()
        # await cave_add.finish()

@cave_add.got("cave", prompt="请发送要加入cave当中的消息")
async def _(event: Event, arg: str = ArgStr("cave")):
    if(arg.count("CQ") >= 2):
        await cave_add.finish("目前暂不支持添加两条以上的图片!")
    elif(arg.count("CQ") == 1):
        qq = int(event.get_user_id())
        res = Handle.checkMsg(qq, arg)
        if (res == -1):
            await cave_add.finish("无法加入cave,请检查图片是否有效")
        await cave_add.finish(res)
    #     patt = re.compile(r"\[CQ=(.*?)]")
    #     b = re.sub(patt, "", arg)
    #     if(b is not None):
    #         await cave_add.finish("目前暂不支持图片+文字消息")
    #
    #     pattern = re.compile(r"CQ:image(.+?)url=(?P<url>.*?)]")
    #     match = re.search(pattern, arg)
    #     if(match is None):
    #         await cave_add.finish("不支持的消息类型!应当为纯图片/纯文字")
    #     url = match.group("url")
    #     try:
    #         Handle.add_image(int(event.get_user_id()), url)
    #         await cave_add.finish("添加成功!")
    #     except ConnectionError:
    #         await cave_add.send("连接超时!无法保存图片...")
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         await cave_add.finish()
    # else:
    #     try:
    #         Handle.add_text(int(event.get_user_id()), arg)
    #         await cave_add.finish("添加成功!")
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         await cave_add.finish()
    # await cave_add.finish()

@cave.handle()
async def _(bot: Bot, args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    if(len(arg) == 1):
        if(arg[0] == "帮助"):
            await cave.finish("cave插件说明:\ncave类似于留言板,所有人可以向里面存储一些乱七八糟的图片或文字,并且所有人都可以从里面随机抽取来看\n使用:\n/cave可以随机抽取内容\n/cave-add可以添加新的内容(非管理员添加后需要SU权限组进行审批后方可使用)")
        if(arg[0] == "SU"):
            await cave.finish("cave管理员帮助:\n/cave-show可以查看指定的内容\n/cave-del可以删除指定内容\n/show-all-temp展示所有未审核cave\n/clear-all-temp清除所有未审核temp\n/decide-cave用于审批")
    try:
        lst = Handle.choose_cave()
    except Exception as e:
        await cave.finish(str(e))
    info = await bot.get_stranger_info(user_id=lst[1], no_cache=False)
    name = info["nickname"]
    if(lst[0] == "text"):
        msg = Message(lst[2] + f"\n\n----作者:{name}({lst[1]})\n====编号:{lst[3]}")
        await cave.finish(msg)
    elif(lst[0] == "image"):
        msg = MessageSegment.image(lst[2]) + Message(f"\n\n----作者:{name}({lst[1]})\n====编号:{lst[3]}")
        await cave.finish(msg)

# max_num = on_command("show-max", priority=20, block=False)
# @max_num.handle()
# async def _():
#=================================================#
def _event(event: Event):
    return isinstance(event, GroupMessageEvent)

show_all_caves = on_command("show-all-temp", rule=_event, priority=1, block=True, permission=SUPERUSER)
@show_all_caves.handle()
async def _(event: Event, bot: Bot):
    cave_lst = Handle._show_temp_cave()
    if(cave_lst == -1):
        await show_all_caves.finish("没有临时cave!")
    msg = []
    for i in cave_lst:
        if(i[0] == "image"):
            sig_msg = Message()
            qq = i[1]
            tid = i[3]
            info = await bot.get_stranger_info(user_id=i[1], no_cache=False)
            name = info["nickname"]
            sig_msg += MessageSegment.image(i[2]) + Message(f"----作者: {name}({qq})\n====作品编号:{tid}")
        else:
            sig_msg = Message()
            qq = i[1]
            tid = i[3]
            content = i[2]
            info = await bot.get_stranger_info(user_id=i[1], no_cache=False)
            name = info["nickname"]
            sig_msg += Message(f"{content}\n----作者: {name}({qq})\n====作品编号:{tid}")
        msg.append(sig_msg)
    try:
        await send_forward_msg(bot, event, "凛绪酱", str(bot.self_id), msg)
        await show_all_caves.finish()
    except ActionFailed:
        await show_all_caves.finish("消息可能被封控~")

clear_all_caves = on_command("clear-all-temp", priority=1, block=True, permission=SUPERUSER)
@clear_all_caves.handle()
async def _():
    res = Handle._clear_temp_cave()
    await clear_all_caves.finish(res)

decide_cave = on_command("decide-cave", priority=1, block=True, permission=SUPERUSER)
@decide_cave.handle()
async def _(args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    if(len(arg) == 0):
        await decide_cave.finish("参数数量过少!")
    elif (len(arg) == 1):
        if(arg[0] == "帮助"):
            await decide_cave.finish("/decide-cave用于审批临时cave\n有两个参数:\n第一个参数为cave序号\n第二个参数为0/1(0否1是)")
        await decide_cave.finish()
    elif(len(arg) == 2):
        if(arg[1] == "0"):
            res = Handle._choose_temp_cave(int(arg[0]), False)
        elif(arg[1] == "1"):
            res = Handle._choose_temp_cave(int(arg[0]), True)
        else:
            await decide_cave.finish("判断参数无效")

        await decide_cave.finish(res)
    else:
        await decide_cave.finish("参数数量过多!")

all_agree = on_command("all-pass", priority=1, block=True, permission=SUPERUSER)
@all_agree.handle()
async def _():
    res = Handle._agree_all_cave()
    await all_agree.finish(res)