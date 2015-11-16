Title: 用Verilog向ISE解释数字电路
Date: 2015-10-21 21:00
Modified: 2015-11-02 17:00
Category: Electronics
Tags: FPGA
Summary: 在写Verilog程序时, 做的笔记. 主要解释与Xst的沟通过程. (一个强迫症患者和Xst警告的纠缠过程)

[TOC]

---

###引言

之前做的XC6SLX25的板子已搞定, 开始写程序了, 本来要总结一下硬件设计部分, 但写了一半画板子太忙就放在那里了. 等有空完善吧~ 

这是完全不同于写单片机程序的感受, ISE的XST你什么时候能明白我的心, 另外能不能照顾一下我强迫症患者的心, 不要再给警告了,

注意: 这是FPGA入门者写的文章, 因此仅供参考.

###关于FF(Flip-Flop)的Reset和Set.

这个问题是这样开始的, 我要做的是一个4象限编码器(就是常用于面板的飞梭)的解码电路,去抖没有问题(3个FF流水线, 然后组合逻辑判断, 采样率1ms), 问题出在后面的输出电路上.

上升沿的到来只有一个周期的持续时间, 我想实现在没有上升沿时, 保持当前的方向指示不变, 也就是说保持之前的状态不变, 只有有脉冲来时才变化, 那么最简单的就是直接用上升沿信号做FF的时钟触发了, 但这样会报 PhysDesignRules:372 - Gated clock 警告, 然后我换成了电平触发, 但报 Xst: 3002 警告, 大概意思是存在竞争的可能, 在最后我把同一段代码移到时钟触发的always内, 妥了.

那么最终我实现的是, 信号首先进一堆FF, 然后一堆组合逻辑, 输出用FF锁存.

OK, 进入主题, 在研究 Xst: 3002 时, 我发现Xilinx的WP309 Targeting and Retargeting Guide for Spartan-6 FPGAs, 中有多项入门级别的与XST沟通的建议, 于是仔细看了一遍, 里面说新的Spartan-6的FF只能有一个Set或Reset输入, 去掉了之前的REV.

![FF difference between spartan-3 spartan-6 artix-3][1]

图中, spartan-3的截图来自UG331, 6和7的来自SliceM. 看到7系列全是这屎样子我也是松了口气, 还好没被坑.

这和我有啥关系呢~因为我在RTL schematic中看到了这玩意儿, 如下图:

![fdrs in RTL schematic][2]

这玩意儿在解码器的输出位置(dir=direction), 原理是当Set有效时, 在时钟(连线未显示)沿到来时, FF会保持输出1, 而Reset时相反, 和以下代码吻合:

```verilog
    always @ (posedge clk) begin

        if (ina_lead)
            dir_out <= 1;
        else if (inb_lead)
            dir_out <= 0;

    ...

```

那么FF只有一个Set/Reset引脚, 怎么办呢? Technology schematic: 

![fdrs in Technology schematic][3]

注意原来FDRS的D,Q环路被一个啥也没有的FF和两个LUT代替.其中的LUT6:

![LUT6 in Technology schematic][4]

其中的LUT3:

![LUT3 in Technology schematic][5]

少了一个Reset需要这么复杂吗? 已晕, 但也没什么好办法, 除非~修改解码器的输出为类似一个增加时钟, 一个减少时钟. 这样应该会避免这个问题吧~

###关于时钟输出.

当你想将一个时钟信号输出时, 就会遇到这个提示, Place:1136, 此时只要将这个时钟信号用下面这个ODDR2来Buffer一下就OK, 

```verilog
ODDR2 #(
    .DDR_ALIGNMENT("NONE"), // Sets output alignment to "NONE", "C0" or "C1" 
    .INIT(1'b0),    // Sets initial state of the Q output to 1'b0 or 1'b1
    .SRTYPE("SYNC") // Specifies "SYNC" or "ASYNC" set/reset
) ODDR2_inst (
    .Q(clk_output),   // 1-bit DDR output data
    .C0(clk_input),   // 1-bit clock input
    .C1(!clk_input),   // 1-bit clock input
    .CE(1'b1), // 1-bit clock enable input
    .D0(1'b1), // 1-bit data input (associated with C0)
    .D1(1'b0), // 1-bit data input (associated with C1)
    .R(1'b0),   // 1-bit reset input
    .S(1'b0)    // 1-bit set input
);
```

