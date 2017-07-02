# -*- coding: utf-8 -*-
#########################################################################################################################
#
# Created: 02 -July -2017
# Purpose: track Payments made to Petya hard coded bitcoin payment site
#          Script will be called every 30 mins from crontab
#########################################################################################################################

from lxml import html
import requests
import re
import math
import tweepy, time
from credentials import *

# Twitter Auth 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Define Function for comparing if value has changed
def Compare(x,y):
	if x==y:
		print x," is equal to ",y
		print "Nothing to do"
	elif x>y:
		tweetlist = ("New payment made for Petya, the total number of payments is now: %s \nTotal Amount Paid: €%s" % (No_transactions,Round_Euro) )
		api.update_status(tweetlist)
		print "Tweet has been sent"
		output = open ("num.txt","w") 
		output.write(str(x)) 
		output.close()
	else:
		print x," is less than ",y 
		print "nothing to do"
		

#retrieve web page
page = requests.get('https://blockchain.info/address/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw')
tree = html.fromstring(page.content)

# this will get the number of transactions, creates lists
total = tree.xpath('//*[@id="n_transactions"]/text()')
Received = tree.xpath('//*[@id="total_received"]/font/span/text()')

#display number of transactions
No_transactions = (", ".join(total))

#Value is in BTC, strip out digits
strip = (", ".join(Received))			# convert to string
No_BTC = re.sub(r"[^0-9.]", "", strip)  # strip out BTC value


page1 = requests.get('http://api.coindesk.com/v1/bpi/currentprice/EUR.json')  # get request to get latest BTC rates in euro
contents = page1.text													
rates = re.findall(r"EUR\",\"rate\":\".*\",\"d", contents )					   # strip out in euro line
rates1 = (", ".join(rates))													   # convert to string
euro_rate = re.findall(r"[0-9]{1,},[0-9]{1,}", rates1 )						   # strip out euro value
euro_rate1 = (", ".join(euro_rate))											   # convert to string
euro_rate2 = re.sub(r"[^0-9]", "", euro_rate1)
Total_Value = float(euro_rate2) * float(No_BTC)
Round_Euro = int(round(Total_Value))


# Check if the number of transaction has increased
x = int(No_transactions)
file = open ("num.txt", "r")
file_contents = file.readline()	
y = int(file_contents)
file.close()

Compare(x,y)
