from mcdreforged.api.all import *
from typing import Dict, Callable, Any
from qq_class import QQSocket
__all__ = ['qq_class']

class Config(Serializable):
    information: Dict = {
        "ip": "127.0.0.1",
        "port": 8080,
        "group_id": '0'
    }
    user_list: Dict[str, int] = {
    }


config: Config
qq: QQSocket


def send_group_message(message=None):
    """
    """
    global config
    global qq
    msg = {
        "group_id": config.information("group_id"),
        "message": message
    }
    return qq.send("send_group_msg", msg)


def on_load(server: PluginServerInterface, old):
    server.logger.info('QQrobot on')
    global config
    global qq
    config = server.load_config_simple('config.json', target_class=Config)
    qq = QQSocket(config["ip"], config["port"])

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
        msg = "[{}] {}".format(info.player, info.content[9:])
        response = send_group_message(msg)
        server.logger.info("sending", msg)
        if str(response) == 'OK':
            server.reply(info, text="Message sent successfully")
        else:
            server.reply(info, text="Message sending failed")


def on_server_start(server: PluginServerInterface):
    response = send_group_message('[server] starting')


def on_server_startup(server: PluginServerInterface):
    response = send_group_message('[server] started')


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if (server_return_code != 0):
        response = send_group_message(
            '[server] Server stopped unexpected, is it a server crash?')
    else:
        response = send_group_message('[server] Server stopped safely')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    msg = "[server] {} joined the game".format(player)
    response = send_group_message(msg)


def on_player_left(server: PluginServerInterface, player: str):
    msg = "[server] {} joined the game".format(player)
    response = send_group_message(msg)


def on_mcdr_stop(server: PluginServerInterface):
    response = send_group_message('[MCDR] MCDR stopped')
