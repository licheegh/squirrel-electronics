Title: Nucleo的ST-LINK_V2-1维修
Date: 2016-05-13 21:00
Category: Electronics
Tags: 维修
Summary: 板载的ST-LINK坏了，怎么办呢？就是个STM32嘛，换一个就好了。

某次把NUCLEO-F401RE上的ST-LINK烧了(碰到12V), 于是买了一个LQFP48的STM32F103CBT6来维修. 顺便把板载的F401也烧了, 这片子貌似不好买(想在一家买), 于是按照ST的文档UM1724找了一圈, 发现好买的只有 STM32F103RBT6 , 好吧~

先换了ST-LINK的MCU, 接上pc显示未能识别的设备. 我去这是咋回事? 这玩意儿不是通过一个PC软件自己更新固件的吗? 于是我吹了一遍，拿着放大镜检查n便，电压检查一遍，最终去看说明书了。

翻AN2586, f103所属的low-density系列只支持从UART1启动, 不支持USB-DFU. 如需启动需要将BOOT0拉高. 开发板上BOOT1是永久拉低的, BOOT0通过一个电阻拉低. 这样看来似乎是留有这个方式的. 

继续翻AN2606, 说是PA9 TX和PA10 RX. 板子上这两个信号完全不像是要接串口的样子, 倒是UART2通过CN3接出来.

OK, 那也就是说ST的意思应当不是通过串口来编程的. 当然飞线也是可以, 但我还有一块Nucleo....

我看了下ST特地把这部分作成一个可选择的跳线出来.

CN4(swd host)   |   CN2(bad board)
-               |   -
1 VCC_TARGET    |   3V3
2 SWCLK         |   SWCLK
3 GND           |   GND
4 SWDIO         |   SWDIO
5 NRST          |   SB11 左边
6 SWO           |   NC

飞线后.连上并且认出来了,那么问题来了,我该往里面写啥? 翻了ST的网站, 似乎没有这个固件,看了升级用的程序, 目录里面也没有这个固件. 那第三方的ST-LINK怎么搞出来的?

* <http://e.pavlin.si/2016/02/28/how-to-program-blank-stm32f1-with-stlink-v2-firmware/>
* <http://www.micromouseonline.com/2014/01/05/mini-st-linkv2-programmer/>
* <http://www.diygoodies.org.ua/?p=417>

[ST LINK V2 Firmware]({attach}../Download/STLinkV2_J16_S4.zip)

据说firmware在一个keil的工程里面.

然后我用另外一个ST-LINK写了进去, OK, 再用update工具升级成功.

然后开发板的芯片也坏了, 原来是 STM32F401RET6  换为  STM32F103RBT6.

经过研究电路图, 只要去掉C26即可.
