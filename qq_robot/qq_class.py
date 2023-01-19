import json
import websocket
from threading import Thread
import queue


class QQSocket:
    def __init__(self, ip="127.0.0.1", port=8080, post_type_list=["message", "message_sent"]):
        self.recv_que = queue.Queue()
        self.post_type_list = post_type_list
        self.ws = websocket.WebSocketApp('ws://{}:{}/'.format(ip, port),
                                         on_message=self.when_message,
                                         on_open=self.when_open,
                                         on_close=self.when_close)

    def run(self):
        thread = Thread(target=self.ws.run_forever)
        thread.setDaemon(True)
        thread.start()

    def when_message(self, ws, message):
        message = json.loads(message)
        if message["post_type"] in self.post_type_list:
            self.recv_que.put(message)

    def when_open(self, ws):
        pass

    def when_close(self, ws):
        pass

    def send(self, action, message, echo=None):
        msg = {
            "action": action,
            "params": message,
        }
        if echo:
            msg["echo"] = echo
        try:
            self.ws.send(json.dumps(msg))
        except Exception:
            return False
        return True

    def get_message(self):
        recv = []
        while not self.recv_que.empty():
            recv.append(self.recv_que.get())
        return recv


if __name__ == "__main__":
    qq = QQSocket()
    qq.run()
    while True:
        msg = input()
        qq.send("send_private_msg", {
            "message_type": "private",
            "user_id": 541665621,
            "message": msg
        })
