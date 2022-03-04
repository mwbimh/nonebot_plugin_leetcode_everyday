import nonebot
from nonebot import get_driver, require, on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment, Message

from .config import Config
from .updater import update_today, prepare_page, shutdown_page, set_page_size

global_config = get_driver().config
config = Config.parse_obj(global_config)

scheduler = require("nonebot_plugin_apscheduler").scheduler
register = require("broker").register
subscribe = require("broker").subscribe

driver = nonebot.get_driver()
lce = on_command("每日一题", aliases={"lce"}, rule=to_me(), block=True)
lcem = on_command("管理", aliases={"lcem"}, rule=to_me(), block=True)

question: Message = None
update_flag: bool = True

publish = register(
    name="leetcode每日一题推送服务",
    title="每日一题",
    aliases=["lce", "mryt"],
    hour=config.lce_hour
)
# 自建定时器，可能scheduler更好
# temp = register(
#     name="更新定时器",
#     title="lce_update_timer",
#     hour=f"{config.lce_hour-7}-{config.lce_hour-1}",
#     minute="*/1",
#     no_check=True
# )
# temp("update")


# FIXME:临时用着，等上游apscheduler修好了就删
def beijing2UTC(hour: int):
    hour -= 8
    if hour < 0:
        hour += 24
    return hour


@driver.on_startup
async def prepare():
    await prepare_page(config.lce_size)
    subscribe(0, reset_flag)
    # subscribe("lce_update_timer", update_lce)


@driver.on_shutdown
async def shutdown():
    await shutdown_page()


def reset_flag(a):
    global update_flag
    update_flag = True


@scheduler.scheduled_job(
    "cron",
    hour=str(beijing2UTC(config.lce_hour - 7)) + "-" + str(beijing2UTC(config.lce_hour - 1)),
    minute="*/15",
    id="lce每日更新服务"
)
async def update_lce():
    try:
        global update_flag
        if update_flag:
            q, url = await update_today()
            if q:
                global question
                question = MessageSegment.image(q) + url
                publish([q, url])
                update_flag = False
    except Exception as e:
        print(driver.bots)
        for user in config.lce_admin["users"]:
            await nonebot.get_bot().send_private_msg(
                user_id=user,
                message="lce更新时发生异常\n" + e.__str__()
            )
        for group in config.lce_admin["groups"]:
            await nonebot.get_bot().send_group_msg(
                group_id=group,
                message="lce更新时发生异常\n" + e.__str__()
            )
        update_flag = True


@lcem.receive()
async def manage(event: MessageEvent):
    if event is GroupMessageEvent:
        if event.group_id not in config.lce_admin["groups"]:
            await lcem.finish("非管理员群，停止指令处理")
    elif not event.get_user_id() in config.lce_admin["users"]:
        await lcem.finish("非管理员用户，停止指令处理")
    msg: str = event.get_plaintext()
    op: list = msg.split(" ")
    if len(op) < 1:
        pass
    elif op[0] in ["更新", "update", "更"]:
        global update_flag
        update_flag = True
        await update_lce()
    elif op[0] in ["结束", "finish", "算了", "end", "没了", "完"]:
        await lcem.finish("已结束事件处理")
        return
    elif op[0] in ["看看", "状态", "看", "status"]:
        await lcem.finish(check())
    elif len(op) < 3:
        await lcem.reject(f"指令错误\n错误指令为:\n{msg}\n请重新输入指令")
    elif op[0] in ["大小", "调整大小", "size", "adj"]:
        try:
            await set_size(op[1], op[2])
        except Exception as e:
            lcem.reject(f"参数错误\n请重新输入指令")
    else:
        await lcem.reject(f"指令错误\n错误指令为:\n{msg}\n请重新输入指令")
    await lcem.finish("指令处理完毕")


async def set_size(w: int, h: int):
    config.lce_size["width"] = w
    config.lce_size["height"] = h
    await set_page_size(config.lce_size)


def check():
    status: str = "lce运行中"
    status += f"\n更新时间:{config.lce_hour}点"
    status += f"\n大小:{config.lce_size['width']}x{config.lce_size['height']}"

    if "users" in config.lce_admin:
        status += "\n管理员用户:"
        for u in config.lce_admin["users"]:
            status += f"\n{u}"

    if "groups" in config.lce_admin:
        status += "\n管理员群:"
        for g in config.lce_admin["groups"]:
            status += f"\n{g}"

    status += "\n以上"
    return status


@lce.handle()
async def send():
    global question
    if question is None:
        global update_flag
        update_flag = True
        await update_lce()
    await lce.finish(question)
