Title: 选择用于低成本软件无线电的FPGA
Date: 2015-08-18 17:00
Modified: 2015-09-13 17:00
Category: Electronics
Tags: FPGA, 软件无线电
Summary: 对于一个简单的软件无线电项目, 对FPGA都有哪些需求? xilinx公司的低成本FPGA: Spartan-3, Spartan-6, Artix-7, 应该如何选择?

[TOC]

---

###引言

前几天看FM立体声解调算法实在是看得头疼, 于是决定看点儿别的散散心. 那么我就先研究一下后边的硬件项目吧, 项目的目标是一个软件无线电的开发板, FPGA将高速ADC中的数据处理通过高速数据接口输出至PC. 那么选择FPGA就有以下地方需要考虑:

1. 可板载高速ADC(>50Msps)
2. 可与PC通过某种高速连接传输数据.
3. 板上具有尽可能丰富的DSP资源.
4. 低成本.
5. 设计起来容易.

---

###已有开源项目比较

目前此类项目还是挺多的, 因此先总结一下.

项目名称        | 主控          | 采集          | 接口          | 带宽  | 备注
-               | -             | -             | -             | -     | -
[PA3FWM][L1]    | XC3S500E      | LTC2216[^5]   | [DP83865][L2] | 25M   | 偶像,另外这个2208很流行
[bladeRF][L3]   | EP4CE40/115   | LMS6002D      | Cypress FX3   | 28M 12bit  | 集成芯片
Ettus USRP1     | EP1C12        | AD9862        | Cy7c68013 FX2 | 16M 8bit    | 集成芯片
Ettus USRP2     | XC3SXX00      | LTC2284       | DP83865       | 50M 8bit | 双AD,AD9777 DAC
[Ettus B100][L4]| XC3S1400      | AD9862        | Cy7c68013 FX2 | 16M 8bit  | 集成芯片
Ettus B2x0      | XC6SLX75/150  | AD9361        | CYUSB3014 FX3 | 61.44M | 强悍的集成AD9361
Ettus N2x0      | XC3SD3400/1800| ADS62P44      | ET1011C2      | 50M 8bit | PHY芯片很奇怪
HackRF One      | LPC4320       | MAX5864+MAX2837 | Integrated /w LPC4320 | 20M 8bit | 复杂的RF设计
[HPSDR][L5]&Hermes| EP3C40        | LTC2208       | KSZ9021RL & CY7C68013A | | 强悍的设计[^6]
[Myriad-RF][L6] | iMX6+XC6SLX45 | LMS6002       | 通过主板连接  |       | 基于[novena][L7]这个开发板
OsmoSDR         | ATSAM3U+LFXP2 | e4000+AD7357  | Integrated /w SAM3 | 1.2M | 很有趣的设计
UmTRX           | XC6SLX75      | LMS6002D      | ET1011C2      | 14M   | 使用Ettus的UHD, 因此PHY一样


[L1]: http://wwwhome.cs.utwente.nl/~ptdeboer/ham/sdr/#nov2008
[L2]: http://www.ti.com/product/dp83865
[L3]: https://www.nuand.com/
[L4]: http://www.ettus.com/product/details/USRPPKG
[L5]: http://openhpsdr.org/wiki/index.php?title=MERCURY
[L6]: https://myriadrf.org/projects/novena-rf/
[L7]: http://www.kosagi.com/w/index.php?title=Novena_Main_Page

