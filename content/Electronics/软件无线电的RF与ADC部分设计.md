Title: 软件无线电的RF与ADC部分设计
Date: 2015-08-24 12:00
Category: Electronics
Tags: 软件无线电
Summary: 要设计一个低成本的软件无线电

[TOC]

---

###引言

本文继续细化前文["选择用于低成本软件无线电的FPGA"]({filename}选择用于低成本软件无线电的FPGA.md)中的细节.

目前我找到了3种方案.

1. 直接采样方案.
2. 超外差方案. Superheterodyne Receiver
3. 正交超外差方案. Direct Conversion Receiver(DCR), Homodyne, Zero-IF

ZTE的一篇[Design of Software-Defined Down-Conversion and Up-Conversion: An Overview](http://wwwen.zte.com.cn/endata/magazine/ztecommunications/2011Year/no4/articles/201202/t20120202_283025.html)

![ZTE Superheterodyne Receiver][2]

文中说超外差主要用于高频应用, 如LTE和802.11ac, 主要的问题是牛x的滤波器不好设计, 而提高IF有利于简化滤波器设计, 但IF提高后虽然镜像频率问题得到解决, 但会让相邻的信号出现在IF内, 那么就需要增加IF滤波器.

![ZTE image theory][4]

![ZTE Direct-Conversion Receiver][3]

在DCR中, 滤波器得到了简化, 只需要LPF, 不需要高Q值滤波器是DCR的一大优势, 但是DCR也有一堆问题(直流偏移, even-order distortion, 载波泄漏, IQ不平衡)

[On the Direct Conversion Receiver -- A Tutorial](http://www.microwavejournal.com/articles/3226-on-the-direct-conversion-receiver-a-tutorial)

文中介绍DCR是在单片radio的驱动下发展起来的.

![Superheterodyne Receiver][5]

同样也从超外差开始, 一般第一个RF Band-Select滤波器是一个SAW器件, 在LNA后的Image-Reject也很重要, 一般是一个陶瓷谐振滤波器, 如去掉的话, 会由于镜像频率的增大而导致LNA的噪声增大. IF频率越高, 对这个image-Reject滤波器的要求越低. 在mix到IF后, 需要一个channel选择滤波器, 该滤波器也是一个SAW滤波器. 双IF可以为滤波器提供更宽的区间. 但设计起来比较麻烦.

所以这个架构不适合做成单片radio, 而且使用SAW之类的器件需要阻抗匹配等麻烦问题, 因此接收机的外围器件很多. 而对于宽带接收机, 由于使用了不可调的多个器件, 因此很难提高接收的带宽, 且受限于器件.

![Hartley Image-Reject][6]

Hartley巧妙的利用三角恒等式解决了image的问题, image被抵消了.

![Weaver Image-Reject][7]

两个Hartley组成Weaver Image-Reject Receiver. 但这两种都要求IQ通道的一致性.

![Low IF Single Conversion Receiver][8]

这个方案是为了去除DCR的直流产生的各种影响, 同时保留了DCR不需要高Q滤波器的优点, 但这时就需要一个高速高分辨率的ADC.

![Wideband IF with Double Conversion Receiver][9]

类似于超外差, 最后是类似DCR转到zero-IF上.

![Direct Conversion Receiver][10]

零中频方案很适合多频带, 多标准的工作, 但有些问题, 导致这种方案一直不如超外差方案. 如由LO自己和自己的信号混频导致的DC输出. 在某些应用中, 这个DC不能用电容隔开, 因为信息会留在低频中, 因此一般采用的是DSP中的DC消除.


![hackrf rf block][11]

图为HackRF的MAX一对芯片的框图, 可以看出max2837实现了DCR的下变频, 而MAX5864实现了ADC采集.

![LMS6002D][12]

大家经常使用LM6002D的框图, 最下面从右至左也是DCR的结构.

![ad9361][13]

Ettus公司B2x0系列的RF前端AD9361的采集部分框图, 也是DCR架构.

![ad9862][14]

Ettus公司其他系列都使用的类似AD9862这样的ADC, 通过接不同的子板来实现不同的频段, 当然也可以直接采样, 如BasicRX和LFRX板.

###ADC

型号        | Res | SR | SNR | SFDR | PC(Typ) | AIB | vcc | Price | Pkg     | Comment
-           |   - | -  |  -  |  -   |  -      |  -  | -   |  -    | -       |
LTC2141-12  | 12  | 40 | 70.8| 89   | 65      | 750 | 1.8 | 11.5  | QFN64   |
AD9231-40   | 12  | 40 | 71.5| 90   | 121.5   | 700 | 1.8 | 12    | LFCSP64 | rs146
ADS4222     | 12  | 65 | 61.5|      | 150.8   | 200 | 1.8 | 7.50  | LFCSP64 | ele131
MAX19515    | 10  | 65 | 60.1| 77   | 85      | 850 | 1.8 | 7.92  | TQFN48  | mo99
AD9204-65   | 10  | 65 | 61.5|      | 150.8   | 200 | 1.8 | 7.50  | LFCSP64 | ele131 淘宝68.3

AD9238-40   | 12  | 40 | 71.5| 90   | 121.5   | 700 | 3.0 | 12.14 | LQFP64  | 淘宝有35 rs127
LTC2292     | 12  | 40 | 70.8| 89   | 65      | 750 | 3.0 | 11.88 | QFN64   |
ADC12DL040  | 12  | 40 | 69  | 85   | 210     | 250 | 3.0 | 10    | TQFP    |
ADS5237     | 10  | 65 | 61.5|      | 150.8   | 200 | 3.3 | 9.49  | TQFP    | ele132
LTC2288     | 10  | 65 | 70.8| 89   | 65      | 750 | 3.0 | 7.50  | QFN64   |
AD9216-65   | 10  | 65 | 61.5|      | 150.8   | 200 | 3.0 | 7.59  | LFCSP64 | rs85.9

###Power

AD9238                  |  FX2           | XC6SLX9            | UDA1334
-                       | -              | -                  | -
AVDD 2.7~3.6 200m       | VCC 3.0~3.6 85m| VCCINT 1.2 1.2A    | VDDA 1.8~3.6 3ma
DRVDD 2.3~3.6 10m@2.5   |                | VCCAUX 2.5,3.3 40m | VDDD 1.8~3.6 2ma
                        |                | VCCO 1.1~3.45 30m  |
其中FPGA的VCCAUX

1. 如接2.5V可以减少功耗40%.
2. 如果在配置时, VCCO_2为1.8V, 则VCCAUX必须为2.5V
3. 如果VCCO_2为2.5V或3.3V,则VCCAUX可以为2.5V或3.3V
4. -1L在使用一些IO Standard时必须为2.5V.
5. 在3.3V时, 下拉电阻要小一点儿, 差分端接电阻需要为100ohm

TPS542
TPS543
TPS562

LMR10515
LMR10520
TLV62090
TLV62065
LM2831
TPS62060
LM2832
TPS62065
TPS62067
TLV62130
TPS62140
TPS62085
TPS62090
TPS62130

项目名称        | 时钟          
-               | -             
[PA3FWM][L1]    | Crystal       
[bladeRF][L3]   | DAC Controlled VCXO to Clk buffer SI5338
Ettus USRP1     | TCXO AD9513
Ettus USRP2     | TCXO AD9510 & exclk DS90CP22 AD9510
[Ettus B100][L4]| TCXO AD9522
Ettus B2x0      | TCXO ADF4001
Ettus N2x0      | TCXO SY89545L AD9510
HackRF One      | SI5351
[HPSDR][L5]&Hermes| VCXO SN65LVDM180D + 10M TCXO for FPGA
[Myriad-RF][L6] | VCTCXO CDCV304PW
OsmoSDR         | SI570 SN65LVDS2
UmTRX           | VCTCXO SI5330

1. 时域
    * Period Jitter: 在定义的所有周期中, 最大的jitter减去平均的jitter.
    * Period Jitter Peak-to-Peak: 在n个中, 最大的时钟周期减去最小的时钟周期.
    * Cycle-to-Cycle Jitter: 在n个相邻的两个周期之间最大的差.
    * Cycle-to-Cycle Jitter peak-to-peak: 在n个相邻的两个周期的差的最大值和最小值的差.
    * Time Interval Error(TIE):
2. 频域
    * Phase Jitter: 这个是将Phase Noise在离载波一定范围内积分.
    * Phase Noise: 信号功率比噪声功率, 并归一化到载波偏移一定量时, 1Hz带宽.

[Basics of Clock Jitter](http://www.onsemi.cn/pub_link/Collateral/AND8459-D.PDF)
[Understanding SYSCLK Jitter](http://cache.freescale.com/files/32bit/doc/app_note/AN4056.pdf)
[抖动计算器](http://www.maximintegrated.com/cn/design/tools/calculators/general-engineering/jitter.cfm)

LX9 Micro | LX9  | 400mA
Anvyl     | LX45 | 2A+
Nexys3    | LX16 | 3A(.2A~1.9A) 200mA IO
SP601     | LX16 | 8A

http://www.xilinx.com/support/documentation/sw_manuals/xilinx14_7/isehelp_start.htm#pim_c_introduction_indirect_programming.htm

###DCR

典型的应用可以参考[LTM9004](http://www.linear.com/product/LTM9004)
[CMX994](http://www.radiolocman.com/news/new.html?di=63542)


[1]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/1.jpg
[2]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/2.gif
[3]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/3.gif
[4]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/4.gif
[5]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/5.jpg
[6]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/6.jpg
[7]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/7.jpg
[8]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/8.jpg
[9]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/9.jpg
[10]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/10.jpg
[11]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/11.png
[12]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/12.png
[13]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/13.png
[14]: {filename}../images/ruan-jian-wu-xian-dian-de-rfyu-adcbu-fen-she-ji/14.png

[^1]: 这一行数据主要来自各自器件的DC and AC switching characteristic中的Recommended Operating Conditions.
