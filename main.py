import time
import logging
from queue import Queue
import os
import sys
sys.path.append(os.path.realpath('.'))
from WeChatPYAPI import WeChatPYApi
import requests
URL='http://api.qingyunke.com/api.php?key=free&appid=0&msg='
# 当前目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO)  # 日志器
msg_queue = Queue()  # 消息队列
def on_message(msg):
    """消息回调"""
    print(msg)
    msg_queue.put(msg)
def on_exit(wx_id):
    """退出事件回调"""
    print("已退出：{}".format(wx_id))
def main():
    #help(WeChatPYApi)
    # 实例化api对象
    w = WeChatPYApi(msg_callback=on_message, exit_callback=on_exit, logger=logging)
    # 启动微信
    w.start_wx()
    # w.start_wx(path=os.path.join(BASE_DIR, "login_qrcode.png"))  # 保存登录二维码
    # 这里需要阻塞，等待获取个人信息
    while not w.get_self_info():
        time.sleep(5)
    my_info = w.get_self_info()
    self_wx = my_info["wx_id"]
    print("登陆成功！")
    print(my_info)

    # 拉取列表（好友/群/公众号等）第一次拉取可能会阻塞，可以自行做异步处理
    # 好友列表：pull_type = 1
    # 群列表：pull_type = 2
    # 公众号列表：pull_type = 3
    # 其他：pull_type = 4
    lists = w.pull_list(self_wx=self_wx, pull_type=1)
    print(lists)
    # 获取群成员列表
    # lists = w.get_chat_room_members(self_wx=self_wx, to_chat_room="123@chatroom")
    # print(lists)
    # 发送文本消息
    #w.send_text(self_wx=self_wx, to_wx="filehelper", msg='作者QQ:\r437382693')
    time.sleep(1)
    me=w.get_self_info()
    # 发送图片消息
    # w.send_img(self_wx=self_wx, to_wx="filehelper", path=r"C:\1.png")
    # time.sleep(1)

    time.sleep(1)
    # 处理消息回调
    print("开始"+'\n')
    while True:
        msg = msg_queue.get()

        # 收款
        if msg['msg_type'] == 1:
            url=URL+msg['content']
            re= requests.get(url)
            r=re.json()
            w.send_text(
                self_wx=me['wx_id'],
                to_wx=msg['wx_id'],
                msg=r["content"]
            )
if __name__ == '__main__':
    main()
