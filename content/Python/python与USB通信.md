Title: python与USB通信
Date: 2015-11-04 12:13
Modified: 2018-01-17 12:00
Category: Python
Tags: USB, Python
Summary: 上位机与CY7C68013A的USB通信, 自然是要用Python来完成.

[TOC]

---

本文提到的代码位于[LCSDR的github中](https://github.com/licheegh/LCSDR)。

首先当然是看看在硬件设计阶段[选择用于低成本软件无线电的FPGA]({static}../Electronics/选择用于低成本软件无线电的FPGA.md)查到的[PyUSB](https://walac.github.io/pyusb/).

PyUSB依赖于一些USB的驱动程序, 这个貌似叫做[无驱驱动](http://wenku.baidu.com/view/98ebaf4a2b160b4e767fcfbe.html), 其中libusb是一统天下者, 当然就要用这个咯. 那么问题来了, libusb这个驱动是怎么装到要开发的设备上呢? 在windows下答案是[Zadig](http://zadig.akeo.ie/), 这个和rtlsdr用的方案是一致的.

下载了最新的Zadig然后选list all device, 可选择的列表里只有WinUSB(这是微软的吧?), libusbk(贵圈好乱), libusb-win32. libusb官网不是说和libusb-win32合并了么? 好吧, 只有选这个了. 但这个相当于libusb 0.1版本的, 估计和OS有关, 我是老迈的xp.

装上后, 给Python装上PyUSB(官网下载后, 按里面说明装),

```python
import usb

usb.core.show_devices()

```

![cmd successful shot][1]

呵呵~好简单~ [PyUSB教程](https://github.com/walac/pyusb/blob/master/docs/tutorial.rst), 文档: 建一个bat文件 `pydoc -b` 运行, 然后在浏览器里找到usb这个package的帮助.

接下来搞PC-FX2-FPGA的Loopback, 悲剧, 在用device那个类的write方法给端点写数据时, 很是诡异, 各种错, 但按照AN61345中描述的用Control Center收发一个文件数据的方法, 工作正常, 经仔细思考, 可能有以下层面问题:

1. Cypress的FX2LP 工作在slave FIFO + 自动发包模式时, 在向上位机机发送时, 没满一个包是不会发的, 因此数数很重要, 数不对就等着timeout吧.
2. FPGA部分copy的Cypress的AN61345, 自己只是写了个简单的testbench玩了一下, 与其说是验证功能, 不如说是我学习它的工作原理.
3. cy7c68013a FW bug, 这个也是copy的AN61345.
4. PyUSB坑爹 or Python代码问题.
5. 硬件错误.

于是为了简化问题, 上逻辑分析仪, 另外把这个打包的大小改小. 于是我查了 **USB Spec 2.0** 5.8.3 Bulk Transfer Packet Size Constraints, 并没有直说不能设小, 那就没问题咯, 于是在FX2中改了AUTOINLEN寄存器(slave.c)和Endpoint Descriptor(dscr.asm) 为2B, 尝试python继续各种错, 逻辑分析仪一看, 这是啥情况?

![Slave FIFO waveform for 1 word transfer between FPGA and FX2LP][2]

解释: Channel0 为clk, 10M, 由于采样率不够(?)的原因, 因此看起来奇怪, slrd与sloe拉低(有效)是因为看到FLAG A, 也就是EP2 EF(Empty Flag)拉高(不是Empty了), 这是应从FX2读入fpga的FIFO, 读完后由于FLAG A回到低, 此时应是从FPGA的FIFO到FX2, 可以看到FIFOADD选择了EP6, FLAG B是EP6的FF(Full Flag), 高意思是现在不是满的, 可以写. 但此时slwr应该拉低才对啊?

![Slave FIFO waveform for 2 word transfer between FPGA and FX2LP][3]

发2 word时, slwr工作正常. 但是, 细节图:

![Slave FIFO waveform for 2 word transfer between FPGA and FX2LP in detail][4]

只写了一个word(上升沿写入). 为毛少一个?

纠结一段时间后终于找到问题, 而且是通过fpga的testbench找到的, 在看cy7c68013a的datasheet时, Slave FIFO Synchronous Write的那个图给了我灵感, 在数据读出后, Flag(由FX2驱动)会改变状态, 这个时间是tXFLG, 最大10ns. 于是我在isim里试了一下, 悲剧. 1个word.

![Slave FIFO waveform for 1 word transfer between FPGA and FX2LP in isim][5]

2个word, 少发一个. SLWR也只有一个.

![Slave FIFO waveform for 2 word transfer between FPGA and FX2LP in isim][6]

```verilog
always@(*)begin
    if((current_loop_back_state == loop_back_read) & (flag_ef == 1'b1))begin
        slrd_n = 1'b0;
        sloe_n = 1'b0;
    end else begin
        slrd_n = 1'b1;
        sloe_n = 1'b1;
    end
end

always@(*) begin
...
        loop_back_read:begin
            if(flag_ef == 1'b0)
                next_loop_back_state = loop_back_wait_flag_ff;
            else
                next_loop_back_state = loop_back_read;
        end
...
```

问题代码, 这样子生成的组合逻辑, 只要FLAG EF是1, 就会让slrd和sloe拉低. 且会转换状态为wait_flag_ff. 也就是说会在FIFO锁存数据的同时转换状态, 则应是存在一个竞争关系. 于是我把slrd和sloe换为钟控.

![Slave FIFO waveform for 2 word transfer between FPGA and FX2LP in isim][7]

搞定.

![Slave FIFO waveform for 1 word transfer between FPGA and FX2LP success][8]

实测1个word.

后来又发现传输数据时, 多向FPGA内的FIFO写一个数据, 在和Cypress的例程战斗了一段时间后, 我最终放弃了, 自己写了一个状态机, 加一个Xilinx的FIFO IP, 搞定.

![last working fpga fw 1][9]

![last working fpga fw 2][10]

全对. :)

接下来实现了从FPGA发送数据到Python.

![data send from fpga to python pyusb controlled by encoder][11]

Python显示实时数据的框架由之前[在python下实时显示麦克风波形与频谱]({static}在python下实时显示麦克风波形与频谱.md)提供. 将数据源从pyaudio换为PyUSB, 搞定.


[1]: {static}../images/pythonyu-usbtong-xin/1.png
[2]: {static}../images/pythonyu-usbtong-xin/2.png
[3]: {static}../images/pythonyu-usbtong-xin/3.png
[4]: {static}../images/pythonyu-usbtong-xin/4.png
[5]: {static}../images/pythonyu-usbtong-xin/5.png
[6]: {static}../images/pythonyu-usbtong-xin/6.png
[7]: {static}../images/pythonyu-usbtong-xin/7.png
[8]: {static}../images/pythonyu-usbtong-xin/8.png
[9]: {static}../images/pythonyu-usbtong-xin/9.png
[10]: {static}../images/pythonyu-usbtong-xin/10.png
[11]: {static}../images/pythonyu-usbtong-xin/11.gif
