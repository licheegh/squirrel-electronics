Title: Windows10"出现了一个意外情况"的修复
Date: 2019-12-5 12:18
Modified: 2019-12-5 12:18
Category: Electronics
Summary: "An unexpected condition occurred. Not all of your requested changes in settings could be made" "出现一个意外的情况。不能完成所有你在设置中所要求的更改" 当出现这个提示的时候，我的内心是崩溃的，这tm什么问题？

---

同事的电脑上不了网，经过查找，发现不知道从哪儿获取了个ipv6的地址，同时还有不知道从哪儿获取的ipv6网关/DNS服务器一应俱全，经过ipv6 ping百度都可以ping通，但上不了网。本人作为一个ipv6白痴，当然第一步是关掉ipv6协议，但win10竟然告诉我：

"An unexpected condition occurred. Not all of your requested changes in settings could be made"

"出现一个意外的情况。不能完成所有你在设置中所要求的更改" 

这tm什么问题？

搜索半天，网上说[用命令行设置IP地址](https://blog.csdn.net/qq_36769100/article/details/77962001)？？那怎么关ipv6？我怎么感觉这路子不太对呀。我又尝试了以下：

* 卸载360（这当然是第一个干的，虽然事实证明不是360的锅）
* 卸载vmware和virtualbox，[网上有人说是这个引起的](https://superuser.com/questions/1076572/cant-change-tcp-ipv4-settings-on-windows-10)
* 卸载openvpn，那和虚拟网卡有关就也干掉试试咯

试了以上一律无效，找到说可以试试卸载网卡驱动，卸载后报错："Windows 仍在设置此设备的类配置。（代码 56）"，网上[有人说要重装系统](https://answers.microsoft.com/zh-hans/windows/forum/windows_10-hardware/windows%E4%BB%8D%E5%9C%A8%E8%AE%BE%E7%BD%AE/41c505c8-514f-4c9e-9dd6-66cb6458a977?page=2)，哥修这么多年电脑，最烦装系统,但大多数用CCleaner清理一下注册表就搞定了。

于是下载CCleaner，清理，网卡好了，网络也可以配置了，去掉ipv6，百度你好~

CCleaner真牛逼（破音）！







