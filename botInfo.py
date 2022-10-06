# Python Script Created by MRS
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot import on_command

info = on_command("help",aliases={"使用说明"}, priority=50, block=False)

@info.handle()
async def _():
    await info.finish(MessageSegment.image(file="file:///home/ubuntu/NewRio/newRio/src/plugins/img/info.png"))