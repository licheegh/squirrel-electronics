Title: PAC1934 USB-A Power Meter体验
Date: 2019-04-23 12:00
Modified: 2019-05-02 12:00
Category: Electronics
Summary: 在21ic免费领了一块PAC1934 USB-A Power Meter，当然不能白拿，要好好玩一下～

---

[TOC]

---

原文发在21ic，但俺不喜欢那地方，因此又搬到这里。。。好累。。。

![PAC1934UAPM盒子][1]

这骚气的红盒子。
[PAC1934UAPM的说明书](http://ww1.microchip.com/downloads/en/DeviceDoc/PAC1934-Power-Meter-User-Guide-50002802A.pdf)

###TF卡耗电测试

那么我就测试一下TF卡的耗电，我这里找到了这几个tf卡：

![各种tf卡][2]

首先测一下读卡器的耗电，大概是6mA：

![tf读卡器的耗电量][3]

接下来测试了一下各个卡的读写耗电量:

![三星tf卡的待机耗电量][4]

![创见tf卡的待机耗电量][5]


| tf卡      | 待机电流  | 写入电流  |
| --------- | -------   | --------- |
| 东芝 128G | 0.007     | 0.277     |
| 三星 128G | 0.008     | 0.254     |
| 创见 4G   | 0.008     | 0.193     |
| 闪迪 32G  | 0.007     | 0.249     |

东芝略坑啊~虽然待机比三星小，但写入高出好多，速度比三星也慢很多。
其他两个并不是同样容量，但如果闪迪的128也是这耗电，那真是厉害了。
当然这个测试包括了读卡器在不同读写速度下的电流，这个没办法去掉。

###优盘耗电测试

我又测试了一下优盘~

闪迪 256

![闪迪256G待机耗电量][6]

闪迪 128

![闪迪128G待机耗电量][7]

| 优盘                          | 待机电流  | 写入电流  |
| ---------                     | -------   | --------- |
| 闪迪至尊 CZ880 128GB          | 0.183     | 0.301     |
| 闪迪type-c USB-a双口 256GB    | 0.130     | 0.179     |

闪迪这个SSD级别的优盘确实比普通速度的高出很多，但并没有到我想象的很高，比如0.49A。
而256G的这个，写入才30MB，竟然这么费电？看来速度和耗电并不是成线性关系的。

###测量超过5v电压(type-c)

根据说明书，USB-A的型号，只能测量5V的电源，而TYPE-C可以测量5~20V。

![pac1934 voltage range][8]
  
但是根据框图：

![pac1934 block diagram][9]
  
唯一接触VBUS的只有DC-DC和PAC1934，而PAC1934可以测量32V啊亲！！！，那么DC-DC呢？

![pac1934UAPM sch][10]

![mcp1754 datasheet][11]

最高16V...不对，那个4.7uF 10V的电容是什么鬼？还要考虑LDO的功率。。。
那只能勉强测一下9V了（注意不要长期工作在9V）：

![pac1934UAPM working under 9.2v][12]

###电量测量

PAC1934还提供了能量统计的功能，使用的是积分的方式，这个方式的意思就是采样电流和电压，乘起来，按照时间积分。
当然这是一种近似，这种方式测量到快速脉冲类型的电流消耗不准确，这需要类似库仑计的方式，如常见的电池电量计。所以最适合的测量就是充电。
比如~剩下50%电量的iphone5s：

![iphone 5s before charge][13]

充满后PAC1934UAPM显示有700多mAh冲进去了。

![iphone 5s after charge][14]

PAC1934UAPM还可以用来测手机的耗电量，先充满手机，然后就可以测量了，比如待机时：

![iphone 5s standby current][15]

最低亮度亮屏电流：

![iphone 5s with lowest lcd brightness][16]

最高亮度电流，可以看出整整高出一倍的耗电量：

![iphone 5s with highest lcd brightness][17]

打开摄像头：

![iphone 5s with camera app running][18]

当然这个是在充电模式下测得，充电模式和正常使用时，手机可能会表现不同~

###总结与拆机

PAC1934是个蛮有意思的芯片，最多4路，32V的测量范围，覆盖了大多数的场景，可自动统计消耗能量，测量精度很不错。且提供QFN封装和超小的WLCSP封装。在电池供电的产品中，是个不错的监控芯片。

拆开看一下，we的插座好评：

![open pac1934UAPM top][19]

csp的封装好小呀，注意ldo旁边的电容。

![open pac1934UAPM bottom][20]

最后测一下[LimeSDR mini](https://www.crowdsupply.com/lime-micro/limesdr-mini)

![limesdr mini standby current][21]

[1]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/1.jpg
[2]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/2.png
[3]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/3.jpg
[4]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/4.jpg
[5]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/5.jpg
[6]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/6.jpg
[7]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/7.jpg
[8]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/8.png
[9]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/9.png
[10]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/10.png
[11]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/11.png
[12]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/12.jpg
[13]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/13.jpg
[14]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/14.jpg
[15]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/15.jpg
[16]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/16.jpg
[17]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/17.jpg
[18]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/18.jpg
[19]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/19.jpg
[20]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/20.jpg
[21]: {static}../images/PAC1934_USB-A_Power_Meter-ti-yan/21.jpg
