from xlrd import open_workbook
import pymysql
import pymysql.cursors
import datetime
import requests
from fake_useragent import UserAgent
from lxml import etree
import collections
import re

if __name__ == "__main__":
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    urlPttStock = 'https://www.ptt.cc/bbs/Stock/index.html'
    res = requests.get(urlPttStock, headers=header, timeout=10)#, proxies=proxies, timeout=self.timeout)

    html = etree.HTML(res.text)
    result = html.xpath('//a/@href')
    previousPageUrl = ''
    urlArray = []
    for oneUrl in result:
        splitUrl = oneUrl.split('/')
        letters = collections.Counter(splitUrl[-1])
        if letters['.']>=3: # filter out urls with less than three dots
            urlArray.append(oneUrl)
        elif re.search('index[0-9]+', splitUrl[-1]):
            previousPageUrl = oneUrl

    print(urlArray)
    print(previousPageUrl)
    exit(1)

    #wb = load_workbook('C:/Users/blueplanet/Desktop/MovieCenter/excel範本/膠片Excel.xlsx')
    wb = open_workbook('C:/Users/blueplanet/Desktop/MovieCenter/excel範本/膠片Excel.xlsx')
    values = []
    for s in wb.sheets():
        # print('Sheet:',s.name)
        for row in range(1, s.nrows):
            col_names = s.row(0)
            # print(s.row(0))
            col_value = []
            for name, col in zip(col_names, range(s.ncols)):
                # print(s.cell(row, col).value)
                value = (s.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.append((s.name, name.value, value))
            values.append(col_value)
    # print(values)

    # src = u"中文"
    # src = src.encode('gbk')
    # print(src)
    # src = src.decode('latin1')
    # print(src)

    conn = pymysql.connect(host='localhost', port=3306, user='admin', passwd='', db='test', charset="utf8")
    # conn.set_charset('utf8')

    cur = conn.cursor()
    # cur.execute("SELECT * FROM 膠片")
    cur.execute("insert into 膠片(藏品類型) values('QQ')")

    print(cur.description)
    print()

    for row in cur:
        print(row)

    cur.close()
    conn.commit()
    conn.close()