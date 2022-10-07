# Python Script Created by MRS
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, Bot, GroupMessageEvent

sign = on_command("打卡")

@sign.handle()
async def sig(event: GroupMessageEvent, bot: Bot):
    try:
        await bot.call_api("send_group_sign", group_id=event.group_id)
        await sign.finish("打卡成功!")
    except Exception as e:
        print(e)
        await sign.finish()

import nonebot
from nonebot import require

he = require("nonebot_plugin_apscheduler").scheduler

@he.scheduled_job("cron", hour='00', minute='00', second='00', id="test")
async def test():
    (bot,) = nonebot.get_bots().values()
    await bot.call_api(
        "send_group_sign",
        group_id=684869122
    )
    await bot.send_msg(
        message_type="group",
        group_id=684869122,
        message="打卡完成!"
    )