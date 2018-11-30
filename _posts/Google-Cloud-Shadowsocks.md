---

title: 'Google Cloud搭建Shadowsocks,高速科学上网，10分钟搞定'
date: 2018-01-22 20:31:10
tags:
    - vpn
categories: 
    - vpn
password: 
top: 100
---

### 开始

公司VPN没有把Pinterest加入白名单，只能自己动手搭建一个shadowsocks，过程很简单。服务器选的是Google Cloud，好处有以下几点：
>1.第一年赠送300美金，配置稍微选的低一点，可以免费用一年
>2.速度很快，Youtube 1080无压力。

### 配置Google Cloud

1.注册Google Cloud Platform账号，需要一张visa信用卡。注册地址：[Google Cloud官网](https://cloud.google.com/)

2.创建一个VM，系统建议选择CentOS7,配置建议选低一点，最低的话大概5美金一个月。地区选择asia-east，abc都可以,勾选HTTP,HTTPS流量。
![](http://qiniu.heheceo.com//18-11-30/16770019.jpg)
3.点击“网络”配置静态ip地址。点击"外部IP"新建一个静态IP,注意选择你vm所在的地区，每个地区只能有一个静态ip。
![](http://qiniu.heheceo.com//18-11-30/34983080.jpg)

### 开启shadowsocks服务

使用google自带的命令行，通过ssh连接到远程服务器。链接成功后依次输入以下命令。

> 1.sudo -i （开启管理员权限）
> 2.yum install python-pip (按照pip，为了安装shadowsocks,中途需要输入“y”来继续安装)
> 3.pip install shadowsocks

安装完成后配饰shadowsocks，通过以下几步。

1.输入命令 vi /etc/shadowsocks.json，点击 i 进入输入状态，输入以下内容，输入完成，点击Esc，输入 :wq 保存并退出。

```json
    {
    "server":"0.0.0.0",
    "server_port":443,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"yourpassword",
    "timeout":300,
    "method":"aes-256-cfb"
    }
```

2.输入命令 ssserver -c /etc/shadowsocks.json -d start 启动shadowsocks。

至此服务器端最基本的配置完成了，配置好客户端就可以使用谷歌来查阅资料了。

### 配置 Shadowsocks 客户端

去 [Github](https://github.com/shadowsocks) 上下载对应的客户端，完成后配置IP，端口信息即可。如下图：

![](http://qiniu.heheceo.com//18-11-30/20512593.jpg)


 **遵守法律，科学上网**