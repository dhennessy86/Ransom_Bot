# -*- coding: utf-8 -*-

from lxml import html
import requests
import re
import math
import tweepy, time
from credentials import *

# Twitter Users to call
Users = "<insert user handle>"

# Twitter Auth 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Define Function for comparing if value has changed
def Compare(x,y):
	if x==y:
		print ("The number of payments has not increased, still at: %s" % (x))
	elif x>y:
		tweetlist = ("Number of Petya-Ransomware Payments: %s \nTotal Amount Paid to Date in Euro: €%s \n%s" % (No_transactions,Round_Euro,Users) )
		api.update_status(tweetlist)
		print "Tweet has been sent"
		output = open ("num.txt","w") 
		output.write(str(x)) 
		output.close()
	else:
		print ("The number of payments has not increased, still at: %s" % (x))
		
#retrieve web page
page = requests.get('https://blockchain.info/address/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw') #<insert new payment sites>
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
rates1 = (", ".join(rates))									   # convert to string
euro_rate = re.findall(r"[0-9]{1,},[0-9]{1,}", rates1 )						   # strip out euro value
euro_rate1 = (", ".join(euro_rate))								   # convert to string
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
