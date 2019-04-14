Title: 在python下通过RTLSDR收听FM广播
Date: 2015-04-14 12:13
Category: Python
Tags: rtlsdr,fm解调,Matplotlib,python
Summary: 系列文章之第四, 本文是最终篇, 汇集之前所学, 写一个在python下的FM收音机.


1. [随机信号]({static}用Matplotlib显示实时信号.md)
2. [麦克风频谱图]({static}在python下实时显示麦克风波形与频谱.md)
3. [RTL-SDR频谱图]({static}在python下实时显示rtlsdr波形与频谱.md)
4. FM解调 <- 本文内容

[本文程序](https://github.com/licheegh/dig_sig_py_study/blob/master/RTL_PY/fm_radio.py)

在之前已经实现了实时显示RTLSDR的数据, 并且[学习了librtlsdr中的fm解调程序]({static}../DSP/阅读librtlsdr中的rtl_fm程序.md), 接下来就是抄一下rtl_fm把音频信号解调出来, 输出到pyaudio就大功告成了.  
步骤:

1. 抽取
2. 反正切.
3. 输出给pyaudio.

###抽取

之前我以为这就是个普通的滤波器, 只要研究明白需要设置的转折频率与阶数就可以, 但...事实证明这玩意儿比较复杂. 在看了[数字信号处理](http://book.douban.com/subject/1450818/)的第10章后, 我发现这滤波器水很深, 有书名为[Multirate Systems and Filter Banks](http://book.douban.com/subject/3916055/)专门讲这个, 这类型的书不止一本. 而[xilinx的一篇文章](http://china.xilinx.com/china/xcell/xl35/19-27.pdf)也在开篇写到

>过去半年有几位客户请我帮助他们设计和实现数字下变频器所用的降采样(即"抽取")滤波器,这种滤波器在软件无线电与数据采集类应用中都很常见.
>这项工作即便对于经验丰富的设计师也不是一件小事.

我要吐槽一下为啥有客户需要让xilinx公司帮着设计? 那客户公司的工程师干什么? 只画板子吗?

按照书中的描述, 这个滤波器的复杂度和要抽取的比例(因子)有关, 比如我现在要做的从1MSPS -> 44.1kSPS(音频的采样率), 需要大概20倍的抽取. 那么问题来了, 这两个肯定不是整数比例, 于是我上网研究了一下. [rtl_fm的作者](http://kmkeen.com/rtl-demod-guide/)提到他是将后边音频所需的采样率转换交给Sox来处理. 另外在[NI的这篇文章](http://www.ni.com/white-paper/13193/en/) 也是如此处理, 还有[mathlab的这篇](http://cn.mathworks.com/help/supportpkg/usrpradio/examples/fm-monophonic-receiver-with-usrp-r-hardware.html)

>Sox will automatically resample the audio to keep your soundcard happy and can apply denoising filters to keep your ears happy.

这让我郁闷了一段时间, 还特意买了本书回来看 [通信系统中的多采样率信号处理](http://book.douban.com/subject/3544815/), 但后来我想到何必纠结于如此奇怪的采样率转换, 声卡肯定是可以调采样率的, 如果两边差一个整数倍就OK啦. 但google了一番一无所获, 没人讨论这个啊, 于是我试了一下, 结果发现在RTL-SDR的最低采样率250k的1/10, 也就是25k, 声卡工作完全正常. 嗯, 那就直接抽取到1/10就可以啦. [scipy的decimate](http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html)就可以完成这个工作.

###反正切

numpy具有arctan2函数, 但它同时还有一个专门[求复数角度的angle函数](http://docs.scipy.org/doc/numpy/reference/generated/numpy.angle.html), 这样就不用分开复数实部和虚部, 直接把复数数据给angle函数就OK.

但是在实际中, 我发现这个处理的步骤有问题, 之所以要先抽取后做反正切, 原因是为了减少运算量, 问题就出在这里: **当采样率降低后, 采样点之间的复角变化也加大了.**为了找到这个结论, 我专门写了一个[验证FM解调的程序](https://github.com/licheegh/dig_sig_py_study/blob/master/RTL_PY/fm_mod_demod.py)来调试不同的方法.

首先介绍一下信号产生方法
```python
m=3.1
C=0
T=np.arange(0,RFSIZE,1)
xInput = np.cos(2*np.pi*T*(4/RFSIZE))
xOuput = np.cos(m*xInput+2*np.pi*T*(C/RFSIZE))+1j*np.sin(m*xInput+2*np.pi*T*(C/RFSIZE))
```
xInput是一个余弦波, 其频率由4/RFSIZE来控制, 4意味着可以在一个Buffer中有4个周期. 然后这个信号用于改变下面这两个cos和sin和频率. 其中C的意思是载波频率, 由于我们可以调整rtl-sdr来把载波去掉, 因此设为0, m为调制度, 可以看到m是乘上xInput来控制频率的. 因此m越大频率变化范围越大.

方法1: 抽取-取反正切-求差.
```python
xCa=signal.decimate(xCa,DOWN_FACTOR,ftype="fir")
angle_data=np.angle(xCa)
audiodata=np.diff(angle_data)
```

![解调方法1 调制度3.1]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/1.png)

第一行为输入信号, 中间两行为调制后的real和imag波形, 最后为解调后的信号. 这时的调制度是3.1. 我们增加到3.2, 程序就会出现问题.

![解调方法1 调制度3.2]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/2.png)

输出出现了尖峰, 它是由于

![解调出现尖峰的原因]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/3.png)

从-pi到pi的转换导致的尖峰.

方法2: 加上unwrap
```python
audiodata=signal.decimate(xCa,DOWN_FACTOR,ftype="fir")
angle_data=np.angle(audiodata)
audioda=np.diff(angle_data)
audiodata=np.unwrap(audioda)
```

![解调方法2 调制度3.2]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/4.png)

可以看到这个unwrap程序神奇的把错误的尖峰去掉了.

![unwrap结果]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/5.png)

但在调制度增加到300时, unwrap的结果也不是很好看.

![解调方法2 调制度300]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/6.png)

方法3: 求反正切-求差-unwrap-抽取

将抽取放在后面, 可以很显著的减少每个采样间的角度差.

![解调方法3 调制度300]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/7.png)

当然这样也还是有上限. 调制度1000000.

![解调方法3 调制度1000]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/8.png)

###输出给Pyaudio

将数据转换为音频格式我也是研究了好一会儿.

```python
audiodata_amp=audiodata*1e4
snd_data = audiodata_amp.astype(np.dtype('<i2')).tostring()
```

###线程问题

在程序终于输出广播后真是令人高兴啊, 但随之而来的是经常弹出错误:

![解调方法3 调制度1000]({static}../images/zai-pythonxia-tong-guo-rtlsdrshou-ting-fmyan-bo/9.jpg)

这是为啥呢~搜到[Python's Hardest Problem](http://www.jeffknupp.com/blog/2012/03/31/pythons-hardest-problem/), 然后似乎明白了, 我猜测是这样子的, 我的thread中有callback的程序, 而且还是block的, 那么当有数据需要写入时, python的GIL还没有运行到这个thread, 或者在数据复制时GIL切换了thread, 那么有可能会造成这个问题. 那么把那个rtlsdr的callback换成直接读取不就OK了么? 换了read_samples以后, 我发现不行, 直接读取的这个函数会丢数据.

好吧, 于是我把程序写成了multiprocessing模式. 就再也没出那个错误.