那么这个ODDR2是什么东东? 占用一个有什么影响呢? 根据UG381, ODDR2是属于OLOGIC2的一部分, 也就是说如果占用一个ODDR2, 则就会占用一个OLOGIC2, 那么OLOGIC2是什么呢? 下图来自FPGA Editor:

![OLOGIC2 in FPGA Editor 1][6]

上面的4个分别是4个IO的pad, 然后两个两个连到下面的两部分上.

![OLOGIC2 in FPGA Editor 2][7]

其中一个的放大图, 由ILOGIC, IODELAY, OLOGIC三个构成, 一个部分有两组, 这样子成双成对应当是为了差分信号. **也就是说每个IO口都有对应的一个OLOGIC可用.** 我记得每个IO口还有什么串转并的SERDES接口又是什么? 

![OLOGIC2 OSERDES in Design Summary][8]

在确认OLOGIC的使用状态时, 看到Design Summery中有这样的写法, 也就是说一个OLOGIC2也可以作为一个OSERDES2来用咯.

参考资料:

* <http://www.xilinx.com/support/answers/35032.html>
* <http://www.xilinx.com/support/answers/41810.html>
* <http://www.edaboard.com/thread206190.html>
* <http://www.edaboard.com/thread197895.html>
* Clock Forwarding xilinx
* <http://www.edaboard.com/thread204985.html>

###NCO/DDS的设计

在写一个NCO的时候, 我正在因为用Python超简单的就生成了ram文件而happy时, XST却告诉我, PhysDesignRules:2410 警告, [Design Advisory for Spartan-6 FPGA - 9K Block RAM Initialization Support](http://www.xilinx.com/support/answers/39999.html) 嗯~是个硬件bug, 虽然在搞PCB之前也读过errata, 但大部分有啥影响我是完全搞不懂啊, 仔细研究后发现只要不加密, ISE会自动搞定这个问题.

后来增加到了使用1k的16bit ROM, XST贴心的给用上了18Kb ram, 警告没有了.

另外研究了一下DDS, 我的还是很简单的嘛~可加入的功能如下:

1. Phase dithering
2. Trigonometric Correction
3. 减少ROM使用, 可使用一半或4分之一的ROM大小.
4. 使用truncated相位累加器来增加可调频率范围.

另外Saleae的逻辑分析仪软件真是好用啊, 虽然俺的是在马云家买的, 但依旧好用, 让我1天就搞定了I2S接口, 最后有个Bug是L和R的时钟周期数不同, Saleae也有提示, 于是就迎刃而解了.

![Saleae Logic help me alot][9]

参考资料:

* Digital Frequency Synthesis Demystified by Bar-Giora Goldberg 好书, 要做DDS的话好好研究下.
* Lattice NCO IP Core User Guide.
* Xilinx DDS Compiler v5.0 Product Guide.

###关于Post-Translate仿真

Xilinx貌似不是很推荐经常用这个来验证功能, 第一次在仿真页面, 像是在Behavioral里面那样的直接点Simulate Behavioral Model, 会报错:

ERROR:Simulator:702

经查找说是如果要仿真的东东**不是顶层模块**, 则要打开在Implementation中的Implement Design-Translate-Generate Post-Translate Simulation Model 的右键中的 Generate Multiple Hierarchical Netlist Files 打勾, 然后才可以. 

然后我打勾, 说生成Model失败, 且无原因, 这条之前只有个info说什么clock wizard生成的那个IP如何如何.





未完待续.

[1]: {filename}../images/用Verilog向ISE解释数字电路/1.png
[2]: {filename}../images/用Verilog向ISE解释数字电路/2.png
[3]: {filename}../images/用Verilog向ISE解释数字电路/3.png
[4]: {filename}../images/用Verilog向ISE解释数字电路/4.png
[5]: {filename}../images/用Verilog向ISE解释数字电路/5.png
[6]: {filename}../images/用Verilog向ISE解释数字电路/6.png
[7]: {filename}../images/用Verilog向ISE解释数字电路/7.png
[8]: {filename}../images/用Verilog向ISE解释数字电路/8.png
[9]: {filename}../images/用Verilog向ISE解释数字电路/9.png
