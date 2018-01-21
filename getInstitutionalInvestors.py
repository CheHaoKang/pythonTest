import re,requests,random
from twstock import Stock
import pymysql.cursors
import sys
import datetime
from fake_useragent import UserAgent
import json

def getInstitutionalInvestors(date):
	# 自營商買賣超彙總表
	# http://www.twse.com.tw/fund/TWT43U?response=json&date=20180112
	# 投信買賣超彙總表
	# http://www.twse.com.tw/fund/TWT44U?response=json&date=&_=1515943335745
	# 外資及陸資買賣超彙總表
	# http://www.twse.com.tw/fund/TWT38U?response=json&date=20180112

	ua = UserAgent()
	insInvestArray = []

	hyphenDate = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

	# 自營商買賣超彙總表
	succeed = False
	while not succeed:
		header = {'User-Agent': str(ua.random)}
		res = requests.get("http://www.twse.com.tw/fund/TWT43U?response=json&date=" + str(date), headers=header)

		try:
			s = json.loads(res.text)
			if 'data' in s:
				for data in s['data']:
					insInvestArray.append((hyphenDate,data[0].strip(),'dealer','dealerSelf',data[2].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerSelf', ('' if data[3].strip().replace(",", "")=='0' else '-') + data[3].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerHedging', data[5].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerHedging', ('' if data[6].strip().replace(",", "")=='0' else '-') + data[6].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealer', data[8].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealer', ('' if data[9].strip().replace(",", "")=='0' else '-') + data[9].strip().replace(",", "")))
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
					insInvestArray.append((hyphenDate,data[1].strip(),' investmentTrust',' investmentTrust',data[3].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[1].strip(), ' investmentTrust', ' investmentTrust', ('' if data[4].strip().replace(",", "")=='0' else '-') + data[4].strip().replace(",", "")))
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
					insInvestArray.append((hyphenDate, data[1].strip(),'foreignInvestor','foreignInvestor',data[3].strip().replace(",", "")))
					insInvestArray.append((hyphenDate, data[1].strip(),'foreignInvestor','foreignInvestor',('' if data[4].strip().replace(",", "") == '0' else '-') + data[4].strip().replace(",", "")))
				succeed = True
			elif '很抱歉' in s['stat']:
				succeed = True
		except:
			print("Unexpected error:", sys.exc_info())

	if insInvestArray:  # not empty
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