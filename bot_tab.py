# -*- coding: utf-8 -*-
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'bot_tab',
    'version': '1.0.0',
    'name': 'BotTab',
    'description': '',
    'author': 'QUGEmoritaka',
    'link': 'https://github.com/QUGEmoritaka/bot_tab'
}

BOT_PREFIX = 'bot_'
BOT_TEAM_NAME = 'BotTeam'
BOT_TAB_PREFIX = '§b§l[Bot] §r'

team_initialized = False

# 服务器启动后初始化队伍
def on_server_startup(server: ServerInterface):
    global team_initialized
    if not team_initialized:
        server.execute(f'team add {BOT_TEAM_NAME}')
        server.execute(f'team modify {BOT_TEAM_NAME} prefix {BOT_TAB_PREFIX}')
        server.execute(f'team modify {BOT_TEAM_NAME} color aqua')
        team_initialized = True

# 玩家加入，静默加入队伍，不显示提示
def on_player_joined(server: ServerInterface, player: str, info: Info):
    if player.lower().startswith(BOT_PREFIX.lower()):
        # 加 silent 1 彻底关闭加入提示
        server.execute(f'team join {BOT_TEAM_NAME} {player} silent 1')