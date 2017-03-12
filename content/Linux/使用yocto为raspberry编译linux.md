Title: 使用yocto为raspberry编译linux
Date: 2017-03-12 22:40
Modified: 2017-03-13 14:00
Category: Linux
Summary: 由于工作的关系需要搞一下yocto，看过介绍觉得这很适合嵌入式应用，个人感觉和openwrt很像。手里有个树莓派，当然最简单的就是先为它编译一个linux系统玩玩。

[yocto](https://www.yoctoproject.org/downloads)网站最新的版本是morty 2.2.1，当然我们要用git clone的方式来获取最新的，但直接clone发现速度只有几kb。我记得我的git是有走socks5的呀～经研究发现git://这种开头的和https://开头的并不一样，通过<https://gist.github.com/laispace/666dd7b27e9116faece6>

```
git config --global https.proxy http://127.0.0.1:1080
git config --global https.proxy https://127.0.0.1:1080
```

这样只能实现对http/https的代理，于是我顺利的在<http://git.yoctoproject.org/cgit/cgit.cgi/poky/>页面的最下面找到了https的链接<https://git.yoctoproject.org/git/poky>。这样虽然也只有80多kb，但已经快了很多。clone完成后文件夹有185MB大小。




