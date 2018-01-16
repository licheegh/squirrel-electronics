Title: LCSDR工程
Date: 2015-11-01 12:00
Modified: 2018-01-16 12:00
Category: Electronics
Tags: FPGA
Summary: 该工程的最新进展, 图片, 程序等.

[TOC]

---

[本项目电路图，PCB , Gerber, BOM](https://github.com/licheegh/LCSDR)
采用Kicad.

---

###硬件

目前发现的硬件Bug:

1. JTAG插座线序有误.
2. 用一个双运放来做Audio DAC的功率放大或许会比目前的TDA2822要好.

"多亏当时这么设计了":

1. Cypress的FX2LP cy7c68013a, 听从了AN15456的要求, 给EEPROM的SDA线加了一个跳线块, 真的是好方便, 改成按钮应该更方便(但需要常闭开关).
2. 不记得从哪里看到说FPGA设计最好将多余的IO引出, 以用来接逻辑分析仪做调试, 之前不解, 有Chipscope谁要那玩意儿, 之后用Saleae调试, 真是好用啊, 就是只接了8 bit略少呀.
3. 两个复位按起来好爽, 放一起好了.

PCB正面:

![LCSDR empty pcb top][1]

PCB背面:

![LCSDR empty pcb bottom][2]

各种试装:

![LCSDR empty pcb USB socket test][3]

![LCSDR empty pcb encoder socket test][4]

![LCSDR empty pcb pot and audio jack socket test][5]

HQPCB加收了50块的BGA费, 结果还是歪的么?

![LCSDR empty pcb bga pad][6]

在马云家找了一家, 30贴了一片, 对比芯片的70多的价格, 贵~

![LCSDR with BGA FPGA xc6slx25 mounted][7]

不过说实话贴的很不错, 还送了瓶水.

![LCSDR with BGA FPGA xc6slx25 mounted side view][8]

边调试软件测试, 边焊接硬件, 最终搞定!

![LCSDR soldering finished][9]

###调试软件

一开始我调的就是USB芯片FX2 cy7c68013a(因为怕layout的有问题影响性能or直接连不上). 可以连上, 于是跑个分吧~使用AN4053的CYStreamer例程，这个例程包括一个上位机软件和fx2的fw，注意上位机软件在AN4053里的比较新，可以显示cpu占用率，另外要注意的是fx2的fw需要注释掉以下内容，因为它是设计在开发板上运行的，而显示是一个I2C的接口，如果运行到这里会死机。

```diff
diff --git a/CYStream.c b/CYStream.c
index 47a80c0..0aaee3b 100644
--- a/CYStream.c
+++ b/CYStream.c
@@ -677,12 +677,12 @@ BOOL DR_SetInterface(void)       // Called when a Set Interface command is recei
        }

    // Update the display to indicate the currently selected alt. Interface
-       if(updateDisplay)
-       {
-          EZUSB_WriteI2C(LED_ADDR, 0x01, &(Digit[AlternateSetting]));
-          EZUSB_WaitForEEPROMWrite(LED_ADDR);
-          updateDisplay = FALSE;
-       }
+       /*if(updateDisplay)*/^M
+       /*{*/^M
+          /*EZUSB_WriteI2C(LED_ADDR, 0x01, &(Digit[AlternateSetting]));*/^M
+          /*EZUSB_WaitForEEPROMWrite(LED_ADDR);*/^M
+          /*updateDisplay = FALSE;*/^M
+       /*}*/^M

    return(TRUE);            // Handled by user code
```

只有16MB/s么? 好低啊~这是咋回事?

![LCSDR cystreamer test][10]

研究了一会儿我发现是我电脑的问题, 下图为连接一个1T西数移动硬盘时的结果:

![a usb ext hdd test][11]

电脑是Lenovo的R61i, USB部分应当是接在ICH8吧~ 后来在朋友的T4xx上测试, 4xMB/s(忘记截图了).

接下来搞定了Audio DAC的输出和编码器部分, 合体后可以控制输出的正弦波的频率.

![Testing Audio DAC output using Spectral View android app][12]

频谱测量用的是android的Spectral View软件, 可测麦克风的频谱瀑布图.

![Testing Audio DAC output using Spectral View android app hw setup 1][13]

耳机输出给手机的话筒.

![Testing Audio DAC output using Spectral View android app hw setup 2][14]

PC-FX2-FPGA loopback 搞定. 上位机使用Python的PyUSB.

![PyUSB and loopback 1][15]

![PyUSB and loopback 2][16]

那么从FPGA到PC就是很简单的事情.

![data send from fpga to python pyusb controlled by encoder][17]

数据由之前设计的NCO提供, 频率也是由编码器控制.

接下来就是ADC采样部分，与ADC之间的通讯逻辑是很简单的，但数据如何发过来是个麻烦的问题，正规的做法是一套抽取的程序，而我为了quick and dirty所以忽略混叠直接用USB的数据输入时钟采样ADC的输出（相当于没有滤波的抽取）。

还有一个问题是差分输入， 同样我也找到了很简单的将一端接在ADC的参考电压上，另一端就可作为单端输入。下图为用函数发生器做输入时，在PC端看到的数据。

![ADC testing using a Function Generator][18]

搞定之后，发现Xilinx自带CIC滤波器的IP，webpack版貌似也可以用，于是用起来。

接下来开始了RF部分的搭建，有点儿着急所以做的很不认真～

![rf block prototype board][19]

第一次做的实验板，目前很多元件都拆到第二块去了。这样子的板上焊贴片真是费劲。第二块：

![rf block prototype board 2][20]

一开始我参考书上的，由一个mosfet（RF用）做前放然后由后面的一个BJT来混频（基极输入），一个BJT来做LO，折腾了几天后，我自觉上RS买了个SA612，回来装上后，立马看到FM信号，现代化真的是好啊。

与ADC的接口也换为TI的THS4521，这样子从前放输出开始，一直到ADC输入都是差分信号。

将原来用RTL-SDR做为数据源的程序换成这个， 顺利的看到了FM电台，但信号很弱，另外只能通过LO调台真是累。而且还发现USB传输速度根本不够，我将USB缓冲区满的标志输出到LED，表现是打开数据读取程序后从常亮变为有点儿暗。

首先怀疑的是PyUSB，于是试用了一下libusb1，在尝试终极的提交多个读取函数，排队读取，但只能达到1秒闪几下的程度，完全达不到不闪的级别。最终我找到了一个用c写的libusb测试程序，结果是几秒偶尔闪一下。

最后我终于相信了某问答论坛上的回答：fx2的缓冲区还是太小，你可以算一下那么小的缓冲区，填满只需要500us（4MB/s，2k缓冲区）。

于是我放弃了高速传输，将传输速度降到1MB/s。

接下来研究了一下Xilinx的FIR IP，用scipy生成了半带滤波器的参数，放了两个在CIC的后面，输出的频谱不再是拱形的了。

再加上了NCO来做复下变频。顺利的听到了FM电台。

![fm spectrum][22]

那么接下来就是要把FM解调部分搬到FPGA里，对于正交信号，有两个选择(方法可参考前面多篇FM解调的文章):

1. 做除法
2. 做反正切

我选择做除法，xilinx的Divide Generator IP， 说实话这是最复杂的一个IP，不是指配置，而是生成时间和占用资源量，或许用Cordic做反正切要容易点儿？在做完FM解调后用FIR做抽取后， 发给之前做好了I2S接口。

![whole board][21]

最后放上演示视频。编码器按下为切换频率调整的精度，粗调和细调。

<embed src="http://player.youku.com/player.php/sid/XMTQwNjQ4NDcxNg==/v.swf" allowFullScreen="true" quality="high" width="480" height="400" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash"></embed>


未完待续.

[1]: {filename}../images/lcsdrgong-cheng/1.jpg
[2]: {filename}../images/lcsdrgong-cheng/2.jpg
[3]: {filename}../images/lcsdrgong-cheng/3.jpg
[4]: {filename}../images/lcsdrgong-cheng/4.jpg
[5]: {filename}../images/lcsdrgong-cheng/5.jpg
[6]: {filename}../images/lcsdrgong-cheng/6.jpg
[7]: {filename}../images/lcsdrgong-cheng/7.jpg
[8]: {filename}../images/lcsdrgong-cheng/8.jpg
[9]: {filename}../images/lcsdrgong-cheng/9.jpg
[10]: {filename}../images/lcsdrgong-cheng/10.png
[11]: {filename}../images/lcsdrgong-cheng/11.png
[12]: {filename}../images/lcsdrgong-cheng/12.png
[13]: {filename}../images/lcsdrgong-cheng/13.jpg
[14]: {filename}../images/lcsdrgong-cheng/14.jpg
[15]: {filename}../images/lcsdrgong-cheng/15.png
[16]: {filename}../images/lcsdrgong-cheng/16.png
[17]: {filename}../images/lcsdrgong-cheng/17.gif
[18]: {filename}../images/lcsdrgong-cheng/18.gif
[19]: {filename}../images/lcsdrgong-cheng/19.jpg
[20]: {filename}../images/lcsdrgong-cheng/20.jpg
[21]: {filename}../images/lcsdrgong-cheng/21.jpg
[22]: {filename}../images/lcsdrgong-cheng/22.png
