# from email import message_from_bytes
from email import message
import time
from tokenize import group
import urllib.request
import urllib.response
import urllib.parse
from flask import Flask, request
from mcdreforged.api.all import *
from typing import Dict, Callable, Any


class Config(Serializable):
    information: Dict[str, str] = {
        'ip': 'http://127.0.0.1:5700',
        'group_id': '0'
    }
    user_list: Dict[str, int] = {
        'ShiinaRikka': 541665621
    }


config: Config


def send_message(id='/send_group_msg', msg=None):
    """
    send message
    :param id : str
    :param msg : str
    :return _UrlopenRet
    """
    global config
    ip = config.information['ip']
    group_id = int(config.information['group_id'])
    url = ip + id
    data = {'group_id': group_id, 'message': msg}
    data = urllib.parse.urlencode(data).encode('utf8')
    request = urllib.request.Request(url, data)
    response = urllib.request.urlopen(request)
    return response


def on_load(server: PluginServerInterface, old):
    server.logger.info('QQrobot on')
    global config
    config = server.load_config_simple('config.json', target_class=Config)

    def exe(func: Callable[[CommandSource, str], Any]):
        return lambda src, ctx: func(src, **ctx)
    server.register_help_message(
        '!!qq',
        {
            'en_us': 'qqrobot',
            'zh_cn': 'QQ机器人'
        }
    )
    server.register_command(
        Literal('!!qq').
        runs(lambda src: src.reply('!!qq send + message')).
        then(
            Literal('send').
            then(
                GreedyText('message').
                runs(lambda src: src.reply('message is sending'))
            )
        )
    )


def on_user_info(server: PluginServerInterface, info: Info):
    txt = info.content
    if txt[0:9] == "!!qq send":
        msg = str("player:") + str(info.player) + ('\n') + \
            str("message:") + str(info.content[9:])
        response = send_message('/send_group_msg', msg)
        server.logger.info(response.read().decode('utf-8'))
        if str(response.reason) == 'OK':
            server.reply(info, text="Message sent successfully")
        else:
            server.reply(info, text="Message sending failed")


def on_server_start(server: PluginServerInterface):
    response = send_message(msg='server starting')


def on_server_startup(server: PluginServerInterface):
    response = send_message(msg='server started')


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if(server_return_code != 0):
        response = send_message(
            msg='Server stopped unexpected, is it a server crash?')
    else:
        response = send_message(msg='Server stopped safely')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    msg = player + ' joined the game'
    response = send_message('/send_group_msg', msg)


def on_player_left(server: PluginServerInterface, player: str):
    msg = player + ' left the game'
    response = send_message('/send_group_msg', msg)


def on_mcdr_stop(server: PluginServerInterface):
    response = send_message('/send_group_msg', 'MCDR stopped')
