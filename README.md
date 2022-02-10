# QQ robot

一个 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)(>=2.X) 插件

使用go-cqhttp实现在服务器里向QQ群发送消息的功能。


# 功能介绍
自主处理用户消息并发送群消息

接收群消息（正在开发）

在服务器启动、启动完成、关闭时发送消息

在玩家进入/退出时发送消息

在MCDR关闭时发送消息

# 配置
**需要配置好[go-cqhttp](https://docs.go-cqhttp.org/)** 连接方式选择http

配置文件：```config/qq_robot/config.json```

```ip```：go-cqhttp的http端口，默认值：```http://127.0.0.1:5700```

```group_id```：发送消息的群号，默认值：```0```

# Command
```!!qq```显示帮助信息

```!!qq send <message>``` 发送消息