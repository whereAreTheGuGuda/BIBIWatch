#coding = utf-8
from requests_html import HTMLSession
from requests_html import HTML
import requests,json
import re
import time
import webbrowser
session = HTMLSession()

header = {
        'authority' : 'bscscan.com',
        'accept': 'text/html',
        'cookie': 'ASP.NET_SessionId=ew0b5s4dlnh4ddobziq4fi2h; __cflb=0H28vyb6xVveKGjdV3CFc257Dfrj7qvxNni7WE44pBW; _ga=GA1.1.113918749.1684322830; b-user-id=64932169-58a1-505e-c328-1d4ec3188f06; __cf_bm=cJIge3qkcAqUg4Uere8cNaYNA1PI2qbjdPS1C4QjvXo-1684325953-0-AcASseqQTZGI89Iy721o1N+M+f+ufOcFmbz4BZVFZ1G/3x5+R2Vy1u9N/GJCwtEePqDO4HHyVQ2u9BvcycWWM+tdvQti0RX8MfYcy9kSW4cm; _ga_PQY6J2Q8EP=GS1.1.1684325953.2.1.1684326516.0.0.0',
        'sec-ch-ua': 'Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
class WatchBIBI:
    

    @classmethod
    def checkError(self,html:str):
        return len(html.split('We encountered an unexpected error')) > 0
    
    @classmethod
    def subString(self,rule,template):
        slotList = re.findall(rule, template)
        return slotList
    
    @classmethod
    def checkAddress(self,wallet):
        
        url = 'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=' + wallet +'&a=0xbe77ecd16216bff4ed60b78c3a2549ab18e82463&sid=9978ec849b82d740b6fd498f16e78833&p=1'
        # url = 'https://bscscan.com/token/' + wallet +'?a=0xbe77ecd16216bff4ed60b78c3a2549ab18e82463'
        r = requests.get(url= url,headers=header)
        print(r.content)
        html = HTML(html=r.content)
        html.render(wait=3)
        print(html.html) 

        return
        walletResp = requests.get(url=url,headers=header)
        print(walletResp.status_code)
        print(walletResp.content)
        wallet_html = str(walletResp.content)
        if (not walletResp.status_code == 200) or WatchBIBI.checkError(wallet_html) :
            # 请求过于频繁 需要等待
            time.sleep(60 * 5)
            WatchBIBI.checkAddress(wallet)
        times = WatchBIBI.subString(' title=(.*?)>',wallet_html)
        print(times)
            # array = html.split('</a></span></td><td>')
            # for i in range(len(array)):
                # value1 = array[i].split('</td><td>')[0]
                # print('anwster     ' + value1 + '   ' + str(i))

    @classmethod
    def watchBIBI(self):
        resp = requests.get(url='https://bscscan.com/token/generic-tokenholders2?a=0xfe8bf5b8f5e4eb5f9bc2be16303f7dab8cf56aa8&sid=&m=normal&s=4206900000000000000000000000000000&p=1',headers=header)
        print(resp.content)
        html = str(resp.content)
        if WatchBIBI.checkError(html):
            time.sleep(5 * 60)
            WatchBIBI.watchBIBI()
        if (resp.status_code == 200):
            # 解析html
            holder_rule = r'</a></span></td><td>(.*?)</td><td>' # 正则规则
            holders = WatchBIBI.subString(holder_rule,html)
            address_rule = '/token/(.*?)\''
            address = WatchBIBI.subString(address_rule,html)
            add = []
            for i in range(len(holders)):
                value :str = holders[i]
                # hold = float(''.join(value.split(',')))
                # if hold > 10000000000000:
                key : str = address[i]
                if key.startswith('0x'):
                    wallet = key.split('?a=')[1].split('#tokenAnalytics')[0]
                    if not wallet.endswith('\\'):
                        if not wallet == '0xbabfb8eac3d264e5e55a22f7bd83e73aa3227e9f' and not wallet == '0x000000000000000000000000000000000000dead' and not wallet == '0xf05bcb4e3f6a015c4d961c413f7b72efdbb31eab':
                            add.append(wallet)

            print(add)
            # for i in range(len(add)):
            for i in range(1):
                wallet = add[i]
                WatchBIBI.checkAddress(wallet)

    @classmethod
    def posttelegram(self,message):
        url = 'https://api.telegram.org/bot' + '6001181347:AAGZFS6NLGNdzdDMxHBEcxNn39VtHdPEeho' + '/sendMessage'
        param = {
            'chat_id' : '-982460337',
            'text' : message
        }
        talk = requests.post(url=url,params=param)
        print(talk.status_code)
        print(talk.content)
if __name__ == '__main__':
    WatchBIBI.checkAddress('0x8f00a4ed0a2c8e308a1d516c436c90bcaf7f1cd2')
    # WatchBIBI.posttelegram('PYTHON SEND TEST')

    # curl -X POST “https://api.telegram.org/bot<包括尖括号替换成机器人的token>/sendMessage" -d "chat_id=<目标的id，一串数字，群id比个人id的前边多了-号>&text=消息消息消息消息消息"
