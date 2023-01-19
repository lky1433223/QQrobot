from mcdreforged.api.all import *
from typing import Dict, Callable, Any
from qq_robot.qq_class import QQSocket
from threading import Thread

__all__ = ['qq_class']

Config = {
    "information": {
        "ip": "127.0.0.1",
        "port": "8080",
        "group_id": "0"
    },
    "user_list": {}
}

config: dict
qq: QQSocket
dealing = False


def send_group_message(message=None):
    """
    """
    global config
    global qq
    msg = {
        "group_id": config["information"]["group_id"],
        "message": message
    }
    return qq.send("send_group_msg", msg)


def msg_dealer(qq: QQSocket, config: dict, server: PluginServerInterface):
    global dealing
    while dealing:
        message_list = qq.get_message()
        for message in message_list:
            # print("in msg_dealer", message)
            if message["message_type"] == "group" and str(message["group_id"]) == config["information"]["group_id"]:
                print("in group")
                user = None
                if message["user_id"] in config["user_list"]:
                    user = config["user_list"][message["user_id"]]
                else:
                    if message["sender"]["card"]:
                        user = message["sender"]["card"]
                    else:
                        user = message["sender"]["nickname"]
                server.broadcast("[{}]{}".format(user, message["message"]))


def on_load(server: PluginServerInterface, old):
    server.logger.info('QQrobot on')
    global config
    global qq
    global dealing
    config = server.load_config_simple('config.json', default_config=Config)
    qq = QQSocket(config["information"]["ip"], int(config["information"]["port"]))
    qq.run()
    dealing = True
    msg_dealer_thread = Thread(target=msg_dealer, args=(qq, config, server))
    msg_dealer_thread.setDaemon(True)
    msg_dealer_thread.setName("msg_dealer_thread")
    msg_dealer_thread.start()

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


def on_unload(server: PluginServerInterface):
    global dealing
    dealing = False


def on_user_info(server: PluginServerInterface, info: Info):
    txt = info.content
    if txt[0:9] == "!!qq send":
        msg = "[{}]{}".format(str(info.player), str(info.content[9:]))
        response = send_group_message(msg)
        server.logger.info("sending" + msg)
        if response:
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
    msg = "[server] {} left the game".format(player)
    response = send_group_message(msg)


def on_mcdr_stop(server: PluginServerInterface):
    response = send_group_message('[MCDR] MCDR stopped')
