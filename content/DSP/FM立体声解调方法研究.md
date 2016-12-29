Title: FM立体声解调方法研究
Date: 2015-07-27 13:00
Modified: 2015-08-13 12:00
Category: DSP
Tags: fm解调
Summary: 介绍了一下啥是FM立体声, 研究了一些FM立体声解码的专利和文章.

[TOC]

###前言
在完成了FM解调后, 我考虑是开始搞硬件呢? 还是搞立体声解调. 于是我花了一天的时间来研究一下看有没有思路, 结论是: 完全不明白该怎么写. 好吧我还是老老实实搞立体声解调吧~

我在wiki上看到了详解,[FM broadcasting - Stereo FM](https://en.wikipedia.org/wiki/FM_broadcasting#Stereo_FM). 我的理解是这样的, 对于非立体声FM来说, 就是音频(基带)直接FM调制到100多M, 而立体声的FM对音频(基带)信号做了手脚, 可以看下面这个图, 图来自wiki.

![FM立体声基带频谱图][1]

低于15k的范围为L+R的音频, 也就是非立体声解调用到的部分. 频率较高的部分中, 一个19k的导频(pilot tone)和23k至53k的L-R音频构成了立体声FM的全部分. 他俩就是用来将L和R声道分开的. wiki上说L-R信号是DSB-SC调制的, 我的理解是L-R乘了一个频率的正弦波, 然后将不用的滤掉, 也有人说就像是AM调制. 至于这个什么导频, wiki上是这样说的

>A 19 kHz pilot tone, at exactly half the 38 kHz sub-carrier frequency and with a precise phase relationship to it, as defined by the formula below, is also generated. This is transmitted at 8–10% of overall modulation level and used by the receiver to regenerate the 38 kHz sub-carrier with the correct phase.

那个L-R信号是这个19k**翻倍**的38k信号来调制的. 而且还与之有精确的相位关系.

1. 为毛不直接给一个38k? 除一半放那里蛋疼不?  

    这个问题我的理解是如果直接给一个38k, 那它就在音频的两个瓣之间, 不容易提取. 而且这个19k信号可以用于判断后边L-R立体声信号的强度.

2. 这有啥相位关系? 我自己搞一个38k出来解调不行么?  

    这个问题我研究了一段时间, 最后在[通信系统 Simon Haykin](http://book.douban.com/subject/1227600/)这本书中找到了答案, 书中 2.3.2 相干检测 中说, 如果用于解调的本振与载波频率之间有相位差, 那么解调出的信号的幅度就会变为cos(相位差)这么大, 因此如果这个差是变化的, 那就幅度调制了. 如果碰巧是某个值, 则输出为0.

而频谱后边53k之后那一堆是数字信号, 本次不研究. OK, 于是我就踏上了翻现成方法的旅途, 找到[Silicon Labs的FM Tutorial](http://www.silabs.com/Marcom%20Documents/Resources/FMTutorial.pdf)找到一幅图.

![FM立体声解调示意图][2]

这图好评啊, 令完全理解不能的我一下子就理解了该如何做. 其中m(t)就是已经fm解调了的信号. 那个rds和57k是数字的,不管它. 那么剩下的都不难, 一堆滤波器和乘法加法. 但那个倍频器是啥? 我学到现在怎么没听说倍频是怎么玩的? 我只听说有种叫(D)PLL的神秘东西可以倍频并锁相, 难道要实现一个DPLL么?

----

###Paper: FM Stereo Receiver Based on Software-Defined Radio

在[这篇paper](http://www.globalcis.org/jdcta/ppl/JDCTA884PPL.pdf)里, 武汉大学的同学对于这个倍频采取的方法是"2 octave", 我搜了半天, 无解, 于是研究了一下里面fpga的连线图, 就是一个简单的平方. 平方可以倍频? 把波形的下半部分移到上半部分就倍频了.       
[Frequency of output of full-wave rectifier](http://electronics.stackexchange.com/questions/86447/frequency-of-output-of-full-wave-rectifier)  
[Why does rectification of a digital signal double the frequency content?](http://electronics.stackexchange.com/questions/11757/why-does-rectification-of-a-digital-signal-double-the-frequency-content)  
这样子做有一些问题, 首先是dc offset, 然后这个正弦波肯定不如原来纯. 那么还有啥先进的方法呢?

----

###US7181018B1 Digital Stereo Recovery Circuitry and Method for Radio Receivers

找了一圈很无奈的我决定翻专利, 痛苦... 在这个Cirrus Logic公司的patent中, 描述了一个pilot doubler的东东.

![US7181018B1 Pilot Doubler][3]

左下角I为19k输入, 然后是一个自乘, 也就是平方, 然后加上一个参数(去除DC), 接下来再乘8, 然后就得到了38k...

![US7181018B1 Stereo Decoder][4]

不过这个19k信号并不是直接BPF滤波出来的, 而是由DPLL提取的, 然后这两之间还有某些交互. 但L-R信号, 确实是19k直接平方去DC后乘解调后信号得到的.

那么这个方法也可以理解为PLL法.

----

###US7079657B2 System and Method of Performing Digital Multi-Channel Audio Signal Decoding

专利为高通的. 在摘要部分说是用于BTSC解调的, BTSC是啥? [Encoder's Spare Channel Embeds Whole-House Stereo Audio in Satellite Set-Top-Box Designs Stably and Cost-Effectively](http://www.analog.com/library/analogDialogue/archives/39-07/btsc.html) ADI的这篇文章介绍了一下, 和FM Stereo差不多哦~[AD1970](http://www.analog.com/media/en/technical-documentation/data-sheets/AD1970.pdf)的说明书也说BTSC的立体声与FM 立体声类似, ADI说了三种方法

1. 直接晶振. 缺点很明显.
2. 用PLL.但是说这个divider需要的除数要求比较高, 所以不适合.
3. 在PLL的反馈路径里加一个AD71028来稳定,辅助生产Master Clock

ok, 看到BTSC和我们这个还是有区别, 看ADI的意思, 这个就需要PLL了. 我们回到这个专利

![US7079657B2 Pilot Detection and DSB demod][5]

可以看到在右下输入信号乘一个信号后出L-R. 文中提到这个恢复的信号需要控制在3度以内(当然这是BTSC), 图中124为8阶IIR BPF, 125这个DPLL由一个PD, cos LUT, loop filter构成. 然后再用一个cos LUT和10阶椭圆低通126来输出L-R. 然后他提到还有具体细节在Scaling adjustment to enhance stereo separation  和 Scaling adjustment using pilot signal 中. 但我看了一下, 和我关心的东西无关. 5555, 高通你们骗我.

当然这还是用的类PLL技术.

----

###US5404405 FM Stereo Decoder and Method Using Digital Signal Processing

公司为Hughes Aircraft Company, 做飞机的公司搞这个干啥? [Hughes @ wiki](https://en.wikipedia.org/wiki/Hughes_Aircraft_Company) 这公司NB, 什么直升机, 卫星, 导弹. 在1994年时搞了[DirectTV](https://zh.wikipedia.org/wiki/DirecTV), 所以在93年搞一个这样的专利可以理解.

![US5404405 Stereo Demod][6]

摘要中说, 他完成了一个不需要PLL的产生38k的方法. 首先先在analog区解调, 然后数字化, 在34那个位置似乎是产生了38k, 下面是传统的产生L与R信号方法. 中间那个Hilbert变换是什么? 老老实实看说明吧.  

文中描述8位置为一连串FIR BPF, 当然他说实现有可能是由LP,HP,BP组合来实现的, 在19k频率的增益为1, 另外强调是线性相位的(FIR不都是么? 我理解错了?). 为了同步, 下面放了一个用于delay的FIR. 接下来在12那个位置, 19k被除去(直接减就可以去掉吗?). 18这是个FIR滤波器, 实现了Hilbert变换, 他说Hilbert对这个19k窄带信号实现了90度相移,而这个FIR的长度需要酌情选择, 他选择15. 这样的话, 这两个信号就是正交的了(哦~原来如此, 这似乎叫什么正交变换吧?)  

然后用三角函数关系来得到38k, 首先I和Q先自乘(平方得到38k?), 然后再一边减一边加, 在30除法器那个位置形成那样的公式, 那么I^2-Q^2就是38k. 这个原理如下图.

![US5404405 公式][7]

而I^2+Q^2按三角函数来说是1, 那么就是38k的幅度. 这个信号接下来要乘原始信号来恢复L-R, 但其幅度波动会影响最终的结果, 因此一般都是用clipping的方法, 但clipping会产生谐波, 干扰L-R信号, 因此除I^2+Q^2可以归一化.

接下来乘2, 据说是传统方法, 为了和L+R匹配. GA为Gain Adjust的意思. OK, 至此核心部分就这些了. **这个方法是很容易理解的, 计算起来也不是很复杂, 很有吸引力哦~**, 因此也可以理解为啥这个专利目前还是已生效状态.

----

###US8406717B1 Digital FM Stereo Receiver Architecture to Recover Carrier Information Based On Stereo or Mono Signals

此乃Marvell公司的专利, 08年还是蛮新的哦.

![US8406717B1 Pilot Tone Recovery][8]

文中的方法为, 首先由410来做BP, 然后由420做平方,

![US8406717B1 Squaring Equation][9]

这公式神奇啊, 没有谐波分量吗? 经查确实是三角恒等式. 然后再经过430滤除低频(直流), 但这样子还不够, 38k的幅度由于立体声协议的要求, 多普勒效应等, 都会造成38k的幅度随时间变化, 那么就需要消除这种影响.   

方法是由450来将平方后信号中的38k除去, 而后在460取反, 那么这里的信号就是1/噪声, 然后再乘38k, 这样子就把这个噪声去掉了.(这和BPF有毛区别?) 那个开关来控制是否使用的这个功能, 还可以定期更新, 等.

----

###US5471534 Devices, Systems and Methods for Composite Signal Decoding Employing Interpolation Filter

来自TI, 看到配图后我震惊了, TI有诚意啊. Marvell那图画的真是烂啊.

![US5471534 Digital Decoder][10]

果然TI延续了写说明书的一贯作风, 看着头疼, 不知所云. fm(t)是已解调的基带信号, 采样率为152k, 为毛是这个呢? TI说有三点:   

1. 在Nyquist以上()  
    106k/2 = 53k 见本文第一幅图.  
2. 这是pilot 19k的整数倍(8)  
    这有啥优势呢? TI解释说这样做出来的DFT 泄漏少. 从而可以通过DFT结果较精确的量出幅度和相位.  
3. 有利于判断什么时候更新音频输出?

接下来在17位置做19k这一点的DFT, 这里输出的I与Q为频域的也就是DFT的输出, 然后求相位, DFT长为128, 这个DFT的计算是有固定的周期的, 首先要保证Pilot最多会在DFT之间飘移6.43度, 而pilot最多会偏出2Hz, TI说这相当于720度/秒, 也就是8.93ms偏6.43度. 然后用8.93ms和152k的fs算出每1357(计算: 8.93/(1/152k) )个sample算一次DFT. 说实话我完全没看懂这是怎么算出来的.

27这个位置算出的相位被用于选择13这个滤波器的核, 而19这个位置算出的19k的幅度被用于产生一个19k信号, 在21中, 共有4个值(sin(n * pi/4), n=1,3,5,7)(明明是8个啊, 152k的采样率, 19k的信号, 难道不是8个一个周期吗?莫非产生的是38k的信号?) 这4个值的幅度由19控制, 然后由25与13的输出一起计算来去掉原信号中的19k.

然后...然后TI给出了源代码...而且每个语句都有注释, TI这是啥意思? 发个专利专门宣传C30这个DSP吗? 另外关键算法竟然是用汇编写的, 于是我默默打开了[TMS320C3x User’s Guide](http://www.ti.com/lit/ug/spru031f/spru031f.pdf)

![US5471534 pilot assembly code]({filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/11.png)

MPYF 的意思是后边两个浮点数相乘, 放在后面的寄存器里.  
LDF load float, 前放后.  
LDI load integer, 前放后.  
SUBF 的意思是浮点减, 前减后,结果放后边.  
NOP 后边这个意思是进行一次dummy read, 应该是让指针+1的意思.  

那么这一段的意思是:幅度 * 4个值的振荡器(为前述的sin(x)), 也就是得出了修正的38k频率. 然后用R0中的值减去它.

![US5471534 pilot assembly code][12]
然后该R2的值根据R1中的值来选择是输出左或右声道. 不是要恢复出38k然后mix的吗? 这么选择不同的数据就可以把L和R都搞出来了? 这时我想到了前面文档关于那个滤波器13说了一堆, 什么插值, 什么相位, 这滤波器如此神奇?

TI说滤波器13由一个polyphase的LPF构成, 通带截至频率为53k, 阻带为99k. 126抽头. 但由于同时做7:1插值, 所以只需要18个抽头. 在每次DFT结束后会根据pilot的相位更新这个FIR的核.

OK, 在研究了一段时间后我发现完全不可理解, 我明白polyphase的这种滤波器可以在滤波插值的同时做下变频, 但那个L+R之类的东西要做加减法的, 滤波器连这个也顺便搞定了么? 在看到ref列表中有TI一个1991年的专利, 好吧, 我研究下那个.

1991年的US5239585文中开头提到US4723288这个专利, 这个是Motorola(现在是Freescale)在1986年的专利, OK, 那先搞这个.

----

###US4723288 Stereo Decoding by Direct Time Sampling

1986年~和我差不多大哦~

摘要介绍: 根据导频的相位来对立体声信号进行采样, 左右声道可以直接采样得到. (这真tm神奇), 然后moto很热心的介绍了一下当年的prior art是怎么解调立体声的, 写了一整篇.

![US4723288 stereo decoder][13]

此图为moto的方案, 到C那个位置, 后边两个mixer取名为Sampler(采样器), 下面乘的是单位脉冲函数, 频率为38k, 与pilot用PLL同步, 也可以理解为再此ADC. **两个samper的周期差180度, 左声道为19k信号的45度和225度,右边为135度和315度.  然后LP后直接出L和R.** moto给了个奇怪的公式, 这式子如何和那些东西联系起来的?

![US4723288 digital form][14]

后边moto给出了个全数字的方案, 用一个DLL来做. 其中提到采样时钟为152k. 必须为76k且大于等于152k.

好吧我还是看看TI的这一篇吧.

----

###US5239585 Devices, Systems, and Methods for Composite Signal Decoding

在摘要中, TI说这个方案不需要采样与Pilot的相位同步, 才用一个叫曲线拟合滤波器的东西来做插值, 而这个滤波器的核是由一个选择器确定的, 这个选择器由相位测量来获得本振与Pilot之间的相位差来选择滤波器的核. 因此可以不用同步, 且输出采样率也可以随便选.

那么这个和US5471534是差不多的原理.

![US5239585 stereo demod][15]

然后TI讲了一下他对US4723288的理解.

![US5239585 equ 1][16]

当38k的载波sin(2ωt)等于+1或者-1时, fm(t)分别等于2L和2R, 再加上19k的pilot. 由于载波是和19k的pilot同步的, 因此pilot就可以用于判断合适应该做sample. 那么这些位置位于pilot的相位在奇数 * 45的位置(也就是45 * 1 = 45度, 45 * 3 = 135度, 45 * 5 = 225度, 45 * 7 = 315度).

好吧, 很简单的道理.

TI也说了一下moto这个东东的缺点, 他说如果相位差了一点儿, 那么就会导致信号的衰减. 所以之前那个专利里, 用了一下PLL, 说这个东东不好实现, 而且这个实现还需要是38k的整数倍.

总的来说这个方案和US5471534的方案基本原理是完全一样的, 只是具体各部分的实现方式不同. 1000部分的功能就是之前的FFT功能, 3000中的和之前的基本一样, 2000中的有些小区别. 所谓的Curve-Fitting就是在插0值后进行的LP滤波.

为啥要插值呢? 滤波器126的采样率为152k, 也就是在19k时, 每周期8次, 如下图, 在0度, 45度, 90度....位置采样, 当然这是在内部采样时钟与输入信号完全同步的情况下. 那么这时, 把前述的那几个角度的采样点的值直接搞出来就是L和R了. 当不同步时, 如输入和采样差15度, 那么在45度采样的值实际上是在30度的, 如果想要45度的采样点, 则需要取得60度时的值, 那么这时, 就可以用插值来得出60度的值.

![US5239585 phasor][17]

图中为插2个点(3:1 插值), 则共有8+8*N, N=2, 也就是24个点. 那么这时的分辨率为360/24=15度. 采样率由152k升为456k. TI说多用的是插6个点也就是7:1的插值, 分辨率为360/56=6.43度. 采样率为1.064M

![US5239585 equ 2][18]

首先, 设L为0, R为1, 那么equ1 就简化为 equ2, 但其中pilot已经删掉了, 加入了一个θ, 也就是要求的角度. 那么要30dB的分离度, 那么就是说此时要在采样L时得到一个比-30dB小的值, L的角度为45度, 对于38k来说就是90度, 因此得出equ3(左边为20log). 求出θ, 也就是说在38k情况下需要14.5度. 14.5度是多长时间呢? equ4求出为1.05us. 也就是说要达到947.5k的采样率, 6.2:1的插值, 就可以实现30dB. 因此TI选择7:1.

----

###US6901146 All-Digital FM Stereo Demodulator and Demodulation Method

来自Mitsubishi的方案, 采用的方法与之前类似, 但他介绍说他是从一篇论文得到的灵感[A DSP-Based Stereo Decoder for Automotive Radio](http://papers.sae.org/900244/), 这篇我没找到, 就只能看三菱写的读后感了.

![US6901146 prior art][19]

可以看到是调整ADC的采样来获得L和R的, 他说在11位置, 产生的是VCO相位和输入pilot之间的差, 然后通过这个差来控制VCO来实现类似PLL的锁定相位的功能. 12,13构成的功能是根据输入的频率信号来分频除8, 后控制一个8个sample大小的LUT来产生mix用的信号. 两个频率一样, 相位不同的信号乘后产生一个固定的偏差? 参考[三角恒等式](https://zh.wikipedia.org/zh/%E4%B8%89%E8%A7%92%E6%81%92%E7%AD%89%E5%BC%8F)的积化和差等式,
结果为一个倍频信号+ or - 一个固定的直流信号. 本方案里, 这个直流信号用来控制VCO.

而且13还控制着7和8的latch.

![US6901146 embodiment 1][20]

于是三菱进行了改进, 将原有的VCO部分用一个类似NCO的东东代替, 而ADC为固定采样率, 由MCLK(4.864M)来提供, 由于12这个table大小为8, 因此最佳的内部采样率为19k*8=152k(也就是8个采样一个周期,刚好为19k), 那么5和4应该为除32.

15这个东东控制着5和16这两个counter, 16的M值由15来设定, 同时15控制5是增加N还是减少N. 16由5来控制计数, 而M由15决定, 在每个M count, 16会复位且让5根据15的命令来增加或减少.

如当15设16为31, 然后M每31个count调整5从32至31. 那么就调整了参考频率的(M\*N-1)/(M\*N)(原文为(M-N-1)/(M-N)=991/992 ?)也就是增加了0.1%.

好吧, 我理理, 采样频率为4.864M, 那么对于38k信号来说是每个周期有128个采样(分辨率2.8度), 当抽取32时, 则是每个周期4个采样, 如果刚好同频率的话, 那么就刚好可以采出L和R, 如果有调整, 如是31时, 则是4.129个采样, 换句话说, 此时的内部采样频率为156.9k与之前在32时的152k相差4.9k 也就是差不多3%的样子. 而三菱说是0.1% ? 为啥?

然后三菱又介绍了一堆类似的方案.

----

###US4630299 Digital Circuit for Decoding Digitized, Demodulated FM Stereo Signals

通用首先采用一个IIR滤波器来得到19k, 描述IIR的部分完全没有看懂, 既然后边的直接乘的, 那么在相位上肯定也是有一些补偿.

![US4630299 embodiment][21]

然后与delay 90度后的信号相乘, 也是采用积化和差公式

![US4630299 equ][22]

当两个角度一致时, 则sin*cos可以产生倍频信号, 其实这和之前的平方倍频是完全一致的道理. 该专利还有中文版本 CN86100932.


----

###US20060251196 Recovering a Signal Without a Phase Locked Loop

CN1826741A 是中文版, 看到配图我也是醉了. 飞利浦你想怎么样?

![US4630299 1][23]

首先他说US5404405 也就是Hughes Aircraft Company搞的那个方案的8那个BPF很复杂, 不容易实现. 29为BPF滤波器, 28为一个固定的振荡器, 22(可用cordic来实现)比较这两个信号的相位差后, 加这个相位差到信号21的相位上, 在加上一个用于补偿22的delay用的常数. 之后这个信号平方来倍频.

我的理解是, 比如本来BPF出来的信号是有噪声的, 鉴频器(应是比较抗噪声干扰的, 如经过LP)就可以得到与纯净信号的相位差, 然后调整这个纯净信号的相位与原信号同步, 则用这个19k来解调L-R就要好的多. 嗯~就是这么个意思.

![US4630299 2][24]

飞利浦还有个这方案, 在前面的方案基础上加上30这个mixer, 那么30的输出就和之前三菱的方案有些类似, 但后边的处理是完全一样的吗? 如果有相位差, mixer之后不就是个直流了吗? 为什么还要鉴频呢? 飞利浦只解释说这样子29那个滤波器只需要设计一个LP就可以了, 不用BPF.

----

###US6714651B2 FM Stereo Signal Demoudulating Apparatus and Method

历时半个月的痛苦的看资料终于要结束了, 这是最后一个. 来自先锋.

![US6714651 prior art][25]

这是号称之前的方案, 图4中, 30为倍19k -> 38k的东东, 其他的是老样子, 只是画法不同, 图5详细描述倍频方案. 这个图的理解需要结合下图.

![US6714651 wave forms][27]

输入为3A波形, 3B为delay了90度的波形, 那么这两个做XOR后就是3C, 3D是3C delay 90度后的结果, 3E为XOR的结果(此时应该为19k*4=76k), 3F为inv后delay 90度的结果, 3C与3F做XOR的结果为3G. 然后乘上一个系数, 再与3C相加, 就得到了31这个波形图. 频率为38k.(真tm神奇). 然后先锋说这东西有缺点, 在图4, 31乘法器位置, 31的输出m与FM信号n相乘时, 这个乘法需要运算量大, 成本高.

![US6714651 embodiment][26]

先锋说在倍频器里, 去掉了点东东, 直接输出信号3C和3G. 那么这时, 就是乘1和0了, 而不是乘一个小数, 当乘1时不变, 乘0时反向, 然后要乘一个小数(这不还是要乘么?), 然后先锋解释说这个乘法可以近似为乘0.5, 也就是向低位移一位, 或者更接近一点儿 2^(-1)-2^(-4)-2^(-6)-2^(-7) (mathjax访问实在是慢T_T).

这是啥原理? 没有mathjax我就贴个图吧~

![US6714651 equ 1][28]

![US6714651 equ 2][29]

其实就是把f(m)乘进去而已~

###总结

看的好辛苦, 先总结一下吧.

1. PLL产生38k法.
2. 三角恒等式法.
    * 正交变换产生38k法或者说是二倍角法.
    * 平方产生38k法或着说是积化和差法.
3. moto/TI的固定相位采样法.
4. 先锋的神奇++--XOR产生38k法.

当然这不是全部的FM Stereo解调算法, 还有很多专利我都没看或没怎么看懂, 另外还有n多paper我没看懂或没下到, 因此这只是冰山一脚.



[1]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/1.png
[2]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/2.png
[3]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/3.png
[4]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/4.png
[5]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/5.png
[6]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/6.png
[7]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/7.png
[8]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/8.png
[9]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/9.png
[10]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/10.png
[11]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/11.png
[12]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/12.png
[13]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/13.png
[14]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/14.png
[15]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/15.png
[16]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/16.png
[17]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/17.png
[18]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/18.png
[19]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/19.png
[20]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/20.png
[21]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/21.png
[22]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/22.png
[23]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/23.png
[24]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/24.png
[25]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/25.png
[26]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/26.png
[27]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/27.png
[28]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/28.gif
[29]: {filename}../images/fmli-ti-sheng-jie-diao-fang-fa-yan-jiu/29.gif
