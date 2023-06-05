from .QQSocket import QQApp
from mcdreforged.api.all import *

Config = {
    "information": {
        "ip": "127.0.0.1",
        "port": "8080",
        "group_id": "0"
    },
    "user_list": {},
    "group_list": {}
}
qq: QQApp
config: dict


def on_qq_message(message, server: PluginServerInterface):
    """
    处QQ消息
    """
    server.say(message)
    server.broadcast(message)


def send_qq_message(command_source: CommandSource, keys: dict):
    """
    发送QQ消息
    """
    global qq
    global config
    server: ServerInterface = command_source.get_server()  # 获取server
    res = qq.send_group_message(group_id=config['information']['group_id'], message=keys['message'])
    server.say(text="发送状态{}".format(res))


def on_load(server: PluginServerInterface, old):
    server.logger.info('QQrobot on')
    global config
    global qq
    # 注册配置
    config = server.load_config_simple('config.json', default_config=Config)

    group_list = config['group_list']
    user_list = config['user_list']
    qq = QQApp(ip=config["information"]["ip"], port=int(config["information"]["port"]), group_list=group_list,
               user_list=user_list, callback=on_qq_message, server=server)
    qq.run()

    server.register_help_message(
        '!!qq',
        {
            'en_us': 'qqrobot, try "!!qq send <text>"command',
            'zh_cn': 'QQ机器人，试试"!!qq send <text>"指令'
        }
    )

    builder = SimpleCommandBuilder()
    builder.command('!!qq send <message>', send_qq_message)
    builder.arg('message', GreedyText)
    builder.register(server)


def on_unload(server: PluginServerInterface):
    global qq
    global config
    qq.send_group_message(config['information']['group_id'], "[server] QQrobot stoped")
    qq.stop()


def on_server_start(server: PluginServerInterface):
    qq.send_group_message(config['information']['group_id'], '[server] starting')


def on_server_startup(server: PluginServerInterface):
    global qq
    global config
    response = qq.send_group_message(config['information']['group_id'], '[server] started')


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global qq
    global config
    if (server_return_code != 0):
        qq.send_group_message(config['information']['group_id'],
                              '[server] Server stopped unexpected, is it a server crash?')
    else:
        qq.send_group_message(config['information']['group_id'],
                              '[server] Server stopped safely')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    msg = "[server] {} joined the game".format(player)
    response = qq.send_group_message(config['information']['group_id'], msg)


def on_player_left(server: PluginServerInterface, player: str):
    msg = "[server] {} left the game".format(player)
    response = qq.send_group_message(config['information']['group_id'], msg)


def on_mcdr_stop(server: PluginServerInterface):
    response = qq.send_group_message(config['information']['group_id'], '[MCDR] MCDR stopped')
