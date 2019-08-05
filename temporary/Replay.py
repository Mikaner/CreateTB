import json
import urllib.request
import random


class Replay:
    data = './replayData/'

    def __init__(self):
        pass

    def TBcat(self):
        with open(self.data + 'catReplay.txt', 'r', 1, encoding='utf-8') as message:
            self.cat = [line.strip() for line in message.readlines()]
        r = random.randrange(0, len(self.cat))
        return self.cat[r]

    def luck(self):
        with open(self.data + 'fortune.txt', 'r', 1, encoding='utf-8') as luckMessage:
            self.fortune = [line.strip() for line in luckMessage.readlines()]
        r = random.randrange(0, len(self.fortune))
        return self.fortune[r]

    def goodMorning(self):
        with open(self.data + 'morningReplay.txt', 'r', 1, encoding='utf-8') as morningMessage:
            self.morning = [line.strip()
                            for line in morningMessage.readlines()]
        r = random.randrange(0, len(self.morning))
        return self.morning[r]

    def goodNoon(self):
        with open(self.data + 'morningReplayInNoon.txt', 'r', 1, encoding='utf-8') as goodNoonMessage:
            self.mNoon = [line.strip() for line in goodNoonMessage.readlines()]
        r = random.randrange(0, len(self.mNoon))
        return self.mNoon[r]

    def goodMorningInAfterNoon(self):
        with open(self.data + 'morningReplayInAfterNoon.txt', 'r', 1, encoding='utf-8') as goodAfterNoonMessage:
            self.mAfterNoon = [line.strip()
                               for line in goodAfterNoonMessage.readlines()]
        r = random.randrange(0, len(self.mAfterNoon))
        return self.mAfterNoon[r]

    def hello(self):
        with open(self.data + 'hello.txt', 'r', 1, encoding='utf-8') as helloMessage:
            self.hello = [line.strip() for line in helloMessage.readlines()]
        r = random.randrange(0, len(self.hello))
        return self.hello[r]

    def goodNight(self):
        with open(self.data + 'sleepGreeting.txt', 'r', 1, encoding='utf-8') as sleepGreetingMessage:
            self.gNight = [line.strip()
                           for line in sleepGreetingMessage.readlines()]
        r = random.randrange(0, len(self.gNight))
        return self.gNight[r]

    def shyTB(self):
        with open(self.data + 'shyReplay.txt', 'r', 1, encoding='utf-8') as shyTBMessage:
            self.shyReplay = [line.strip()
                              for line in shyTBMessage.readlines()]
        r = random.randrange(0, len(self.shyReplay))
        return self.shyReplay[r]

    def TBhelp(self):
        with open(self.data + 'help.txt', 'r', 1, encoding='utf-8') as helpMessage:
            self.helpMessage = helpMessage.read()
        return self.helpMessage

    def weatherReport(self, keyMessage, day, informationFlag, time):
        # day {0:today,1:tomorrow,2:next_tomorrow}
        with open(self.data + 'cityCodes.json', 'r', 1, encoding='utf-8') as cityCodes:
            self.cityCodes = json.load(cityCodes)

        # どこの天気のことを言っているのかを探す
        city = None
        for cityName in self.cityCodes.keys():
            if cityName in keyMessage:
                city = cityName

        if city in self.cityCodes.keys():
            code = self.cityCodes[city]
            responce = urllib.request.urlopen(
                'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' %
                code).read()
            # responce =
            # urllib3.PoolManager().request('GET','http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%cityCode)
            # HTTPsも使える版
            responce = json.loads(responce.decode('utf-8'))

            if informationFlag:
                reply = responce['description']['text']
            elif (day >= 0 and day < 2) or (day == 2 and time >= 10):
                weather = responce['forecasts'][day]
                reply = weather['dateLabel'] + "は" + weather['telop'] + "だよ！"
            else:
                reply = responce['location']['city'] + "の天気は\n"
                for a in responce['forecasts']:
                    reply = reply + a['dateLabel'] + "は" + a['telop'] + "\n"
                reply += "これ以上はわかんないや。ごめんね！"
        else:
            reply = 'cannot find the city.'

        return reply

    def ohayo(self, time):
        if time in {23}:  # 時間で変動処理。pythonにswitchないのがつらいところ。
            reply = 'もうそろそろ寝る時間じゃない？'
        elif time in {19, 20, 21, 22}:
            reply = 'もう夜だよ...'
        elif time in {16, 17, 18}:
            reply = 'もう夕方だよぉ'
        elif time in {15}:
            reply = 'もうおやつの時間だよー'
        elif time in {14}:
            reply = self.goodMorningInAfterNoon()  # 変数名長いって？僕もそう思う。
        elif time in {12, 13}:
            reply = self.goodNoon()
        elif time in {7, 8, 9, 10, 11}:
            reply = self.goodMorning()
        elif time in {4, 5, 6}:
            reply = '朝早いね～'
        elif time in {0, 1, 2, 3}:
            reply = 'まだ深夜だよ'
        else:
            reply = 'いま何時？'
        return reply

    def tst(self):
        print("いえーい")


if __name__ == '__main__':
    rply = Replay()
    print(rply.goodNight())
    rply.tst()
