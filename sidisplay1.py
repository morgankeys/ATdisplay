#new version replacing basic authentication with oauth. Requires python-oath2 version 1.2 and httplib2

#!/usr/bin/env python
import sys
import config
# if you installed httplib2 and oauth2 system-wide (rather than in your home directory),
# just comment out the next 3 line
sys.path.append(config.lib) #see config.py
sys.path.append(config.oauth) #see config.py
sys.path.append(config.httplib) #see config.py
#print sys.path

import urllib2, BeautifulSoup, time, datetime, pickle, urllib
from tweetob import Tweet
import oauth2 as oauth

import socket
import urllib2

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

filepath = "/home/display/public_html/"
	
def oauth_req(url, http_method="GET", post_body=None, http_headers=None):
	key = config.key #see config.py
	secret = config.secret #see config.py
	consumer = oauth.Consumer(config.consumerKey, config.consumerSecret) #see config.py
	token = oauth.Token(key=key, secret=secret)
	client = oauth.Client(consumer, token)
	resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
	return content
	
def LoadTweetFile():
	url="http://api.twitter.com/statuses/mentions.xml"
	feed = oauth_req(url)
	return feed

def Follow():
	followers='http://api.twitter.com/followers/ids/'+config.twitteruser+'.xml' #see config.py
	followers=urllib2.urlopen(followers)
	from BeautifulSoup import BeautifulStoneSoup
	soup=BeautifulStoneSoup(followers.read())
	followers=soup.findAll('id')
	friends='http://api.twitter.com/friends/ids/'+config.twitteruser+'.xml' #see config.py
	friends=urllib2.urlopen(friends)
	soup=BeautifulStoneSoup(friends.read())
	friends=soup.findAll('id')
	pending = "http://api.twitter.com/1/friendships/outgoing.xml"
	pending = oauth_req(pending) 
	soup=BeautifulStoneSoup(pending)
	pending=soup.findAll('id')
	friends.extend(pending)
	for person in followers:
		if person not in friends:
			url = "http://api.twitter.com/1/friendships/create.xml"
			data = 'user_id='+person.contents[0]
			follow= oauth_req(url, http_method="POST", post_body=data)
			
def DateTime(publisheddate):
	date= datetime.datetime.fromtimestamp(time.mktime(time.strptime(publisheddate, '%a %b %d %H:%M:%S +0000 %Y')))
	return date		
	
def TweetCollection(feed):
	"""parses the feed with beautifulsoup and creates a list of Tweet objects"""
	tweets=[]
	from BeautifulSoup import BeautifulStoneSoup
	soup=BeautifulStoneSoup(feed,selfClosingTags=["link"])
	for entry in soup.findAll("status"):
		tweet=str(entry.find('text').contents[0])
		username=str(entry.find('screen_name').contents[0])
		name=str(entry.find('name').contents[0])
		if name == username:
			name=''
		picture=str(entry.find('profile_image_url').contents[0])
		date=str(entry.find('created_at').contents[0])
		date=DateTime(date)
		tweetid=int(entry.find('id').contents[0])
		tweet=Tweet(tweet,picture,username,name,date,tweetid)
		tweets.append(tweet)
	return tweets

def addtoPickle(newtweets):
	try:
		output=open(filepath+'tweets.pkl','rb')
		inpickle=pickle.load(output)
		output.close()
		if len(inpickle) > 0:
			tweetids = []
			for tweet in inpickle:
				tweetids.append(tweet.tweetid)
			
			for tweet in newtweets:
				if tweet.tweetid not in tweetids:
					inpickle.append(tweet)
			picklefile=open(filepath+'tweets.pkl','wb')
			pickle.dump(inpickle, picklefile)
			picklefile.close()
		else:
			output = open(filepath+"tweets.pkl","wb")
			pickle.dump(newtweets,output)
			output.close()

	except:
		output=open(filepath+'tweets.pkl','wb')
		pickle.dump(newtweets,output)
		output.close()
	
def main():
	Follow()
	feed=LoadTweetFile()
	tweets=TweetCollection(feed)
	addtoPickle(tweets)
		
	
if __name__ == "__main__":
    main()

