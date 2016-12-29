Title: 一次不成功的Kindle维修
Date: 2015-09-30 12:00
Category: Electronics
Tags: 维修
Summary: 老友的Kindle Paperwhite砖了, 据说可以连tty(UART)接口来重新来过.

老友的Kindle Paperwhite某一天突然只能看大树了, 在反复插拔USB接口到充电器与PC上, 以及各种姿势按电源按钮无效的情况下, 打算拆开重新刷.

KPW的主板是有预留出linux下调试用的tty接口的, 所谓的tty也就是1.8V的串口/UART, 这一点我特意用示波器看了一下, 确实是1.8V. 我之前搞的一个板子上有CP2102这个USB转串口的芯片, 但它是3.3V供电且输入的高电平最低为2.0V, 那么问题来了, 又要上淘宝买个兼容1.8V的USB转换器吗?

或者说可以接个三极管转换一下? 反正是单向传输. 于是搜了一下, [Is a N-Channel Mosfet save/reliable for level shifting UART from 3V3 to 5V?](http://electronics.stackexchange.com/questions/102603/is-a-n-channel-mosfet-save-reliable-for-level-shifting-uart-from-3v3-to-5v), 中alexan_e提出了一个好方法.

![UART Level Converter][1]

这电路唯一的问题是速度, UART这种应用是没有问题的, 不行的话可以调低上拉电阻的值, 但要注意IO口的电流驱动能力.

![Kindle tty 1.8V to 3.3V converter][2]

电阻是随便找的7.4k, 二极管为1N4148.

![KPW connected to UART-USB][3]

右边为Kindle, 左边为被利用的CP2102板.

![KPW tty rx tx soldering][4]

这三个焊点不是很好焊. 另外接地可以不用接这里, 而且这里地面积略大, 焊不动啊~ 焊完还用热熔胶固定了一下, 不小心把焊盘扯下来就好玩了.

![mmcblk0 error][5]

启动后满屏的mmcblk0错误. 文件系统错误导致的么?

![format mmc0][6]

于是我就格了一下~然并卵, 我不是格了么? 为啥还可以看大树?

![repairing KPW with a windows and a mac pc][7]

那么我就试试刷系统吧, 连fastboot竟然需要一台mac, 我也是醉了. 参考[How to unbrick an Amazon Kindle Paperwhite](https://gist.github.com/TobiasWooldridge/22f0cdca75190b9a473f).

刷完后还是大树, 于是我仔细搜了一下~某国外著名刷kindle论坛果然有类似的问题, [Bad mmc0 ?](http://www.mobileread.com/forums/showthread.php?t=186035), 直接拿去换吧, 修不好了.

我个人是觉得应当是BGA下面的焊接问题, 但无奈这Flash不仅是个BGA而且还有个屏蔽罩. 这基本就是无法修复. 于是我只能放弃了.

资料:

* <https://gyf.blog.ustc.edu.cn/kindle-paperwhite-2-repair/>
* <http://www.izheteng.com/teardown/fix-kindle-paperwhite.html>
* <http://blog.sina.com.cn/s/blog_4d66a3cb0101klkm.html>
* <http://www.xodustech.com/guides/kindle-paperwhite-demo-unlock>
* 还有著名的mobileread论坛.

![KPW3 PCB with shield removed][8]

最后上一张KPW3的PCB图, 来自ZOL.


[1]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/1.png
[2]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/2.jpg
[3]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/3.jpg
[4]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/4.jpg
[5]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/5.png
[6]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/6.png
[7]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/7.jpg
[8]: {filename}../images/yi-ci-bu-cheng-gong-de-kindlewei-xiu/8.jpg
