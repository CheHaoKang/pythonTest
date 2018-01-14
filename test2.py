import re,requests,random
from twstock import Stock
import pymysql.cursors
import sys
import datetime

header={'headers':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

class GatherProxy(object):
	'''To get proxy from http://gatherproxy.com/'''
	url='http://gatherproxy.com/proxylist'
	pre1=re.compile(r'<tr.*?>(?:.|\n)*?</tr>')
	pre2=re.compile(r"(?<=\(\').+?(?=\'\))")

	def getelite(self,pages=1,uptime=70,fast=True):
		'''Get Elite Anomy proxy
		Pages define how many pages to get
		Uptime define the uptime(L/D)
		fast define only use fast proxy with short reponse time'''

		proxies=set()
		for i in range(1,pages+1):
			params={"Type":"elite","PageIdx":str(i),"Uptime":str(uptime)}
			r=requests.post(self.url+"/anonymity/t=Elite",params=params,headers=header)
			for td in self.pre1.findall(r.text):
				if fast and 'center fast' not in td:
					continue
				try:
					tmp= self.pre2.findall(str(td))
					if(len(tmp)==2):
						proxies.add(tmp[0]+":"+str(int('0x'+tmp[1],16)))
				except:
					pass
		return proxies

def importProxies(fileName):
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
	cur = conn.cursor()

	with open(fileName, 'r', encoding='UTF-8') as file:
		for line in file:
			try:
				insert = "INSERT INTO stockproxies (proxyIPPort, proxyFailtimes, proxyReponseperiod) VALUES (%s, 0, '0')"
				cur.execute(insert, line.strip())
			except:
				print("Unexpected error:", sys.exc_info()[0])
				cur.close()
				conn.close()
				raise

	cur.close()
	conn.commit()
	conn.close()

if __name__ == "__main__":
    proxyIPList = ['121.232.199.131:9000','121.232.199.131:9001','121.232.199.131:9000','121.232.199.131:9002']
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198',
                               db='stockevaluation', charset="utf8")
        cur = conn.cursor()
        insert = "INSERT IGNORE INTO stockproxies (proxyIPPort) VALUES (%s)"
        cur.executemany(insert, proxyIPList)
        cur.close()
        conn.commit()
        conn.close()
    except:
        print("Unexpected error:", sys.exc_info())
        cur.close()
        conn.close()