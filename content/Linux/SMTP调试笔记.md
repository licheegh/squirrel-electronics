Title: SMTP调试笔记
Date: 2018-01-15 12:00
Modified: 2018-01-16 12:00
Category: Linux
Summary: 公司邮箱是企鹅的企业邮，在用`git send-mail`时，死活连不上服务器，报认证错误。
但我的邮件客户端都不报错呀？于是我就踏上了debug SMTP的旅程。

我直接配置git send-mail后报错，而打开debug也没什么用，这是怎么回事？

```
Unable to initialize SMTP properly. Check config and use --smtp-debug. VALUES: server=smtp.exmail.qq.com encryption=tls hello=localhost.localdomain port=465 at /usr/lib/git-core/git-send-email line 1383.
```

首先我找到了[mxtoolbox](https://mxtoolbox.com/SuperTool.aspx?action=smtp%3asmtp.exmail.qq.com&run=toolpage#)这个工具，可以检测smtp服务器支持的认证方式。

![mxtoolbox screen shot][1]

然后我根据下面文章得知smtp可以telnet

* [how-to-check-an-smtp-connection-with-a-manual-telnet-session](https://www.port25.com/how-to-check-an-smtp-connection-with-a-manual-telnet-session-2/)
* [can-the-telnet-or-netcat-clients-communicate-over-ssl](https://superuser.com/questions/346958/can-the-telnet-or-netcat-clients-communicate-over-ssl)

而企鹅的服务器似乎只支持ssl登陆，于是用以下指令测试：

```bash
openssl s_client -crlf -connect smtp.exmail.qq.com:465
openssl s_client -starttls smtp -crlf -connect smtp.exmail.qq.com:587
```

[这篇很详细的介绍了怎样debug](https://easyengine.io/tutorials/mail/server/testing/smtp/)
,这篇也写的很详细：[12. SMTP Authentication for Mail clients](http://postfix.state-of-mind.de/patrick.koetter/smtpauth/smtp_auth_mailclients.html)，详细阅读12.3.2. Broken clients这里。

用下面的指令生成加密的账户与密码。

```bash
echo -ne '\0admin@example.com\0password' | base64
```

然后用这个来login服务器。

```
EHLO localhost.localdomain
AUTH PLAIN #base64编码#
```


```
250-smtp.qq.com
250-PIPELINING
250-SIZE 73400320
250-AUTH LOGIN PLAIN
250-AUTH=LOGIN
250-MAILCOMPRESS
250 8BITMIME
```

然后我忽然发现之前的git sendmail 开关设的并不对，正确的设置为 `--smtp-debug=1`。

```bash
git send-email 0000-cover-letter.patch --smtp-debug=1 --to example@xxx.com
465 ssl
Net::SMTP::SSL>>> Net::SMTP::SSL(1.03)
Net::SMTP::SSL>>>   IO::Socket::SSL(2.024)
Net::SMTP::SSL>>>     IO::Socket::IP(0.37)
Net::SMTP::SSL>>>       IO::Socket(1.38)
Net::SMTP::SSL>>>         IO::Handle(1.35)
Net::SMTP::SSL>>>           Exporter(5.72)
Net::SMTP::SSL>>>   Net::Cmd(3.05)
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 220 smtp.qq.com Esmtp QQ Mail Server
Net::SMTP::SSL=GLOB(0x1a8d4e0)>>> EHLO localhost.localdomain
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-smtp.qq.com
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-PIPELINING
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-SIZE 73400320
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-AUTH LOGIN PLAIN
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-AUTH=LOGIN
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250-MAILCOMPRESS
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 250 8BITMIME
Net::SMTP::SSL=GLOB(0x1a8d4e0)>>> AUTH LOGIN
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 334 。。。。。。。。。。
Net::SMTP::SSL=GLOB(0x1a8d4e0)>>> 。。。。。。。。。。。。。
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 334 。。。。。。。。
Net::SMTP::SSL=GLOB(0x1a8d4e0)>>> 。。。。。。。。
Net::SMTP::SSL=GLOB(0x1a8d4e0)<<< 535 Error: authentication failed, system busy
Error: authentication failed, system busy
```

终于有了登陆的debug信息。这时可以看到登陆过程的信息打印。这时我注意到base64那里的信息并不对。

然后找到了相当高级的debug工具[swaks](http://www.jetmore.org/john/code/swaks/latest/doc/ref.txt)。

```bash
./swaks -t llu@phytec.cn --from example@xxx.com --a LOGIN,PLAIN -tls --auth-user example@xxx.com --auth-password 'password' -s smtp.exmail.qq.com
```

这时密码错误的问题得到了确认，我发的密码转为base64后确实是错了，研究后发现要在git的配置中的密码上加单引号，包括其他一些直接输入密码的地方都要加，除非密码比较简单。


[1]: {filename}../images/smtptiao-shi-bi-ji/1.jpg