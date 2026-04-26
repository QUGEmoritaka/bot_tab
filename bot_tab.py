# -*- coding: utf-8 -*-
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'bot_tab',
    'version': '1.0.1',
    'name': 'BotTab',
    'description': '自动将 bot_ 开头的玩家加入 BotTeam（静默），并在 Tab 栏显示前缀',
    'author': 'QUGEmoritaka',
    'link': 'https://github.com/QUGEmoritaka/bot_tab'
}

BOT_PREFIX = 'bot_'
BOT_TEAM_NAME = 'BotTeam'
BOT_TAB_PREFIX = '§b§l[Bot] §r'

team_initialized = False
pending_silent_join = set()   # 用于记录即将静默加入的玩家


def on_server_startup(server: ServerInterface):
    """服务器启动后创建队伍（如已存在则跳过）"""
    global team_initialized
    if team_initialized:
        return
    try:
        server.execute(f'team add {BOT_TEAM_NAME}')
    except:
        pass
    server.execute(f'team modify {BOT_TEAM_NAME} prefix {BOT_TAB_PREFIX}')
    server.execute(f'team modify {BOT_TEAM_NAME} color aqua')
    team_initialized = True


def on_player_joined(server: ServerInterface, player: str, info: Info):
    """玩家加入时，若名字以 bot_ 开头则静默加入 BotTeam"""
    if player.lower().startswith(BOT_PREFIX.lower()):
        # 将玩家加入待屏蔽集合，然后执行加入命令
        pending_silent_join.add(player.lower())
        server.execute(f'team join {BOT_TEAM_NAME} {player}')


def on_info(server: ServerInterface, info: Info):
    """拦截队伍加入提示，实现静默加入"""
    if not info.is_from_server:
        return
    # 匹配服务器输出的加入队伍消息：通常为 "xxx joined team BotTeam"
    # 不同服务器语言可能略有差异，这里用简单关键字判断
    content = info.content
    if 'joined team' not in content and '加入了队伍' not in content:
        return

    for player_lower in list(pending_silent_join):
        # 检查消息是否包含该玩家名和队伍名
        if player_lower in content.lower() and BOT_TEAM_NAME.lower() in content.lower():
            pending_silent_join.remove(player_lower)
            # 拦截此消息，不广播给玩家
            info.cancel_send_to_server()
            break