Title: 水果pi设计调研
Date: 2017-01-13 18:00
Modified: 2018-01-16 18:00
Category: Electronics
Summary: 设计一个水果pi来玩?

[TOC]

---

现在市场上各种pi很多，原始的raspberry pi，后来的orange pi，Banana pi，beagle bone。这么多板子导致我也想画一个玩玩。看着企鹅在上面跑多好玩呀~

那么需求是什么呢?

* 所有BGA间距0.8以上。做个板子好几千我搞不起。
* 原件便宜。
* 接口不用很全，有串口就行。(做个核心板?)

经查找有意思的soc厂商有 全志， nxp。

---

###全志

为何选这个鸟珠海企业是有原因的，看看他们公司产品的开源支持，还是很不错的。[linux-sunxi](https://linux-sunxi.org/)这个开源社区包括了所有信息。比全志的网站内容丰富多了。


| 芯片 | 口号                           | 封装              | 例子                     | 价格 | 备注              |
| ---- | ------------------------------ | ----------------- | ------------------------ | ---- | ----------------- |
| A20  | 平台型双核处理器               | BGA441 19x19 0.8  | Cubieboard,香蕉pi,olimex | 15   | 社区支持很好      |
| A33  | 最稳定的四核平板解决方案       | BGA282 14x14 0.8  | 昂达V809s平板            | 20   | 目前一般,未来支持 |
| H3   | 完整4K OTT盒子解决方案         | BGA347 14x14 0.65 | 橘子pi,友善之臂          | 27   | 封装不友好        |
| R16  | 最具竞争力的四核智能硬件处理器 | ?                 | NES Classic              | 35   | 该芯片等于A33     |
| V3s  | 入门级双路行车记录仪方案       | LQFP              | ?                        | ?    | 内置DDR内存       |

还有一个[youtube视频Upstream Allwinner | ARM SoC (A10 / sunxi) Support Status](tps://www.youtube.com/watch?v=EAYa095r5tE&feature=share),该视频叙述了各个soc目前的linux kernel,uboot的状态. 下图来自这个视频.

![allwinnner compare][1]

A20算是支持最好的soc了,各大linux发行版均官方支持,而且A20的虚拟化也得到了支持,可以在上门跑虚拟机,如kvm.而且该SOC支持众多接口,如sata,GbE,hdmi.该有的都有.

A33虽然算是新出的soc,但众多接口均没有,连网口也没有,完全是一副为平板设计的芯片,管脚数也比较少,只有282. 当然该芯片以后会得到各大linux的支持.

H3算是当红明星soc,感觉由橘子pi和友善之臂推动,价格便宜,4核.社区支持增加中.封装很不友好,0.65.它还有个小兄弟H2+,也用在几个开发板上.

R8在kickstarter上的C.H.I.P 9刀电脑火了一把,虽然好多人买回来没什么用,但还是挡不住火.后来出的R16又用在 任天堂的官方模拟器nes classic上,近日已被破解.

V3s由于其相当友好的封装和不用lay外部DDR,因此非常适合练手,[有人做了荔枝pi](https://www.kancloud.cn/lichee/lichee/225317),还[录了视频](https://shop152705481.taobao.com/?spm=a1z10.5-c.0.0.f0kxFG)

ref:

* [debian支持列表](https://wiki.debian.org/InstallingDebianOn/Allwinner)
* [ubuntu支持列表](https://help.ubuntu.com/lts/installation-guide/armhf/ch02s01.html)
* [arch支持列表](https://archlinuxarm.org/platforms/armv7/allwinner)
* [armbian社区支持H3和A20](https://forum.armbian.com/index.php/topic/1351-h3-board-buyers-guide/)
* [armbian社区选板工具](https://www.armbian.com/download/)


---

###NXP

高通,不,nxp,也就是曾经的Freescale,是目前联想旗下的摩托罗拉曾经的半导体部门发展而来,摩托的68000相信是大名鼎鼎.因此我自觉的去翻他们的产品线.

目前nxp的主流为I.MX系列,我个人觉得这名字起的不好,第一:以i开头是向乔帮助致敬吗?第二:中间这个点造成各大搜索引擎障碍.

我能用的了的版本为 i.mx6和i.mx7,其中,淘宝爆款为 MCIMX6G2DVM05AA 当然我也研究的不是很透,nxp这产品线真是太长了,一个型号一堆不同的版本.imx7是自带cortex m4单片机的单片处理器,确实很适合作iot产品,但其封装为0.75或0.4pitch. 而imx6友好很多, 为0.8.

imx6的另一个优势是有些型号有双网口版本.

在软件支持方面作为大厂商各种linux包括android都有支持,而社区支持似乎一般.

价格方面imx6大概为85一片,imx7之在mouser上查了一下0.75的大概是170多.

18年年初我又想起来，于是研究了一下，貌似市场上最省电的还是imx6ul，而且硬件也比较省心，电源部分简单。

| 芯片       | idle(mW)  | Dhrystone(mW) | Video(mW)  | Power Rail | Easiest Packaging |
| ---------- | --------- | ------------- | ---------- | ---------- | ----------------- |
| i.MX6ULL   | 20        | 269@528MHz    | 414@528MHz | 3          | 14x14 0.8         |
| i.MX6UL    | 28@518MHz | 264@528MHz    | 419@528MHz | 3          | 14x14 0.8         |
| i.MX7 Solo | ?         | ?             | ?          | 5          | 19x19 0.75        |
| i.MX7 Dual | 51        | 352@1GHz      | ?          | 5          | 19x19 0.75        |
| i.MX7 ULP  | ?         | ?             | ?          | ?          | 14x14 0.5         |

i.MX6ul确实是省电的王者，使用A7处理器本身就很有优势，全速cpu仅260mW，那就是说对于锂电池而言只需要70mA的电流（按3.7V计算，且未计算ddr等），一个1000mAH的电池轻松跑10个小时全速。

而将要出的imx7ulp则是nxp还未推出的处理器，据称采用更好的制程（28nm FD-SOI）来获得更好的省电效果。但这封装和电源真的是不省心，虽然有单配的PMIC。
而imx7系列都具有的M4+A7这种搭配确实是很适合某些类型的应用。

[1]: {static}../images/shui-guo-pishe-ji-diao-yan/1.png
