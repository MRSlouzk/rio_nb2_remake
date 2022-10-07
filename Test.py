# Python Script Created by MRS
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, Event

a = on_command("a")
@a.handle()
async def _(event: Event):
    print(event.get_type)
    print(event.dict())
    print(event.get_event_description)
    print(event.get_event_name)
    await a.finish()