from .QQSocket import QQApp
from mcdreforged.api.all import *
from .QQSocket import Message

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


def on_qq_message(message: Message, server: PluginServerInterface):
    """
    处QQ消息
    """
    # TODO:链接
    res_msg = RTextBase.format('[{}]', RText(message.get_sender(), color=RColor.light_purple))
    msg_list = message.get_message_list()
    tmp = RAction.open_url
    for msg in msg_list:
        if msg['type'] == 'image':
            text = RText('>图片 点我<', color=RColor.blue).set_click_event(RAction.open_url, msg['data'])
            res_msg = RTextBase.format('{}{}', res_msg, text)
        else:
            res_msg = RTextBase.format('{}{}', res_msg, RText(msg['data']))
    # /tellraw @a {"text":"","extra":[{"text":"网站名称或者你想说的话","color":"颜色","bold":"true","clickEvent":{"action":"open_url","value":"网站"}}]}
    server.broadcast(res_msg)


def qq_help(command_source: InfoCommandSource, keys: dict):
    click_event = RText('点我发消息', color=RColor.green).set_click_event(RAction.suggest_command, '!!qq send ')

    text = RTextBase.format('[{}]', click_event)

    server = command_source.get_server()
    server.broadcast(text)


def send_qq_message(command_source: InfoCommandSource, keys: dict):
    """
    发送QQ消息
    """
    global qq
    global config

    # server: ServerInterface = command_source.get_server()  # 获取server

    # 获取用户
    user = "console"
    if command_source.is_player:
        info = command_source.get_info()  # InfoCommandSource是CommandSource的子类，可以get_info
        user = info.player
    msg = "[{}]{}".format(user, keys['message'])

    # 对用户进行发送情况反馈
    res = False
    res_status = ""
    try:
        res = qq.send_group_message(group_id=config['information']['group_id'], message=msg)
    except Exception as err:
        res = False
        res_status = str(err)
    finally:
        command_source.reply(message="发送状态{} {}".format(res, res_status))


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
    builder.command('!!qq', qq_help)
    builder.command('!!qq send <message>', send_qq_message)
    builder.arg('message', GreedyText)
    builder.register(server)

    qq.send_group_message(config['information']['group_id'], "[server] QQrobot started")


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
    if server_return_code != 0:
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
