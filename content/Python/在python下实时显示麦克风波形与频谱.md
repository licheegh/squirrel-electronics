Title: 在Python下实时显示麦克风波形与频谱
Date: 2015-04-09 18:50
Modified: 2017-01-15 14:51
Category: Python
Tags: Matplotlib,pyaudio,python
Summary: 系列文章之第二, 本文中用之前学到的方法实时显示从pyaudio读取到的麦克风数据.


1. [随机信号]({static}用Matplotlib显示实时信号.md)
2. 麦克风频谱图 <- 本文内容
3. [RTL-SDR频谱图]({static}在python下实时显示rtlsdr波形与频谱.md)
4. [FM解调]({static}在python下通过RTLSDR收听FM广播.md)

[本文程序](https://github.com/licheegh/dig_sig_py_study/blob/master/Analyse_Microphone/audio_fft.py)

运行截图

![程序运行截图]({static}../images/zai-pythonxia-shi-shi-xian-shi-mai-ke-feng-bo-xing-yu-pin-pu/1.gif)

在上一篇中已经实现了实时显示随机的信号, 那么要实现麦克风的音频信号显示, 待实现的就是:

1. 从音频接口读出数据.
2. 转换数据格式, 显示实时波形.
3. 做FFT, 显示频谱.

###音频接口

音频接口用的是[pyaudio](http://people.csail.mit.edu/hubert/pyaudio/), 而且是直接用的Record这个例子, 但读取数据由调用函数读取改为callback读取, 把数据放在了一个queue里面, 这样子写好之后就不用管他了. 需要数据的之后直接读取这个queue就好了.

```python
def audio_callback(in_data, frame_count, time_info, status):
    global ad_rdy_ev

    q.put(in_data)
    ad_rdy_ev.set()
    if counter <= 0:
        return (None,pyaudio.paComplete)
    else:
        return (None,pyaudio.paContinue)
```

另外还包括一个event, *ad_rdy_ev*也就是数据OK时, 通知处理部分程序用的Event.

###数据处理.

这部分我是放在一个thread里面执行的,

```python
def read_audio_thead(q,stream,frames,ad_rdy_ev):
    global rt_data
    global fft_data

    while stream.is_active():
        ad_rdy_ev.wait(timeout=1000)
        if not q.empty():
            #process audio data here
            data=q.get()
            while not q.empty():
                q.get()
            rt_data = np.frombuffer(data,np.dtype('<i2'))
            rt_data = rt_data * window
            fft_temp_data=fftpack.fft(rt_data,rt_data.size,overwrite_x=True)
            fft_data=np.abs(fft_temp_data)[0:fft_temp_data.size/2+1]
            if Recording :
                frames.append(data)
        ad_rdy_ev.clear()
```

这个线程会等待数据OK的event, 在数据OK时, 读出一个数据, 扔掉其他的(我的机器比较慢,不扔掉我发现这个queue会越来越长). 这个数据的转换是通过numpy的frombuffer来实现的. 后边的 `np.dtype('<i2')` 的意思是little endian的16-bit整数, [参考这里](http://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html#arrays-dtypes-constructing).  
数据OK了, 后边进行了处理, 这里加了一个窗后进行fft. 对于一个numpy的array来说, 直接乘就是点乘.

###显示部分

我在显示随机数的那个框架([用Matplotlib显示实时信号]({static}用Matplotlib显示实时信号.md))上做了一些修改, 改成了显示两个axes, 一个是实时波形, 另一个是fft. 且fft这个图的y轴指数的.  
另外我用tkinter做了一个只有退出按钮的小界面, 这样可以控制程序在想退出的时候关闭.

---

这个程序我分别的xp环境下的cmd命令行环境和spyder中都测试了一下, OK, 但在命令行环境时, tkinter的界面会在matplotlib的窗口关掉后才弹出来. 我感觉是在matplotlib会在`plt.show()`时block住程序执行, 其原因未知.
