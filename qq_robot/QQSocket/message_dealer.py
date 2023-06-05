"""
处理CQ格式消息
参考文档https://docs.go-cqhttp.org/cqcode
"""


class MessageDealer:
    def __init__(self, user_list=None):
        if user_list is None:
            user_list = {}
        self.dealer_list: {str: any} = {
            'face': self.deal_message_face,
            'record': self.deal_message_record,
            'at': self.deal_message_at,
            'share': self.deal_message_share,
            'image': self.deal_message_image,
            'text': self.deal_message_text
        }

        # 用户qqid和用户名对照表
        self.user_list: {str: str} = user_list

    def deal_message(self, message: list[dict]):
        res_message = ""
        for msg in message:
            if msg['type'] in self.dealer_list:
                apd_msg = "{}".format(self.dealer_list[msg['type']](msg))
                res_message += apd_msg
            else:
                res_message += '[未知消息]'
        return res_message

    def deal_message_face(self, message: dict):
        """
        处理表情消息
        :param message:
        :return:
        """
        res_message = message['data']['id']
        res_message = "[表情{}]".format(res_message)
        return res_message

    def deal_message_record(self, message: dict):
        """
        处理语音消息
        :param message:
        :return:
        """
        res_message = message['data']['file']
        res_message = "[语音消息]"
        return res_message

    def deal_message_at(self, message: dict):
        """
        处理at消息
        :param message:
        :return:
        """
        res_message = "@"
        at_message = message['data']['qq']
        if at_message == 'all':
            res_message += "all"
        elif at_message in self.user_list:
            res_message += str(self.user_list[at_message])
        else:
            res_message += str(at_message)
        return res_message

    def deal_message_share(self, message):
        """
        处理连接分享
        :return:
        """
        url = message['data']['url']
        title = message['data']['title']
        res_message = "分享了：{}，链接{}".format(url, title)
        return res_message

    def deal_message_image(self, message):
        """
        处理图片消息
        :param message:
        :return:
        """
        url = message['data']['url']
        res_message = "[图片，请点击链接 {} 查看]".format(url)
        return res_message

    def deal_message_text(self, message):
        """
        处理文字消息
        :param message:
        :return:
        """
        return message['data']['text']
