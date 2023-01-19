# QQ robot

一个 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)(>=2.X) 插件

使用go-cqhttp实现在服务器里向QQ群发送消息的功能。


# 功能介绍
自主处理用户消息并发送群消息

接收群消息并发送到服务器

在服务器启动、启动完成、关闭时发送消息

在玩家进入/退出时发送消息

在MCDR关闭时发送消息

# Requirements
```shell
pip install -r requirements.txt
```

# 配置
**需要配置好[go-cqhttp](https://docs.go-cqhttp.org/)** 连接方式选择http

配置文件：```config/qq_robot/config.json```

```ip```：go-cqhttp的Websocket地址，默认值：```127.0.0.1```

```port```：go-cqhttp的Websocket端口，默认值：```8080```

```group_id```：发送消息的群号，默认值：```0```

```userlist```：QQ号和游戏id的对应表

# Command
```!!qq```显示帮助信息

```!!qq send <message>``` 发送消息
