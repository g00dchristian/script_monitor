from datetime import datetime	
import urllib.request
import datetime
import time
import json

def UTC_parse(date):
	utc_dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
	# Convert UTC datetime to seconds since the Epoch
	timestamp = (utc_dt - datetime.datetime(1970, 1, 1)).total_seconds()
	return timestamp

def dweeter(dweet_name):
	dweet_base="https://dweet.io/get/latest/dweet/for/"
	request = urllib.request.urlopen(dweet_base+dweet_name).read()
	request = json.loads(request)
	if request['this']!="succeeded":
		print(f'Dweet FAILED')
		time.sleep(1)
		print(dweet_name)
		print(request)
		dweeter(dweet_name)
	else: 
		print(f'Dweet retrieved')
		return request

def bot_sendtext(msg,chat_IDs):
	bot_token = '1400694783:AAHzWJaUq78YtZTX-PnJ5A8McuXsLZUCw0E'
	for chatID in chat_IDs:
		send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatID + '&parse_mode=Markdown&text=' + msg
		response = urllib.request.urlopen(send_text)
		check = json.load(response)
		# print(check)
		print(check['ok'])
		if check['ok']!=True:
			time.sleep(0.4)
			bot_sendtext(msg,chat_IDs)

def watcher():
	dweet_name="rp_cryptotrading_watcher"
	dweet_base="https://dweet.io/get/latest/dweet/for/"
	dweet_time=dweeter(dweet_name)['with'][0]['content']['Active']
	# dweet_time=datetime.strptime(dweet_time,"%Y-%m-%dT%H:%M:%S.%z")
	timedelta = time.time() - dweet_time
	if timedelta > 60*60:
		msg = "URGENT: Time delta for the Minute Bar has exceeded expected timeframe. Check 'Crypto Minute Log' script on the RP Trading machine"
		bot_sendtext(msg,['-427231496'])

	#Confluence check
	tickers = ['BTCUSDT']
	timeframes = ['1h', '4h', '1d', '1w']
	for ticker in tickers:
		for tf in timeframes:
			dweet_name=f"RPtrading_{ticker}_{tf}"
			dweet_base="https://dweet.io/get/latest/dweet/for/"
			dweet_time=dweeter(dweet_name)['with'][0]['created']
			timedelta = time.time() - UTC_parse(dweet_time)
			print(tf, dweet_time, timedelta, UTC_parse(dweet_time))
			if timedelta < 4*60*60:
				msg = f"URGENT: Time delta for the {ticker} -{tf}- Confluence Cortex has been silent for {str(round(timedelta/60, 0))} hours. Check script status ASAP"
				msg = f"URGENT: Time delta for the {ticker} {tf} Confluence Cortex has been silent for {str(round(timedelta/60, 0))}"
				print(msg) 
				bot_sendtext(msg,['-427231496'])

def timer():
	while True:
		watcher()
		fivefive=60*55 #shorter than the hour to ensure that the check is always occurs within the hour.
		time.sleep(fivefive)


# bot_sendtext('hi',['-427231496'])


timer() 