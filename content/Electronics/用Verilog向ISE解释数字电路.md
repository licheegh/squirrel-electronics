Title: 用Verilog向ISE解释数字电路
Date: 2015-10-21 21:00
Category: Electronics
Tags: FPGA
Summary: 在写Verilog程序时, 做的笔记. 主要解释与Xst的沟通过程.

[TOC]

---

###引言

之前做的XC6SLX25的板子已搞定, 开始写程序了, 本来要总结一下硬件设计部分, 但写了一半画板子太忙就放在那里了. 等有空完善吧~ 

这是完全不同于写单片机程序的感受, ISE的XST你什么时候能明白我的心.

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

未完待续.

[1]: {filename}../images/用Verilog向ISE解释数字电路/1.png
[2]: {filename}../images/用Verilog向ISE解释数字电路/2.png
[3]: {filename}../images/用Verilog向ISE解释数字电路/3.png
[4]: {filename}../images/用Verilog向ISE解释数字电路/4.png
[5]: {filename}../images/用Verilog向ISE解释数字电路/5.png
