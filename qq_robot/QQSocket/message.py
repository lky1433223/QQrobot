class Message:
    """
    message类，用于包含一整条消息
    """

    def __init__(self, sender: str):
        self.sender = sender
        self.message_list = []

    def append(self, msg):
        self.message_list.append(msg)

    def __str__(self):
        res_msg = "[{}]".format(self.sender)
        for item in self.message_list:
            res_msg += item['data']
        return res_msg

    def get_sender(self):
        return self.sender

    def get_message_list(self):
        return self.message_list
