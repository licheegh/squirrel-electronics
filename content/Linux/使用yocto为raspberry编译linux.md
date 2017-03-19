Title: 使用yocto为raspberry编译linux
Date: 2017-03-12 22:40
Modified: 2017-03-19 23:00
Category: Linux
Summary: 由于工作的关系需要搞一下yocto，看过介绍觉得这很适合嵌入式应用，个人感觉和openwrt很像。手里有个树莓派，当然最简单的就是先为它编译一个linux系统玩玩。

电脑是一台debian，已刷最新，树莓派为古老的model B。

[yocto](https://www.yoctoproject.org/downloads)网站最新的版本是morty 2.2.1，当然我们要用git clone的方式来获取最新的，但直接clone发现速度只有几kb。我记得我的git是有走socks5的呀～经研究发现git://这种开头的和https://开头的并不一样，通过<https://gist.github.com/laispace/666dd7b27e9116faece6>

```
git config --global https.proxy http://127.0.0.1:1080
git config --global https.proxy https://127.0.0.1:1080
```

这样只能实现对http/https的代理，于是我顺利的在<http://git.yoctoproject.org/cgit/cgit.cgi/poky/>页面的最下面找到了https的链接<https://git.yoctoproject.org/git/poky>。这样虽然也只有80多kb，但已经快了很多。clone完成后文件夹有185MB大小。

根据教程这里应该要安装一堆东西，我的系统是debian

```
apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib \
     build-essential chrpath socat cpio python python3 pip3 pexpect libsdl1.2-dev xterm
```

但我这里提示

```
E: Unable to locate package pip3
E: Unable to locate package pexpect
```

先不管它，

```
source oe-init-build-env
```

此时会建立一个build目录，并且把一些配置文件放在conf这个文件夹里面，在执行这个script的时候会提示说没有'conf/local.conf'和'conf/bblayers.conf'文件，因此新建了新的。

```
You had no conf/local.conf file. This configuration file has therefore been
created for you with some default values. You may wish to edit it to, for
example, select a different MACHINE (target hardware). See conf/local.conf
for more information as common configuration options are commented.

You had no conf/bblayers.conf file. This configuration file has therefore been
created for you with some default values. To add additional metadata layers
into your configuration please add entries to conf/bblayers.conf.
```

这时准备raspberry的bsp，<http://git.yoctoproject.org/cgit/cgit.cgi/meta-raspberrypi/>。这个库很小。

在这个库的about栏目里有介绍使用方法。

修改local.conf

```
MACHINE ??= "raspberrypi"
```

修改bblayers.conf，增加刚刚clone的树梅派的bsp的路径。

```
BBLAYERS ?= " \
  /home/lichee/work/yocto/poky/meta \
  /home/lichee/work/yocto/poky/meta-poky \
  /home/lichee/work/yocto/poky/meta-yocto-bsp \
  /home/lichee/work/yocto/meta-raspberrypi \
  "
```

OK，这样就可以编译出默认的配置了。

```
bitbake rpi-hwup-image
```

结果报错:

```
You system needs to support the en_US.UTF-8 locale.
```

<https://wiki.debian.org/Locale>根据这里，我这里原来设的是'en_HK.UTF-8'，于是按照流程处理一遍为en_US utf8，但还是不对，用locale看依然是hk。最后终于找到<http://unix.stackexchange.com/questions/224286/how-to-set-english-as-a-default-language-in-debian>

```
export LANGUAGE=en_US
export LANG=en_US.UTF-8
update-locale LANG=en_US.UTF-8 LANGUAGE=en_US
```

又报错~

```
WARNING: Host distribution "Debian-9.0" has not been validated with this version of the build system; you may possibly experience unexpected failures. It is recommended that you use a tested distribution.
ERROR:  OE-core's config sanity checker detected a potential misconfiguration.
    Either fix the cause of this error or at your own risk disable the checker (see sanity.conf).
    Following is the list of potential problems / advisories:

    Please install the following missing utilities: diffstat,chrpath
```

安装~

```

WARNING: Host distribution "Debian-9.0" has not been validated with this version of the build system; you may possibly experience unexpected failures. It is recommended that you use a tested distribution.
ERROR: /home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi_dev.bb: Error executing a python function in <code>:  | ETA:  --:--:--

The stack trace of python calls that resulted in this exception/failure was:
File: '<code>', lineno: 18, function: <module>
     0014:__anon_18__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_yocto_inc(d)
     0015:__anon_364__home_lichee_work_yocto_poky_meta_classes_kernel_yocto_bbclass(d)
     0016:__anon_6__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_dtb_inc(d)
     0017:__anon_148__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_rpi_inc(d)
 *** 0018:__anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc(d)
File: '/home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi.inc', lineno: 37, function: __anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc
     0033:# Set programmatically some variables during recipe parsing
     0034:# See http://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html#anonymous-python-functions
     0035:python __anonymous () {
     0036:    kerneltype = d.getVar('KERNEL_IMAGETYPE')
 *** 0037:    kerneldt = get_dts(d, d.getVar('LINUX_VERSION'))
     0038:    d.setVar("KERNEL_DEVICETREE", kerneldt)
     0039:}
     0040:
     0041:do_kernel_configme_prepend() {
Exception: TypeError: getVar() missing 1 required positional argument: 'expand'

ERROR: Failed to parse recipe: /home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi_dev.bb
ERROR: /home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi_4.9.bb: Error executing a python function in <code>:

The stack trace of python calls that resulted in this exception/failure was:
File: '<code>', lineno: 18, function: <module>
     0014:__anon_18__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_yocto_inc(d)
     0015:__anon_364__home_lichee_work_yocto_poky_meta_classes_kernel_yocto_bbclass(d)
     0016:__anon_6__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_dtb_inc(d)
     0017:__anon_148__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_rpi_inc(d)
 *** 0018:__anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc(d)
File: '/home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi.inc', lineno: 37, function: __anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc
     0033:# Set programmatically some variables during recipe parsing
     0034:# See http://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html#anonymous-python-functions
     0035:python __anonymous () {
     0036:    kerneltype = d.getVar('KERNEL_IMAGETYPE')
 *** 0037:    kerneldt = get_dts(d, d.getVar('LINUX_VERSION'))
     0038:    d.setVar("KERNEL_DEVICETREE", kerneldt)
     0039:}
     0040:
     0041:do_kernel_configme_prepend() {
Exception: TypeError: getVar() missing 1 required positional argument: 'expand'

ERROR: /home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi_4.4.bb: Error executing a python function in <code>:

The stack trace of python calls that resulted in this exception/failure was:
File: '<code>', lineno: 18, function: <module>
     0014:__anon_18__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_yocto_inc(d)
     0015:__anon_364__home_lichee_work_yocto_poky_meta_classes_kernel_yocto_bbclass(d)
     0016:__anon_6__home_lichee_work_yocto_poky_meta_recipes_kernel_linux_linux_dtb_inc(d)
     0017:__anon_148__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_rpi_inc(d)
 *** 0018:__anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc(d)
File: '/home/lichee/work/yocto/meta-raspberrypi/recipes-kernel/linux/linux-raspberrypi.inc', lineno: 37, function: __anon_39__home_lichee_work_yocto_meta_raspberrypi_recipes_kernel_linux_linux_raspberrypi_inc
     0033:# Set programmatically some variables during recipe parsing
     0034:# See http://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html#anonymous-python-functions
     0035:python __anonymous () {
     0036:    kerneltype = d.getVar('KERNEL_IMAGETYPE')
 *** 0037:    kerneldt = get_dts(d, d.getVar('LINUX_VERSION'))
     0038:    d.setVar("KERNEL_DEVICETREE", kerneldt)
     0039:}
     0040:
     0041:do_kernel_configme_prepend() {
Exception: TypeError: getVar() missing 1 required positional argument: 'expand'

```

报错~然后发现我clone的yocto是morty版本的，但树梅派的bsp是master最新的，于是切回morty的版本。终于开始编译。


```
WARNING: Host distribution "Debian-9.0" has not been validated with this version of the build system; you may possibly experience unexpected failures. It is recommended that you use a tested distribution.
Parsing recipes: 100% |#######################################################################################################################| Time: 0:02:24
Parsing of 884 .bb files complete (0 cached, 884 parsed). 1338 targets, 73 skipped, 0 masked, 0 errors.
NOTE: Resolving any missing task queue dependencies


Build Configuration:
BB_VERSION        = "1.32.0"
BUILD_SYS         = "i686-linux"
NATIVELSBSTRING   = "Debian-9.0"
TARGET_SYS        = "arm-poky-linux-gnueabi"
MACHINE           = "raspberrypi"
DISTRO            = "poky"
DISTRO_VERSION    = "2.2.1"
TUNE_FEATURES     = "arm armv6  vfp arm1176jzfs callconvention-hard"
TARGET_FPU        = "hard"
meta              
meta-poky         
meta-yocto-bsp    = "morty:6a1f33cc40bfac33cf030fe41e1a8efd1e5fad6f"
meta-raspberrypi  = "HEAD:cce6292e41493158c26f5b1b7fded97faacf10d7"
```

其中下载了几个比较大的包，binutils，glibc，firmware，gcc，linux。都是自己下载然后放在download文件夹里面，下载方法是通过task manager打开show full command line，然后就可以看到url，用下载工具下载下来就行。然后把bitbake ctrl-c掉，删掉download中的两个文件，重起即可。

最终编译出来的文件位于tmp/deploy/images/raspberrypi2/，然后用dd写入sd卡，注意这个命令需要root，执行前要确认好/dev中sd卡的路径。可以通过插入sd卡后查看dmesg来获得。

```
dd if=tmp/deploy/images/raspberrypi2/rpi-basic-image-raspberrypi2.rpi-sdimg of=/dev/mmcblk0 bs=16M
```

接下来找个usb-ttl的串口转换，<http://elinux.org/RPi_Serial_Connection>这里有接线方法。

登陆用户名为root,密码空。


```
[    0.000000] Booting Linux on physical CPU 0x0
[    0.000000] Initializing cgroup subsys cpuset
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
[    0.000000] Linux version 4.4.48 (lichee@lichee) (gcc version 6.2.0 (GCC) ) #1 Wed Mar 15 04:20:59 HKT 2017
[    0.000000] CPU: ARMv6-compatible processor [410fb767] revision 7 (ARMv7), cr=00c5387d
[    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT nonaliasing instruction cache
[    0.000000] Machine model: Raspberry Pi Model B Rev 2
[    0.000000] cma: Reserved 8 MiB at 0x1b400000
[    0.000000] Memory policy: Data cache writeback
[    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 113680
[    0.000000] Kernel command line: dma.dmachans=0x7f35 bcm2708_fb.fbwidth=656 bcm2708_fb.fbheight=416 bcm2708.boardrev=0xd bcm2708.serial=0x80e4913 smsc95xt
[    0.000000] PID hash table entries: 2048 (order: 1, 8192 bytes)
[    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)
[    0.000000] Inode-cache hash table entries: 32768 (order: 5, 131072 bytes)
[    0.000000] Memory: 436436K/458752K available (6090K kernel code, 437K rwdata, 1904K rodata, 372K init, 726K bss, 14124K reserved, 8192K cma-reserved)
[    0.000000] Virtual kernel memory layout:
[    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
[    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
[    0.000000]     vmalloc : 0xdc800000 - 0xff800000   ( 560 MB)
[    0.000000]     lowmem  : 0xc0000000 - 0xdc000000   ( 448 MB)
[    0.000000]     modules : 0xbf000000 - 0xc0000000   (  16 MB)
[    0.000000]       .text : 0xc0008000 - 0xc07d6a00   (7995 kB)
[    0.000000]       .init : 0xc07d7000 - 0xc0834000   ( 372 kB)
[    0.000000]       .data : 0xc0834000 - 0xc08a1568   ( 438 kB)
[    0.000000]        .bss : 0xc08a1568 - 0xc09570b0   ( 727 kB)
[    0.000000] SLUB: HWalign=32, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.000000] NR_IRQS:16 nr_irqs:16 16
[    0.000026] sched_clock: 32 bits at 1000kHz, resolution 1000ns, wraps every 2147483647500ns
[    0.000067] clocksource: timer: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275 ns
[    0.000164] bcm2835: system timer (irq = 27)
[    0.000463] Console: colour dummy device 80x30
[    0.000500] Calibrating delay loop... 697.95 BogoMIPS (lpj=3489792)
[    0.060304] pid_max: default: 32768 minimum: 301
[    0.060667] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.060694] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.061685] Disabling cpuset control group subsystem
[    0.061734] Initializing cgroup subsys io
[    0.061769] Initializing cgroup subsys memory
[    0.061827] Initializing cgroup subsys devices
[    0.061857] Initializing cgroup subsys freezer
[    0.061885] Initializing cgroup subsys net_cls
[    0.061967] CPU: Testing write buffer coherency: ok
[    0.062041] ftrace: allocating 20550 entries in 61 pages
[    0.174475] Setting up static identity map for 0x81c0 - 0x81f8
[    0.176313] devtmpfs: initialized
[    0.184898] VFP support v0.3: implementor 41 architecture 1 part 20 variant b rev 5
[    0.185446] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
[    0.187193] pinctrl core: initialized pinctrl subsystem
[    0.188102] NET: Registered protocol family 16
[    0.193746] DMA: preallocated 4096 KiB pool for atomic coherent allocations
[    0.201740] hw-breakpoint: found 6 breakpoint and 1 watchpoint registers.
[    0.201769] hw-breakpoint: maximum watchpoint size is 4 bytes.
[    0.201946] Serial: AMBA PL011 UART driver
[    0.202354] 20201000.uart: ttyAMA0 at MMIO 0x20201000 (irq = 81, base_baud = 0) is a PL011 rev2
[    0.555744] console [ttyAMA0] enabled
[    0.560187] bcm2835-mbox 2000b880.mailbox: mailbox enabled
[    0.609198] bcm2835-dma 20007000.dma: DMA legacy API manager at f2007000, dmachans=0x1
[    0.618150] SCSI subsystem initialized
[    0.622242] usbcore: registered new interface driver usbfs
[    0.627927] usbcore: registered new interface driver hub
[    0.633409] usbcore: registered new device driver usb
[    0.648616] raspberrypi-firmware soc:firmware: Attached to firmware from 2016-11-25 16:03
[    0.684358] clocksource: Switched to clocksource timer
[    0.741629] FS-Cache: Loaded
[    0.745027] CacheFiles: Loaded
[    0.767230] NET: Registered protocol family 2
[    0.772922] TCP established hash table entries: 4096 (order: 2, 16384 bytes)
[    0.780157] TCP bind hash table entries: 4096 (order: 2, 16384 bytes)
[    0.786715] TCP: Hash tables configured (established 4096 bind 4096)
[    0.793286] UDP hash table entries: 256 (order: 0, 4096 bytes)
[    0.799207] UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
[    0.805910] NET: Registered protocol family 1
[    0.810834] RPC: Registered named UNIX socket transport module.
[    0.816849] RPC: Registered udp transport module.
[    0.821562] RPC: Registered tcp transport module.
[    0.826306] RPC: Registered tcp NFSv4.1 backchannel transport module.
[    0.833903] hw perfevents: enabled with armv6_1176 PMU driver, 3 counters available
[    0.843071] futex hash table entries: 256 (order: -1, 3072 bytes)
[    0.865878] VFS: Disk quotas dquot_6.6.0
[    0.870214] VFS: Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
[    0.880033] FS-Cache: Netfs 'nfs' registered for caching
[    0.886762] NFS: Registering the id_resolver key type
[    0.891914] Key type id_resolver registered
[    0.896228] Key type id_legacy registered
[    0.904587] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 252)
[    0.912426] io scheduler noop registered
[    0.916491] io scheduler deadline registered
[    0.921185] io scheduler cfq registered (default)
[    0.928635] BCM2708FB: allocated DMA memory 5b800000
[    0.933669] BCM2708FB: allocated DMA channel 0 @ f2007000
[    0.946755] Console: switching to colour frame buffer device 82x26
[    2.053473] bcm2835-rng 20104000.rng: hwrng registered
[    2.058928] vc-cma: Videocore CMA driver
[    2.062865] vc-cma: vc_cma_base      = 0x00000000
[    2.067631] vc-cma: vc_cma_size      = 0x00000000 (0 MiB)
[    2.073037] vc-cma: vc_cma_initial   = 0x00000000 (0 MiB)
[    2.078892] vc-mem: phys_addr:0x00000000 mem_base=0x1ec00000 mem_size:0x20000000(512 MiB)
[    2.112031] brd: module loaded
[    2.127237] loop: module loaded
[    2.131560] vchiq: vchiq_init_state: slot_zero = 0xdb880000, is_master = 0
[    2.140918] Loading iSCSI transport class v2.0-870.
[    2.147337] usbcore: registered new interface driver smsc95xx
[    2.153358] dwc_otg: version 3.00a 10-AUG-2012 (platform bus)
[    2.359680] Core Release: 2.80a
[    2.362847] Setting default values for core params
[    2.367731] Finished setting default values for core params
[    2.573651] Using Buffer DMA mode
[    2.577020] Periodic Transfer Interrupt Enhancement - disabled
[    2.582860] Multiprocessor Interrupt Enhancement - disabled
[    2.588472] OTG VER PARAM: 0, OTG VER FLAG: 0
[    2.592897] Dedicated Tx FIFOs mode
[    2.597005] WARN::dwc_otg_hcd_init:1047: FIQ DMA bounce buffers: virt = 0xdb814000 dma = 0x5b814000 len=9024
[    2.606929] FIQ FSM acceleration enabled for :
[    2.606929] Non-periodic Split Transactions
[    2.606929] Periodic Split Transactions
[    2.606929] High-Speed Isochronous Endpoints
[    2.606929] Interrupt/Control Split Transaction hack enabled
[    2.629436] WARN::hcd_init_fiq:413: FIQ on core 0 at 0xc041040c
[    2.635370] WARN::hcd_init_fiq:414: FIQ ASM at 0xc04106e8 length 36
[    2.641658] WARN::hcd_init_fiq:439: MPHI regs_base at 0xdc898000
[    2.647797] dwc_otg 20980000.usb: DWC OTG Controller
[    2.652830] dwc_otg 20980000.usb: new USB bus registered, assigned bus number 1
[    2.660259] dwc_otg 20980000.usb: irq 56, io mem 0x00000000
[    2.665930] Init: Port Power? op_state=1
[    2.669859] Init: Power Port (0)
[    2.673490] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002
[    2.680353] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.687629] usb usb1: Product: DWC OTG Controller
[    2.692345] usb usb1: Manufacturer: Linux 4.4.48 dwc_otg_hcd
[    2.698047] usb usb1: SerialNumber: 20980000.usb
[    2.703888] hub 1-0:1.0: USB hub found
[    2.707806] hub 1-0:1.0: 1 port detected
[    2.713313] usbcore: registered new interface driver usb-storage
[    2.719945] mousedev: PS/2 mouse device common for all mice
[    2.726760] bcm2835-cpufreq: min=700000 max=700000
[    2.731964] sdhci: Secure Digital Host Controller Interface driver
[    2.738244] sdhci: Copyright(c) Pierre Ossman
[    2.743201] sdhost: log_buf @ db813000 (5b813000)
[    2.804623] mmc0: sdhost-bcm2835 loaded - DMA enabled (>1)
[    2.810666] sdhci-pltfm: SDHCI platform and OF driver helper
[    2.837293] ledtrig-cpu: registered to indicate activity on CPUs
[    2.843491] hidraw: raw HID events driver (C) Jiri Kosina
[    2.849310] usbcore: registered new interface driver usbhid
[    2.854953] usbhid: USB HID core driver
[    2.861165] Initializing XFRM netlink socket
[    2.869030] NET: Registered protocol family 17
[    2.873711] Key type dns_resolver registered
[    2.886621] registered taskstats version 1
[    2.891068] vc-sm: Videocore shared memory driver
[    2.896043] [vc_sm_connected_init]: start
[    2.901250] [vc_sm_connected_init]: end - returning 0
[    2.906642] Indeed it is in host mode hprt0 = 00021501
[    2.973624] of_cfs_init
[    2.977382] of_cfs_init: OK
[    2.981694] uart-pl011 20201000.uart: no DMA platform data
[    2.988068] Waiting for root device /dev/mmcblk0p2...
[    2.997992] mmc0: host does not support reading read-only switch, assuming write-enable
[    3.008739] mmc0: new high speed SD card at address 0002
[    3.015432] mmcblk0: mmc0:0002 00000 1.87 GiB
[    3.024433]  mmcblk0: p1 p2
[    3.098064] EXT4-fs (mmcblk0p2): INFO: recovery required on readonly filesystem
[    3.105516] EXT4-fs (mmcblk0p2): write access will be enabled during recovery
[    3.112737] usb 1-1: new high-speed USB device number 2 using dwc_otg
[    3.121039] Indeed it is in host mode hprt0 = 00001101
[    3.273350] EXT4-fs (mmcblk0p2): recovery complete
[    3.290068] EXT4-fs (mmcblk0p2): mounted filesystem with ordered data mode. Opts: (null)
[    3.298355] VFS: Mounted root (ext4 filesystem) readonly on device 179:2.
[    3.307761] devtmpfs: mounted
[    3.311985] Freeing unused kernel memory: 372K (c07d7000 - c0834000)
[    3.324936] usb 1-1: New USB device found, idVendor=0424, idProduct=9512
[    3.331773] usb 1-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    3.340463] hub 1-1:1.0: USB hub found
[    3.345491] hub 1-1:1.0: 3 ports detected
INIT: version 2.88 booting
[    3.624473] usb 1-1.1: new high-speed USB device number 3 using dwc_otg
[    3.745029] usb 1-1.1: New USB device found, idVendor=0424, idProduct=ec00
[    3.751936] usb 1-1.1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    3.776036] smsc95xx v1.0.4
[    3.862668] smsc95xx 1-1.1:1.0 eth0: register 'smsc95xx' at usb-20980000.usb-1.1, smsc95xx USB 2.0 Ethernet, b8:27:eb:0e:49:13
Starting udev
cmp: EOF on /etc/udev/cache.data
udev: Not using udev cache because of changes detected in the following files:
udev:     /proc/version /proc/cmdline /proc/devices
udev:     lib/udev/rules.d/* etc/udev/rules.d/*
udev: The udev cache will be regenerated. To identify the detected changes,
udev: compare the cached sysconf at   /etc/udev/cache.data
udev: against the current sysconf at  /dev/shm/udev.cache
[    4.245846] udevd[105]: starting version 3.2
[    4.315157] random: udevd: uninitialized urandom read (16 bytes read, 67 bits of entropy available)
[    4.324982] random: udevd: uninitialized urandom read (16 bytes read, 67 bits of entropy available)
[    4.334315] random: udevd: uninitialized urandom read (16 bytes read, 67 bits of entropy available)
[    4.458251] udevd[106]: starting eudev-3.2
[    4.946262] bcm2835-wdt 20100000.watchdog: Broadcom BCM2835 watchdog timer
[    4.964267] gpiomem-bcm2835 20200000.gpiomem: Initialised: Registers at 0x20200000
[    6.926859] EXT4-fs (mmcblk0p2): re-mounted. Opts: data=ordered
Populating dev cache
[    8.149316] random: dd: uninitialized urandom read (512 bytes read, 76 bits of entropy available)
Tue Mar 14 21:08:02 UTC 2017
INIT: Entering runlevel: 5
Configuring network interfaces... [    8.567800] smsc95xx 1-1.1:1.0 eth0: hardware isn't capable of remote wakeup
udhcpc (v1.24.1) started
Sending discover...
Sending discover...
Sending discover...
No lease, forking to background
done.
Starting syslogd/klogd: done

Poky (Yocto Project Reference Distro) 2.2.1 raspberrypi /dev/ttyAMA0

raspberrypi login: [   19.676010] random: nonblocking pool is initialized

Poky (Yocto Project Reference Distro) 2.2.1 raspberrypi /dev/ttyAMA0

raspberrypi login: raspberry
Password: 
Login incorrect
raspberrypi login: raspberrypi
Password: 
Login incorrect
raspberrypi login: rot
Password: 
Login incorrect

Poky (Yocto Project Reference Distro) 2.2.1 raspberrypi /dev/ttyAMA0

raspberrypi login: root
root@raspberrypi:~# 
```

Reference:

* [Building Raspberry Pi Systems with Yocto](http://www.jumpnowtek.com/rpi/Raspberry-Pi-Systems-with-Yocto.html)
* [Build a Raspberry Pi 2 Minimal Image with The Yocto Project](http://www.cnx-software.com/2015/02/27/yocto-project-raspberry-pi-2-board-minimal-image/)


