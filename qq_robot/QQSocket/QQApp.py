import json
import threading
import time
import uuid

import websocket
from .message_dealer import MessageDealer
from .message import Message
import requests

class QQApp:
    def __init__(self, callback, group_list=None, user_list=None, ip: str = "127.0.0.1", port: int = 8080, **kwargs):

        self.Thread = None
        if user_list is None:
            user_list = {}
        if group_list is None:
            group_list = [int]
        self.url = "ws://{}:{}/".format(ip, port)
        self.ws = websocket.WebSocketApp(
            url=self.url,
            on_message=self.when_message,
            on_open=self.when_open,
            on_close=self.when_close
        )
        self.group_list = group_list
        self.user_list = user_list
        self.callback = callback
        self.Dealear = MessageDealer(user_list=self.user_list)
        self.wating_queue = set()  # 发送消息后的等待列表
        self.finished_list = {}
        self.Thread: threading.Thread
        self.kwargs = kwargs

    def deal_message(self, message):
        message = json.loads(message)
        if 'post_type' in message:
            if message['post_type'] == 'message':
                if message['message_type'] == 'group':
                    if message['group_id'] in self.group_list:
                        user = str(message['user_id'])
                        if user in self.user_list:
                            user = self.user_list[user]
                        res_message = Message(user)
                        self.Dealear.deal_message(message['message'], res_message)
                        self.callback(res_message, **self.kwargs)
        elif 'status' in message:
            if 'echo' in message and message['echo'] in self.wating_queue:
                msg_id = message['echo']
                self.finished_list[msg_id] = message
                self.wating_queue.discard(msg_id)

    def send(self, message: dict):
        if type(message) is not dict:
            raise TypeError
        # TODO:websock
        url = 'http://192.168.3.205:5700/send_group_msg'

        response = requests.post(url, json=message['params'])
        # self.ws.send(json.dumps(message))
        return response
    def send_group_message(self, group_id: int, message: str) -> bool:
        """
        发送群消息并返回是否发送成功
        :param group_id:
        :param message:
        :return:
        """
        msg_id = str(uuid.uuid4())
        msg = {
            'action': 'get_login_info',
            'params': {
                'group_id': group_id,
                'message': message,
                'auto_escape': True
            },
            'echo': str(msg_id)
        }
        self.wating_queue.add(msg_id)
        self.send(msg)

        start_time = time.time()
        while time.time() - start_time < 20:  # 循环20秒
            if msg_id in self.finished_list:
                message = self.finished_list[msg_id]
                status = message['status']
                self.finished_list.pop(msg_id)
                return status == 'ok'
            time.sleep(1)  # 延迟1秒
        if msg_id in self.wating_queue:
            self.wating_queue.discard(msg_id)
        if msg_id in self.finished_list:
            self.finished_list.pop(msg_id)
        return False

    def when_message(self, ws, message):
        self.deal_message(message)

    def when_open(self, ws):
        print("opened")
        pass

    def when_close(self, ws):
        print("closed")
        pass

    def run(self):
        self.Thread = threading.Thread(target=self.ws.run_forever)
        self.Thread.daemon = True
        self.Thread.name = 'QQAPP'
        self.Thread.start()
        time.sleep(5)  # 等待五秒确保线程已经启动

    def stop(self):
        self.ws.close()


if __name__ == "__main__":
    webapp = QQApp(ip="192.168.3.205", port=8080, group_list=[1067245310, 839640112],
                   user_list={"541665621": "ShiinaRikka"}, callback=lambda x: print(x))
    webapp.run()

    res = webapp.send_group_message(839640112, "1")
    while True:
        msg = input("输入消息")
        res = webapp.send_group_message(839640112, msg)
        print(res)
