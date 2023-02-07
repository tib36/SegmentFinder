#!/usr/bin/env python
# -*- coding:utf-8 -*-
#---[ Author:nokali ]---

#本程序仅可用于合法测试，使用者需自行承担风险

import colorama
import requests
from requests.packages import urllib3
from bs4 import BeautifulSoup
import multiprocessing
from faker import Faker
import logging
import sys
import time

logging.captureWarnings(True)    #屏蔽多余警告信息

def scan(url):
    RandomUA=Faker()
    ua=RandomUA.user_agent()    #随机生成仿真UserAgent信息
    headers={'user-agent':ua}
    try:
        result=requests.get(url,headers=headers,timeout=1,verify=False)    #默认超时（timeout）为1，且关闭证书验证
        #print(url)    #调试代码
        soup=BeautifulSoup(result.text,'html.parser')
        console_output=str(soup.find_all('title'))    #调用bs4处理http返回数据，提取title信息
        console_output=console_output.replace("<title>","")
        console_output=console_output.replace("</title>","")
        console_output='Status:'+str(result.status_code)+' - Length:'+str(len(result.text))+' - Title:'+console_output

        if str(result.status_code):
            print(colorama.Back.BLACK+colorama.Fore.YELLOW+'[+] '+
                colorama.Fore.GREEN+url+' '+
                colorama.Fore.RED+console_output)
                #输出当前url的扫描结果
            with open('outfile.txt','a',encoding='utf-8') as outfile:
                outfile.write(url+'\n')
                outfile.close()
    except:
        pass


if __name__=='__main__':
    start_time=time.time()

    procs=50    #进程池大小

    ports=[80, 81, 443, 591, 2082, 2087, 2095, 2096,
        3000, 8000, 8001, 8008, 8080, 8083, 8443, 
        8834, 8888]    #指定扫描端口，默认为这些常见端口

    print(colorama.Back.BLACK+colorama.Fore.CYAN+'''
███████╗███████╗ ██████╗ ███╗   ███╗███████╗███╗   ██╗████████╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██╔════╝██╔════╝ ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
███████╗█████╗  ██║  ███╗██╔████╔██║█████╗  ██╔██╗ ██║   ██║   █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
╚════██║██╔══╝  ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
███████║███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                            
''')
    print("===== Author:NOKALI =====")
    print("")

    try:
        ip=sys.argv[1]
        mode=sys.argv[2]
    except:
        print('''
第一个参数为目标范围内的IP
第二个参数为扫描模式
扫描模式允许B段或C段
如果使用B段则需要指定扫描范围

Example:
python Scanner.py 192.168.10.100 C
如上    即扫描192.168.10.0-255的这一C段
python Scanner.py 192.168.233.233 B 10 20
如上    即扫描192.168.10-20.0-255的这一B段
在进行B段扫描时不建议指定大范围
扫描范围以5以下为最佳
例如B 1 5
即扫描192.168.1.0~192.168.5.255
扫描结果会自动追加写入文件
''')

    try:
        if mode=='B':    #扫描B段
            B_range_min=int(sys.argv[3])
            B_range_max=int(sys.argv[4])
            print('[*] 正在扫描 '+ip+' 范围为'+str(B_range_min)+'~'+str(B_range_max))
            target=ip.split('.')
            target=target[0]+'.'+target[1]+'.'
            pool = multiprocessing.Pool(processes = procs)    #进程池，限制并行进程数量
            for i in range(B_range_min,B_range_max+1):
                for c in range(255):
                    for port in range(len(ports)):
                        url='http://'+target+str(i)+'.'+str(c)+':'+str(ports[port])
                        pool.apply_async(scan, (url, ))

            pool.close()
            pool.join()
        elif mode=='C':    #扫描C段
            print('[*] 正在扫描 '+ip+'/24')
            target=ip.split('.')
            target=target[0]+'.'+target[1]+'.'+target[2]+'.'
            pool = multiprocessing.Pool(processes = procs)    #进程池，限制并行进程数量
            for i in range(255):    #扫描一个网段
                for port in range(len(ports)):
                    url='http://'+target+str(i)+':'+str(ports[port])
                    pool.apply_async(scan, (url, ))

            pool.close()
            pool.join()
        else:
            print('扫描模式有误')
    except:
        pass
    

    print(colorama.Fore.RESET,end='')
    print(colorama.Back.RESET,end='')
    print(colorama.Style.RESET_ALL,end='')
    #程序执行结束，还原终端颜色
    
    end_time=time.time()

    print('[*] 程序执行时间：'+str(int(end_time-start_time))+'秒')


