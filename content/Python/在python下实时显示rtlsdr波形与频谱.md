Title: 在python下实时显示rtlsdr波形与频谱
Date: 2015-04-10 17:18
Category: Python
Tags: Matplotlib,rtlsdr,python
Summary: 系列文章之第三, 本文中用之前学到的方法实时显示从rtl-sdr读取到的数据. 也就是简单的把信号源从麦克风换为rtl-sdr.


1. [随机信号]({filename}用Matplotlib显示实时信号.md)
2. [麦克风频谱图]({filename}在python下实时显示麦克风波形与频谱.md)
3. RTL-SDR频谱图 <- 本文内容
4. [FM解调]({filename}在python下通过RTLSDR收听FM广播.md)

[本文程序](https://github.com/licheegh/dig_sig_py_study/blob/master/RTL_PY/sdr_fft.py)

运行截图

![程序运行截图]({filename}../images/在python下实时显示rtlsdr波形与频谱/4.png)

之前已经实现了从声卡读取数据再显示, 那么现在用在rtlsdr上, 就只是读数据接口的问题, 只要把读取数据的接口换成rtlsdr的, 外加一些数据转换, 就OK.

这里用的python库是[pyrtlsdr](https://github.com/roger-/pyrtlsdr)试用了一下两个例子, [demo_waterfall.py](https://github.com/roger-/pyrtlsdr/blob/master/demo_waterfall.py) 都做成这个高级样子了... 当然我自己的还是要继续写的.

![demo_waterfall.py运行截图]({filename}../images/在python下实时显示rtlsdr波形与频谱/1.JPG)

我在test.py中看到有这么个函数, 嗯~这不是和pyaudio中的一样嘛, 于是我兴高采烈的换上去试了一下.

```python
    sdr.read_samples_async(test_callback, 256*1024)
```

其间我注意到test.py中有个奇怪的地方

```python
@limit_calls(2) # 这是啥?
def test_callback(samples, rtlsdr_obj):
    print('  in callback')
    print('  signal mean:', sum(samples)/len(samples))
```

经查询发现这个函数位于helpers.py, 意思是这函数只被调用两次就结束. 另外在rtlsdr.py中的read_samples_async()函数下面

```python
    def cancel_read_async(self):
        ''' Cancel async read. This should be called eventually when using async
        reads, or callbacks will never stop. See also decorators limit_time()
        and limit_calls() in helpers.py.
        '''
```

结束async就关闭设备好了, 为啥要cancel? **callback永远不会停止?** 一头雾水的我决定先试试. 结果悲剧, 程序每次开始callback后, 就如同死机一般. 更改要读的数据大小无用. google `read_samples_async + rtlsdr` 就只有一页结果. 

最后我终于想到了这玩意要看原c语言版本的说明, 这只是一个套在dll库文件上的python接口. 于是我找来[librtlsdr的c代码](https://github.com/steve-m/librtlsdr), 看了一下[rtlsdr.h头文件](https://github.com/steve-m/librtlsdr/blob/master/include/rtl-sdr.h).

```c
/*!
 * Read samples from the device asynchronously. This function will block until
 * it is being canceled using rtlsdr_cancel_async()
 *
 * NOTE: This function is deprecated and is subject for removal.
 *
 * \param dev the device handle given by rtlsdr_open()
 * \param cb callback function to return received samples
 * \param ctx user specific context to pass via the callback function
 * \return 0 on success
 */
RTLSDR_API int rtlsdr_wait_async(rtlsdr_dev_t *dev, rtlsdr_read_async_cb_t cb, void *ctx);
```

这函数竟然会block! 并且会直到被cancel才返回! 好吧我火星了. 然后我大概看了一下rtl_test.c, 它的处理都是放在callback里面的, 当按键后, 会cancel callback... 好吧我搞个线程什么的来执行它.

最终, 读取数据OK了, 但我遇到了另一个问题, 数据是复数形式的, 也就是包含I/Q两个信号, 这个数据用来做FM解调是容易, 但做完FFT结果是啥? 怎么据说还有个负频率? 研究了书中的描述, 看了网上的说明, 不懂. 于是我打算自己实验一下.

```python
data=q.get()                                            #从queue中取出数据
while not q.empty():                                    #清掉queue中的内容
q.get()
rt_data = np.real(data)                                 #取实部显示在实时显示里
data = data * window                                    #在算FFT前先加窗
fft_temp_data=fftpack.fft(data,overwrite_x=True)
fft_data=np.abs(fft_temp_data)[0:fft_temp_data.size]    #计算幅度
```

数据处理过程如上, 然后我把接收频率(center frequency)调整到先锋89.8附近, 以它为基准, 看看调整接收频率先锋89.8会往哪个方向移动.

![COMPLEX INPUT FFT 分析]({filename}../images/在python下实时显示rtlsdr波形与频谱/2.png)

首先在设定为90MHz时, 先锋位于右半边, 也就是传说中的负频率部分, 如果是实输入信号, 则这部分与左半边是重复的. 当增加接收频率时, 先锋向左移动. OK, 那么首先89.8MHz离我们设定的90MHz的距离是-0.2MHz, 当增加到90.1MHz时,距离为-0.3MHz, 那么也就是说这里就是传说中的负频率部分, 这部分的最右边是设定的接收频率, 最左边是接收频率减去采样率的一半, 也就是89.5MHz(90MHz).在最后一张图中,当设定接收频率小于89.8MHz时, 先锋就跑到正频率的部分里. 

![负频率部分说明]({filename}../images/在python下实时显示rtlsdr波形与频谱/3.png)

应当注意的是, 这里我们设定的接收频率是更改的接收电路的本振频率以及一些滤波器的参数, 与采样部分没有什么关系, 采样部分始终都是以8-bit 1MSPS的速度进行采样.

numpy有一个fftshift的函数可以转换上面所说的这种奇怪的排列方式, 将采样的频率(零频率)放在显示的中间.

```python
fft_temp_data=fftpack.fftshift(fftpack.fft(data,overwrite_x=True))
```

在加上这个函数后, 终于我得到的FFT图与demo_waterfall.py是一致的了.

