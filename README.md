# README
暂时分三个部分 控制 通信和硬件控制

## control
    center_control：中心解析指令，执行指令的模块
    node_control:   子节点解析指令，执行指令的模块
    order_config：  定义一些指令的编码
    user_scipt:     为用户脚本提供API接口

## hardware
    agent:  抽象出来的硬件控制agent，只是作为一个接口
    G1-Raspberry：控制G1无人小车的驱动，实现agent里面需要的函数
    raspberrypi： 写了一下目前用的树莓派的控制程序，目前只加入了sgp30和dht22传感器的读取
    action_config： 定义动作指令编码

## transform
    封装通信模块，分为中心和节点的指令收发模块和数据收发模块
    通信模块监听连接的socket，收到的指令存进队列等待control模块读取执行
    数据收发模块接受control的控制，发送或接收文件


## 需要扩展的部分
* 重构之后还没来得及测试 需要测试一下bug，尤其是互操作机制，就是用一个节点去尝试控制另一个节点
* 写一下用户脚本的API，设想的是通过实例化user_scipt来控制节点和获取信息，user_scipt通过socket通信将指令发给control实现控制和数据交互
* 设计一下无人小车，传感器 可以用的动作有哪些，编码在action config里面