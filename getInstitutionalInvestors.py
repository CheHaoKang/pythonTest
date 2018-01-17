import re,requests,random
from twstock import Stock
import pymysql.cursors
import sys
import datetime
from fake_useragent import UserAgent
import json

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

def getInstitutionalInvestors(date):
	# 自營商買賣超彙總表
	# http://www.twse.com.tw/fund/TWT43U?response=json&date=20180112
	# 投信買賣超彙總表
	# http://www.twse.com.tw/fund/TWT44U?response=json&date=&_=1515943335745
	# 外資及陸資買賣超彙總表
	# http://www.twse.com.tw/fund/TWT38U?response=json&date=20180112

	ua = UserAgent()
	insInvestArray = []

	# 自營商買賣超彙總表
	succeed = False
	while not succeed:
		header = {'User-Agent': str(ua.random)}
		res = requests.get("http://www.twse.com.tw/fund/TWT43U?response=json&date=" + str(date), headers=header)

		try:
			s = json.loads(res.text)
			if 'data' in s:
				for data in s['data']:
					insInvestArray.append((date,data[0].strip(),'dealer','dealerSelf',data[2].strip().replace(",", "")))
					insInvestArray.append((date, data[0].strip(), 'dealer', 'dealerSelf', ('' if data[3].strip().replace(",", "")=='0' else '-') + data[3].strip().replace(",", "")))
					insInvestArray.append((date, data[0].strip(), 'dealer', 'dealerHedging', data[5].strip().replace(",", "")))
					insInvestArray.append((date, data[0].strip(), 'dealer', 'dealerHedging', ('' if data[6].strip().replace(",", "")=='0' else '-') + data[6].strip().replace(",", "")))
					insInvestArray.append((date, data[0].strip(), 'dealer', 'dealer', data[8].strip().replace(",", "")))
					insInvestArray.append((date, data[0].strip(), 'dealer', 'dealer', ('' if data[9].strip().replace(",", "")=='0' else '-') + data[9].strip().replace(",", "")))
				succeed = True
			elif '很抱歉' in s['stat']:
				succeed = True
		except:
			print("Unexpected error:", sys.exc_info())

	# 投信買賣超彙總表
	succeed = False
	while not succeed:
		header = {'User-Agent': str(ua.random)}
		res = requests.get("http://www.twse.com.tw/fund/TWT44U?response=json&date=" + str(date), headers=header)

		try:
			s = json.loads(res.text)
			if 'data' in s:
				for data in s['data']:
					insInvestArray.append((date,data[1].strip(),' investmentTrust',' investmentTrust',data[3].strip().replace(",", "")))
					insInvestArray.append((date, data[1].strip(), ' investmentTrust', ' investmentTrust', ('' if data[4].strip().replace(",", "")=='0' else '-') + data[4].strip().replace(",", "")))
				succeed = True
			elif '很抱歉' in s['stat']:
				succeed = True
		except:
			print("Unexpected error:", sys.exc_info())

	# 外資及陸資買賣超彙總表
	succeed = False
	while not succeed:
		header = {'User-Agent': str(ua.random)}
		res = requests.get("http://www.twse.com.tw/fund/TWT38U?response=json&date=" + str(date), headers=header)

		try:
			s = json.loads(res.text)
			if 'data' in s:
				for data in s['data']:
					insInvestArray.append((date, data[1].strip(),'foreignInvestor','foreignInvestor',data[3].strip().replace(",", "")))
					insInvestArray.append((date, data[1].strip(),'foreignInvestor','foreignInvestor',('' if data[4].strip().replace(",", "") == '0' else '-') + data[4].strip().replace(",", "")))
				succeed = True
			elif '很抱歉' in s['stat']:
				succeed = True
		except:
			print("Unexpected error:", sys.exc_info())

	try:
		conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198',
							   db='stockevaluation', charset="utf8")
		cur = conn.cursor()
		insert = "INSERT INTO stockInstitutionalInvestor (stockDate, stockCode, stockInvestorType, stockInvestorTypeDetail, stockAmount) VALUES (%s, %s, %s, %s, %s)"
		cur.executemany(insert, insInvestArray)
		cur.close()
		conn.commit()
		conn.close()
	except:
		print("Unexpected error:", sys.exc_info())
		cur.close()
		conn.close()

if __name__ == "__main__":
	getInstitutionalInvestors(str(sys.argv[1]))

