#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from wxpy import Bot

bot = Bot(console_qr=True, cache_path="logoo.pkl")
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}


def auto_send():
    try:
        weather = get_weather()
        gw = parse_weather(weather)
        my_friend = bot.friends().search(u'史博琼')[0]
        my_friend.send(u"早上好Y(^o^)Y，这里是今日份的天气信息请查收!")
        my_friend.send(gw)
        # t = Timer(60, auto_send)
        # t.start()
    except:
        my_friend = bot.friends().search(u'史博琼')[0]
        print my_friend
        my_friend.send(u"报告老板，今日份的信息发送失败了！")


def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=fe23b6a085b5aef9b825082cde62295e&city=110100&extensions=all"
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    return rep.content


def get_calendar(date):
    url = "http://v.juhe.cn/calendar/day?key=4902d05822f120f191f0ae3869fbb455&date=" + date
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    return rep.content


def parse_calendar(date):
    data = json.loads(get_calendar(date))
    if data.get("error_code") != 0:
        print "get calendar error: " + str(data)
        return None
    return data.get("result").get("data")


def get_limit():
    url = "http://yw.jtgl.beijing.gov.cn/jgjxx/services/getRuleWithWeek"
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    data = json.loads(rep.content)
    if data.get("state") != "success":
        return None
    return data.get("result")


def parse_weather(weather):
    weather = json.loads(weather)
    status = weather.get("status")
    if status != "1":
        print "status: " + status
        return None
    info = weather.get("info")
    if info != "OK":
        print "info: " + info
        return None
    forecasts = weather.get("forecasts")[0]
    date = forecasts.get("reporttime")[0:10]
    for cast in forecasts.get("casts"):
        format_date = date_format(date)
        if cast.get("date") == date:
            calendar_data = parse_calendar(date)
            if calendar_data is None:
                print "error calendar"
                return None
            limit = get_limit()
            if limit is None:
                print "error limit"
                return None
            limit_v = ""
            for limit_d in limit:
                if format_date == limit_d.get("limitedTime"):
                    date = format_date
                    cast["week"] = limit_d.get("limitedWeek")
                    limit_v = limit_d.get("limitedNumber")

            return u"-----温馨提示-----\n" \
                   u"->今日{}\n" \
                   u"->{}\n" \
                   u"->农历{}\n" \
                   u"->北京限行{}\n" \
                   u"->今天白天: {}风{}级\n" \
                   u"->温度范围: {}~{}°C" \
                .format(
                date,
                cast.get("week"),
                calendar_data.get("lunar"),
                limit_v,
                cast.get("daywind"),
                cast.get("daypower"),
                cast.get("daytemp"),
                cast.get("nighttemp"))
    return None


def date_format(date):
    sp = "2021-11-19".split("-")
    return u"{}年{}月{}日".format(sp[0], sp[1], sp[2])


if __name__ == "__main__":
    auto_send()
