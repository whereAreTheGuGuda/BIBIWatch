# coding = utf-8
import requests, json
import re
import time


header = {
    "authority": "bscscan.com",
    "accept": "text/html",
    "cookie": "ASP.NET_SessionId=ew0b5s4dlnh4ddobziq4fi2h; __cflb=0H28vyb6xVveKGjdV3CFc257Dfrj7qvxNni7WE44pBW; _ga=GA1.1.113918749.1684322830; b-user-id=64932169-58a1-505e-c328-1d4ec3188f06; __cf_bm=cJIge3qkcAqUg4Uere8cNaYNA1PI2qbjdPS1C4QjvXo-1684325953-0-AcASseqQTZGI89Iy721o1N+M+f+ufOcFmbz4BZVFZ1G/3x5+R2Vy1u9N/GJCwtEePqDO4HHyVQ2u9BvcycWWM+tdvQti0RX8MfYcy9kSW4cm; _ga_PQY6J2Q8EP=GS1.1.1684325953.2.1.1684326516.0.0.0",
    "sec-ch-ua": 'Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}


class WatchBIBI:
    @classmethod
    def checkError(self, html: str):
        return len(html.split("We encountered an unexpected error")) > 1

    @classmethod
    def subString(self, rule, template):
        slotList = re.findall(rule, template)
        return slotList

    @classmethod
    # 获取目标地址的在bibi上的交易记录
    def checkBSN_BEP_20Transfer(self, wallet):
        try:
            time.sleep(1)
            bibi = "0xFE8bF5B8F5e4eb5f9BC2be16303f7dAB8CF56aA8"
            token = "JUZRZX8SCXAWI4M1QS9EPQR4NVNM2SA8DZ"
            url = (
                "https://api.bscscan.com/api?module=account&action=tokentx&contractaddress="
                + bibi
                + "&address="
                + wallet
                + "&page=1&offset=5&startblock=0&endblock=999999999&sort=asc&apikey="
                + token
            )
            resp = requests.get(url=url)
            j = json.loads(resp.content)
            presult = j["result"]
            tramsfer = presult[0]
            date_now = int(time.time())
            timeStamp = tramsfer["timeStamp"]
            datetime_stamp = date_now - int(timeStamp)
            m_end, s_end = divmod(datetime_stamp, 60)
            h_end, m_end = divmod(m_end, 60)
            print("地址上次交易时间在 " + "%02d小时:%02d分:%02d前" % (h_end, m_end, s_end))
            if datetime_stamp < 60 * 20:
                # 报警
                address_url = (
                    "https://bscscan.com/token/"
                    + wallet
                    + "?a=0xbe77ecd16216bff4ed60b78c3a2549ab18e82463#tokenInfo"
                )
                WatchBIBI.posttelegram(
                    "警告！！！ BIBI账户地址："
                    + wallet
                    + " 在 %02d小时:%02d分:%02d前发生了交易行为, \n 请访问 "
                    + address_url
                    + " 关注"
                )
        except:
            print("崩溃了！！！ 重新请求！！！" + wallet)
            WatchBIBI.checkBSN_BEP_20Transfer(wallet)

    @classmethod
    def watchBIBI(self):
        resp = requests.get(
            url="https://bscscan.com/token/generic-tokenholders2?a=0xfe8bf5b8f5e4eb5f9bc2be16303f7dab8cf56aa8&sid=&m=normal&s=4206900000000000000000000000000000&p=1",
            headers=header,
        )
        print(resp.content)
        html = str(resp.content)
        if WatchBIBI.checkError(html):
            time.sleep(5 * 60)
            WatchBIBI.watchBIBI()
        if resp.status_code == 200:
            # 解析html
            holder_rule = r"</a></span></td><td>(.*?)</td><td>"  # 正则规则
            holders = WatchBIBI.subString(holder_rule, html)
            address_rule = (
                "0xfe8bf5b8f5e4eb5f9bc2be16303f7dab8cf56aa8(.*?)#tokenAnalytics"
            )
            address = WatchBIBI.subString(address_rule, html)
            add = []
            addnew = []
            for i in range(len(address)):
                wallet: str = address[i][3 : 34 + 2 + 9]
                addnew.append(wallet)
            print(addnew.pop(0))
            del addnew[0]
            address = list(set(addnew))
            for i in range(len(address)):
                wallet: str = address[i]
                value: str = holders[i]
                hold = "".join(value.split(","))
                a = float(hold)
                b = float(10000000000000)
                if (
                    not wallet == "0xbabfb8eac3d264e5e55a22f7bd83e73aa3227e9f"
                    and not wallet == "0x000000000000000000000000000000000000dead"
                    and not wallet == "0xf05bcb4e3f6a015c4d961c413f7b72efdbb31eab"
                ):
                    if a > b:
                        add.append(wallet)
            print("总数量" + str(len(holders)))
            print("符合的数量" + str(len(add)))
            for i in range(len(add)):
                wallet = add[i]
                WatchBIBI.checkBSN_BEP_20Transfer(wallet)
                time.sleep(5)
        time.sleep(10 * 60)
        WatchBIBI.watchBIBI()

    @classmethod
    def posttelegram(self, message):
        url = (
            "https://api.telegram.org/bot"
            + "6001181347:AAGZFS6NLGNdzdDMxHBEcxNn39VtHdPEeho"
            + "/sendMessage"
        )
        param = {"chat_id": "-982460337", "text": message}
        talk = requests.post(url=url, params=param)
        print(talk.status_code)
        print(talk.content)


if __name__ == "__main__":
    WatchBIBI.watchBIBI()
    # WatchBIBI.checkBSN_BEP_20Transfer("0x8f00a4ed0a2c8e308a1d516c436c90bcaf7f1cd2")
    # WatchBIBI.posttelegram('PYTHON SEND TEST')

    # curl -X POST “https://api.telegram.org/bot<包括尖括号替换成机器人的token>/sendMessage" -d "chat_id=<目标的id，一串数字，群id比个人id的前边多了-号>&text=消息消息消息消息消息"
