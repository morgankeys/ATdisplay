#!/usr/bin/python

import pickle, datetime, demjson
from tweetob import Tweet

def SortByDate(tweetlist):
	def sortfunction(tweet):
		timesince=datetime.datetime.now()-tweet.date
		return timesince
	tweetlist=sorted(tweetlist,key=sortfunction)
	return tweetlist

def FilterTweets(tweetlist,minvalue,maxvalue,time):
	newlist=[]
	for tweet in tweetlist:
		timesince=datetime.datetime.now()-tweet.date
		if timesince<=datetime.timedelta(hours=time):
			newlist.append(tweet)
	if len(newlist)>=minvalue and len(newlist)<=maxvalue:
		newlist=newlist
	elif len(newlist)>maxvalue:
		newlist=newlist[0:maxvalue]
	elif len(newlist)<minvalue:
		newlist=tweetlist[0:minvalue]
	return newlist

def loadHolidayTweet():
	htweet = Tweet("Veterans Day","http://www.etags.ca/images/yellow-ribbon.gif","","",datetime.datetime(2009,11,11,9,0),"0")
	return htweet

def main():
	picklefile=open('tweets.pkl','rb')
	picklecontents=pickle.load(picklefile)
	try:
		tweetlist=SortByDate(picklecontents)
		tweetlist.append(loadHolidayTweet())
		tweetlist = SortByDate(tweetlist)
		tweetlist=FilterTweets(tweetlist,8,32,24)
	except:
		tweetlist=[picklecontents]
	output=demjson.encode({"tweets":tweetlist})
	print "Content-type:text/plain\n"
	print output
	
if __name__ == "__main__":
    main()
