import datetime
import time
import urllib
import json
import requests
# 获取V2EX热榜
from lxml import etree
from operator import methodcaller

get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


class Spider:
    def __init__(self):
        self.urls = {
            "V2EX": "https://www.v2ex.com/?tab=hot",
            "ITHome": "https://www.ithome.com/",
            "ZhiHu": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true",
            "WeiBo": "https://s.weibo.com/top/summary/summary",
            "TieBa": "http://tieba.baidu.com/hottopic/browse/topicList",
            "DouBan": "https://www.douban.com/group/explore",
            "TianYa": "http://bbs.tianya.cn/list.jsp?item=funinfo&grade=3&order=1",
            "HuPu": "https://bbs.hupu.com/all-gambia",
            "GitHub": "https://github.com/trending",
        }

    def GetV2EX(self):
        url = "https://www.v2ex.com/?tab=hot"
        response = requests.get(url=url, headers=HEADERS)
        html = etree.HTML(response.text)
        titles = html.xpath("//span[@class='item_title']/a/text()")
        urls = html.xpath("//span[@class='item_title']/a/@href")
        urls = list(map(lambda x: "https://www.v2ex.com" + x, urls))
        print(titles, urls)

    def GetITHome(self):
        url = "https://www.ithome.com/"
        response = requests.get(url=url, headers=HEADERS)
        html = etree.HTML(response.content.decode('utf-8'))
        titles = html.xpath(
            "//div[@class='lst lst-2 hot-list']/div[1]/ul/li/a[@title]/text()")
        urls = html.xpath(
            "//div[@class='lst lst-2 hot-list']/div[1]/ul/li/a/@href")
        print(titles, urls)

    def GetZhiHu(self):
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        response = requests.get(url=url, headers=HEADERS)
        json_result = response.json()
        json_data = json_result['data']
        print(json_data)

    def GetWeiBo(self):
        url = self.urls.get("WeiBo")
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.text)
        titles = html.xpath("//table/tbody/tr/td[2]/a/text()")
        urls = html.xpath("//table/tbody/tr/td[2]/a/@href")
        urls = list(map(lambda x: "https://s.weibo.com" +
                                  urllib.parse.unquote(x).replace("#", "%23"), urls))
        print(titles, urls)

    def GetTieBa(self):
        url = self.urls.get("TieBa")
        response = requests.get(url, headers=HEADERS)
        json_result = response.json()

        json_data = json_result['data']['bang_topic']['topic_list']

        titles = []
        urls = []

        for x in json_data:
            titles.append(x['topic_name'])
            urls.append(urllib.parse.unquote(
                x['topic_url'].replace('amp;', '')))
        print(titles, urls)

    def GetDouBan(self):
        url = self.urls.get("DouBan")

        response = requests.get(url, headers=HEADERS)

        html = etree.HTML(response.text)

        titles = html.xpath(
            "//div[@class='channel-item']/div[@class='bd']/h3/a/text()")
        urls = html.xpath(
            "//div[@class='channel-item']/div[@class='bd']/h3/a/@href")

        print(titles, urls)

    def GetTianYa(self):
        url = self.urls.get("TianYa")
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "http://bbs.tianya.cn/list.jsp?item=funinfo&grade=3&order=1",
            "Host": "bbs.tianya.cn"
        }

        response = requests.get(url, headers)
        html = etree.HTML(response.text)
        titles = html.xpath(
            "//table/tbody/tr/td[1]/a/text()")
        urls = html.xpath("//table/tbody/tr/td[1]/a/@href")
        print(titles, urls)

    def GetHuPu(self):
        """
        虎扑
        :return:
        """
        url = self.urls.get("HuPu")
        response = requests.get(url, HEADERS)
        html = etree.HTML(response.text)
        titles = html.xpath("//div[@class='bbsHotPit']//div/ul/li/span[1]//a/@title")
        urls = html.xpath("//div[@class='bbsHotPit']//div/ul/li/span[1]//a/@href")
        print(titles, urls)

    def GetGitHub(self):
        """
        github
        :return:
        """
        url = self.urls.get("GitHub")
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.text)
        urls = html.xpath("//article[@class='Box-row']/h1/a/@href")
        titles = list(map(lambda x: x[1:].replace("/", " / "), urls))
        urls = list(map(lambda x: "https://github.com" + x, urls))
        print(titles, urls)

    def GetBaiDu(self):
        """
        百度
        :return:
        """
        url = 'http://top.baidu.com/buzz?b=341'
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.content.decode('gb2312'))
        titles = html.xpath(
            "//table[@class='list-table']//tr/td[@class='keyword']/a[@class='list-title']/text()")
        urls = list(map(lambda x: "https://www.baidu.com/s?wd=" + x, titles))
        print(titles, urls)

    def Get36Kr(self):
        """
        36Kr
        :return:
        """
        url = 'https://36kr.com/newsflashes'
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.content.decode('utf-8'))
        titles = html.xpath(
            "//div[@class='hotlist-main']/div//a//text()")
        urls = html.xpath(
            "//div[@class='hotlist-main']/div[@class='hotlist-item-toptwo']/a[1]/@href|//div[@class='hotlist-main']/div[@class='hotlist-item-other clearfloat']/div[@class='hotlist-item-other-info']/a/@href")
        urls = list(map(lambda x: "https://36kr.com" + x, urls))
        print(titles, urls)

    def GetQDaily(self):
        """
        好奇心日报
        :return:
        """
        url = 'https://www.qdaily.com/tags/29.html'
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.content.decode("utf-8"))
        titles = html.xpath("//div[@class='packery-container articles']/div/a/div/div/img/@alt")
        urls = html.xpath("//div[@class='packery-container articles']/div/a/@href")
        print(titles, urls)

    def GetGuoKr(self):
        """
        果壳
        :return:
        """
        url = "https://www.guokr.com/apis/minisite/article.json?retrieve_type=by_channel&channel_key=hot&limit=20"
        response = requests.get(url, headers=HEADERS)
        json_result = response.json()
        json_data = json_result['result']
        titles = []
        urls = []
        for x in json_data:
            titles.append(x['title'])
            urls.append(x['resource_url'])
        print(titles, urls)

    def GetHuXiu(self):
        """
        虎嗅
        :return:
        """
        data = {
            "platform": "www",
            "pagesize": 22
        }
        url = "https://article-api.huxiu.com/web/article/articleList"
        response = requests.post(url, data)
        json_result = response.json()
        json_data = json_result['data']['dataList']
        titles = []
        urls = []
        for x in json_data:
            titles.append(x['title'])
            urls.append("https://www.huxiu.com/article/" + x['aid'] + ".html")
        print(titles, urls)

    def GetDBMovie(self):
        """
        豆瓣热门电影
        :return:
        """
        url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=50&page_start=0"
        # headers2 = {
        #     'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Connection': 'close'}
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, headers=HEADERS)
        json_result = response.json()
        json_data = json_result['subjects']
        titles = []
        urls = []
        for x in json_data:
            titles.append(x['title'])
            urls.append(x['url'])
        print(titles, urls)

    def GetDBTV(self):
        """
        豆瓣热门电视剧
        :return:
        """
        url = "https://movie.douban.com/j/search_subjects?type=tv&tag=热门&page_limit=50&page_start=0"
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, headers=HEADERS)
        json_result = response.json()
        json_data = json_result['subjects']
        titles = []
        urls = []
        for x in json_data:
            titles.append(x['title'])
            urls.append(x['url'])
        print(titles, urls)

    def GetZHDaily(self):
        """
        知乎日报
        :return:
        """
        url = 'https://daily.zhihu.com'
        response = requests.get(url, headers=HEADERS)
        html = etree.HTML(response.text)
        titles = html.xpath("//div[@class='box']/a/span/text()")
        urls = html.xpath("//div[@class='box']/a/@href")
        urls = list(map(lambda x: "https://daily.zhihu.com" + x, urls))
        print(titles, urls)

    def GetSegmentfault(self):
        """
        思否
        :return:
        """
        url = 'https://segmentfault.com/hottest'
        response = requests.get(url, headers=HEADERS)

        html = etree.HTML(response.text)

        titles = html.xpath(
            "//div[@class='news__item-info clearfix']/a/div/h4/text()")
        urls = html.xpath("//div[@class='news__item-info clearfix']/a/@href")
        urls = list(map(lambda x: "https://segmentfault.com" + x, urls))
        print(titles, urls)


def ExecGetData():
    pass


if __name__ == '__main__':
    spider = Spider()
    allData = [
        "V2EX",
        "ZhiHu",
        "WeiBo",
        "TieBa",
        "DouBan",
        "TianYa",
        "HuPu",
        "GitHub",
        "BaiDu",
        "36Kr",
        "QDaily",
        "GuoKr",
        "HuXiu",
        "ZHDaily",
        "Segmentfault",
        # "WYNews",
        # "WaterAndWood",
        # "HacPai",
        # "KD",
        # "NGA",
        # "WeiXin",
        # "Mop",
        # "Chiphell",
        # "JianDan",
        # "ChouTi",
        # "ITHome",
    ]
    print("开始爬取"+str(len(allData))+"种数据类型")
    for value in allData:
        funcname = "Get"+value
        methodcaller(funcname)(spider)