不多的几款产品是PCI-E接口, 但不开源.[Bitshark™ Express RX](http://www.epiqsolutions.com/express-rx/) 和 [Noctar](http://www.pervices.com/noctar/).

一篇不错的评测[SDR Showdown: HackRF vs. bladeRF vs. USRP](http://www.taylorkillian.com/2013/08/sdr-showdown-hackrf-vs-bladerf-vs-usrp.html)

可以看出大多数项目都是使用USB来作为接口, 而用网络的大多数都是使用Ettus公司开源的UHD接口, 那么大多数人的选择还是认为网络或多或少有些问题.

使用的FPGA方案一律都是选大容量的, 尤其是Ettus公司.

---

###高速PC数据接口

其实高速的数据接口最佳的应该是PCI-E, 很多FPGA都内置PCI-E接口, 但PCI-E这东西不怎么好玩, 不说别的, 万一把主板给烧了不就好玩了吗. 所以~还是网络或者USB吧.

根据wiki, USB 2.0可以达到35MBps, 而采用2.0的开源项目都可以采集到16M宽的频谱, 最大20M, 而3.0就不用说了Ettus的B200可以达到60M. 但本人目前没有USB 3.0的电脑,  而千兆网很普及, 我家路由和所有电脑一律都有千兆网. 千兆网应当可达到100M没有问题, 这些项目中Ettus公司的N2x0达到了50M, 我偶像达到25M.

其实对于大多数应用, 我个人觉得有10M就够用了. 当然如果可以到20M, FM广播就全覆盖了. USB的开发难度应当是不高的, Cypress公司肯定有各种应用的参考程序可供使用, 要使用其他公司的有USB的MCU也应当是很容易的. 上位机开发有[PyUSB](https://walac.github.io/pyusb/)据说是开箱即用, 我想一定不难. 

* [PHYS Ethernet or FPGA](http://electronics.stackexchange.com/questions/49407/phys-ethernet-or-fpga) 回答说Ethernet这玩意儿很难, 轻易不要碰.
* [Retrieving samples from an FPGA using Ethernet](http://electronics.stackexchange.com/questions/103955/retrieving-samples-from-an-fpga-using-ethernet?rq=1) 这篇问答提到其实要做点对点的连接很简单, 直接广播就可以了.
* Eli Billauer的博文(墙外)
    * [Designed to fail: Ethernet for FPGA-PC communication](http://billauer.co.il/blog/2011/11/gigabit-ethernet-fpga-xilinx-data-acquisition/) 这篇博文中作者说广播or简单的Ethernet方案是不靠谱的, "丢包是允许的, 如丢了要重发, 那FPGA里要做一个外部缓存来重发包吗?"
    * [An FPGA-based PCI Express peripheral for Windows: It’s easy](http://billauer.co.il/blog/2012/02/pcie-usb-ezusb-marvell-alaska/) 作者介绍了各种从FPGA与PC的传输方案, 作者说Cypress的EZ-USB虽然是简单易行的方案, 但片子安到板子上后就各种闹脾气, 说是有"个性". 而Ethernet他说从FPGA到PC, 这种方案很简单, MAC包很容易构建, 但有上文提到的问题. 最后推荐他利益相关的PCI-E方案.
    * [List of FPGA boards and IP cores with PCIe/USB and their vendors](http://billauer.co.il/blog/2012/04/fpga-pcie-usb-board-ip-core/) 介绍了一些USB的接口芯片, 以及有PCI-E和USB接口的开发板, 并提供了一个FPGA开发板大全列表[FPGA Boards and Systems](http://www.fpga-faq.com/FPGA_Boards.shtml), 这列表点赞.
* [What is a good microcontroller for Ethernet applications?](http://electronics.stackexchange.com/questions/297/what-is-a-good-microcontroller-for-ethernet-applications) 热情的网友写了很多带有Ethernet接口的MCU.

经过搜索, 支持千兆的MCU(或MP)只有那些可以跑android系统的, 和专用来做路由器芯片. 跑android系统芯片都太复杂, 我搞定它就不用干别的了. 而路由器芯片资料少, 大多数都需要NDA. 因此找一个支持千兆的简单MCU是不可行的.

OK, 总结一下:

1. Ethernet方案:
    * MCU集成MAC+PHY : 只能到100M, 只发不收难度应不高, 都有例程.
    * FPGA + Gigabit PHY : 只能做到点对点传输. 这可以说是利用这个接口实现了想要的功能. 网口当USB用了.
2. USB方案: Cypress FX搞定, 3.0和2.0 HS都有支持. 经查libusb还有个fxload可以支持给FX下载FW.

顺便提一下FX3, 它采用一个200MHz的ARM926EJ-S, 可见其中肯定有限制必须要这个级别的MCU才可以搞定. 因此Gigabit Ethernet只出现在高端处理器上也就不奇怪了.

刚写这篇的时候我考虑的是尽量高的传输数据, 所以想选择FX3, 但外出散步思考了一下后, 我觉得带宽这件事情需要仔细的考虑. 高带宽有什么样的好处呢? 首先"视野"开阔了, 能同时看到更多的信号传输, 其次某些应用本身的信号带宽就很宽, 如wifi, 那么想要收到这样的信号, 宽带的接收是必须的. 但高带宽也带来一些问题, 第一提高了整个设计的成本, 需要高速的ADC, 高速的数据连接, 高速的处理系统.

其实我用这个东东也就是玩玩, 那些高带宽的应用我肯定是不需要的, 而我感兴趣的应用大多数应都不会大于1M的带宽. 另外我想与其将带宽做到最大, 不如将可接收的范围扩大, 比如很火爆的hackRF one, 它可以工作的带宽达到30M-6G, 虽然只有20M的带宽, 但依然挡不住它的火爆.

**因此我决定采用古老的USB2.0 HS.**
    
---

###ADC接口

大多数的开源项目
找到三篇讲述ADC接口的文章. [Interfacing FPGAs to an ADC Converter’s Digital Data Output](http://www.analog.com/media/en/training-seminars/tutorials/MT-201.pdf), [Interface from TI](http://www.ti.com/europe/downloads/Interfaces.pdf), [Interfacing LTC ADCs to Altera FPGAs](http://www.stecinc.ru/filemanager/download/23843/) 总的来说, 有以下接口可供选择.

接口 | 优点 | 缺点
- | - | -
并行CMOS | 简单, 比LVDS耗电少. | 需要IO数多. EMI辐射比LVDS大. 速度限于250M
并行LVDS | 高速, 并可抑制共模噪声, 两边可独立供电, EMI低 | 在不用DDR的情况下每个bit需要2根线, 耗电稍大
串行LVDS | IO少. | 最大至125Msps, 比并联CMOS耗电大
JESD204 | 超级简单的连接(SerDes), 封装变小, 成本降低 | 我这菜鸟能搞定这么高速的连接吗?

关于这个JESD204, 可以参考TI的介绍[JESD204](http://www.ti.com.cn/lsds/ti_zh/data-converters/high-speed-adc-greater-10msps-jesd204b.page)

于是天真的我以为可以找到类似20pin, 串行接口的12bit 50Msps+ ADC, 结果digikey搜索结果是, 小于30pin的全部是并行接口, 唯一一个是LVDS并行的TI ADC08100, 结果是digikey标注错误, 还是并行接口. 真正串行的LVDS和JESD204接口, 都是用于单片多通道的ADC, 2通道都比较少见, 大多数是4+通道, 这些芯片要是用并行CMOS, 只是数据口就有40+, 因此用这些串行接口优势明显.

**那么我就老老实实用并行CMOS吧, 找一个IO口电平独立的ADC就好.**

---

###FPGA的选择

从前文可以看出, PC接口与ADC接口对FPGA没有什么要求, 那么就只需要考虑DSP能力和设计复杂度了. 之前曾经画过一个基于Spartan-3A的板子, 上面还有个mega32, 做好以后也没怎么玩, 就扔在那里了, jtag的下载线也买了, 那么这次最佳选择就是Xilinx公司的产品. [wp396](http://www.xilinx.com/support/documentation/white_papers/wp396_S6_HV_Perf_Power.pdf)中有Spartan-6与Cyclone IV之间的对比.

![Spartan 3A 200 + Mega32][2]

3E系列是比较古老的了, 我记得我最开始学这东西的时候, 有个著名的开发板, [Spartan 3E Starter Board](http://www.digilentinc.com/Products/Detail.cfm?NavTop=2&NavSub=423&Prod=S3EBOARD&CFID=15108165&CFTOKEN=6bf8988b50c049a-A0264518-5056-0201-0238ED0146D7CA23), 曾经还想搞一块.

![Spartan 3E Starter Board][1]

根据Spartan-3 UserGuide, 3E和3是属于第一代产品, 3A, 3AN, 3A DSP是扩展(Extended)版本, 90nm工艺, Extended版本在下载Bitstream方式, 供电等方面有更新, 其中3A DSP采用DSP48A作为DSP加速模块, 而其他用的是18x18乘法器. Spartan3之间架构是基本一致的.

Spartan-6 为45nm工艺, 集成了内存控制器, 支持DDR3, CLB得到了加强, LUT由4输入升级为6输入(根据[THE SPARTANS](http://www.fpgarelated.com/showarticle/3.php), LUT用量大概会减少10%), 时钟控制部分也复杂了很多, [据说可以产生任意频率](https://translate.google.com/translate?sl=auto&tl=en&js=y&prev=_t&hl=en&ie=UTF-8&u=http%3A%2F%2Fwww.tokudenkairo.co.jp%2Fsp6%2Fsp3diff.html&edit-text=&act=url). DSP模块升级为DSP48A1. 关于3和6之间的差异还可以看看[wp309](http://www.xilinx.com/support/documentation/white_papers/wp309.pdf).

Artix-7 为28nm工艺, 集成了一个1Msps的12bit ADC, DSP模块升级为DSP48E1(功能强悍很多). 去掉了内存控制器(参考Xilinx MIG的说明书, 普通DDR2需要7633个LUT和4588个FF, 这分别是XC7A15T的73%和22%), 全系列都有PCI-E, GTP. CLB部分去掉了6中最小的SLICEX, 所有的SLICE都具有carry输入与输出. 另外CLB采用了[ASMBL架构](http://www.xilinx.com/company/press/kits/asmbl/asmbl_arch_pres.pdf)的排列方式. [wp405](http://www.xilinx.com/support/documentation/white_papers/wp405-7Series-Logical-Advantage.pdf)中有7系列CLB与6系列的对比.

另外一篇非常好的比较Spartan-6之前各个版本xilinx FPGA的PPT: [Basic FPGA Architectures](http://www.csd.uoc.gr/~hy220/2009f/lectures/11_basic_fpga_arch.pdf).

3,6,7之间的结构在PlanAhead软件中的对比:

![Spartan 3A, Spartan 6, Kintex 7 compare 1][3]

6和7之间的差别其实不大, 但3与6之间确实有很大的差别. 逻辑单元细节对比. (更正: 图中XC6SLX25左上黑色部分不是内存控制器, 内存控制器为上半部两边的粉色框, 黑色部分为不明物体.)

![Spartan 3A, Spartan 6, Kintex 7 compare detail][4]

这样就能很直观的看到6中SLICE的排列方式.

当然我这是相当业余且简单的比较:), xilinx并没有官方的比较这些产品的区别. 接下来我从一个具体的型号来比较一下, 这里的基准是XC3S500E, 因为我偶像用的是它.

项目    | XC3S500E  | XC3S700A  | XC6SLX16  | XC7A15T[^3]
-       | -         | -         | -         | -
LUTs    | 9312      | 11776     | 9112      | 10400
LE[^4]  | 10476     | 13248     | 14579     | 16640
Slices  | 4656      | 5888      | 2278      | 2600
Dis RAM | 73k       | 92k       | 136k      | 200k
Blk RAM | 360k      | 360k      | 576k      | 900k
DSP     | 20        | 20        | 32        | 45
价格($) | 30        | 37.6      | 25.5      | 25.7
供电[^1]|           | 最少两组  | 最少两组  | 最少三组[^2]

选择的依据是尽可能一致的LUT数目, 因为每一代产品并不能找到完全一样的进行比较, 但并不能找到完全一致的产品. 价格来自digikey.

另外在开发软件支持方面:

* ISE Webpack支持3A,3E的所有型号(除3A DSP的最高档), Spartan 6的XC6SLX4至XC6SLX75T, Artix-7的100T和200T. [ISE 14 Release Notes](http://www.xilinx.com/support/documentation/sw_manuals/xilinx14_7/irn.pdf)
* 新的Vivado Webpack支持XC7A35T, XC7A50T, XC7A75T, XC7A100T, XC7A200T. 另外要求操作系统是win7 64或更高. [Vivado Release Notes](http://www.xilinx.com/support/documentation/sw_manuals/xilinx2015_1/ug973-vivado-release-notes-install-license.pdf)

OK, 那也就是说, 老一代的3系列产品在价格上并没有优势, 而性能还不如新产品, 那么我面临的选择就是Artix和Spartan-6. 新的Artix虽然在CLB上并没有太大的改进, 但是在CLB的排列方式上有很大改进, 而且新的DSP模块支持ALU也挺吸引人, 但其新增的PCI-E和GTP我完全用不上. 另外电源多了一组. 复杂度增加.

据我之前在马云家询的价, Vivado Webpack版本支持的最低档Artix-7(XC7A35T)要价300+, 还没有现货, 从digikey买也差不多是这价, 而Spartan-6便宜很多, 马云家FTG256的LX25竟然只要不到100. 在开发软件方面Artix也不是很友好, 不能使用15T外, 还必须是win7 64bit. 

**因此我很倾向于用Spartan-6.**

为了练习BGA, 所以选择最小pin count, 最大pin pitch的FTG256封装. 可以焊上去LX9, LX16, LX25三个型号.

###总结

那么这个项目就是由一个Spartan-6(FTG256封装)的FPGA从一个并行接口的ADC采集信号后通过Cypress的FX3 USB3.0 Controller传输到PC.

后边会继续研究项目细节.

1. RF部分.
2. ADC部分.
3. 其他外围器件.

[1]: {filename}../images/选择用于低成本软件无线电的FPGA/1.jpg
[2]: {filename}../images/选择用于低成本软件无线电的FPGA/2.jpg
[3]: {filename}../images/选择用于低成本软件无线电的FPGA/3.png
[4]: {filename}../images/选择用于低成本软件无线电的FPGA/4.png

[^1]: 这一行数据主要来自各自器件的DC and AC switching characteristic中的Recommended Operating Conditions.
[^2]: 根据ug482, Chap 5, Pin Description and Design Guidelines, GTP的电源如不用可以接地. 根据ug480, Chap 1, Table 1-1, XADC如不用可以将电源与Vccaux接在一起. 那么IO + aux + int&bram就是三组电源, 当然如果IO用1.8v, 就可以减少到2组.
[^3]: 这是最小的Artix-7.
[^4]: 这个在xilinx这里被称为Equivalent Logic Cell. 据说是等效ASIC业内行话.
[^5]: 作者之前用LTC2208, 但后来改为LTC2216.
[^6]: 该项目全部开源(所有PCB, HDL, PC软件), 虽然不是最紧凑的方案, 但是非常灵活, 研究一下好处多多:) 并且衍生出很多其他项目,如Hermes.
