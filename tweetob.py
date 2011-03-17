import datetime

class Tweet:
    """ Class that keeps track of everything that goes with a single tweet
    Instance variables for:
    -- tweet: (string) 
    -- picture: (string) link to the users profile picture
    -- username: (string) 
    -- realname: (string) blank if the same as username
    -- date: (datetime object)
    -- tweetid: (integer)
    -- html: (string)"""
    
    def __init__(self,tweet,picture,username,realname,date,tweetid):
	""" Constructor just sets name and initializes tweets"""
	self.tweet=tweet
        self.picture = picture
        self.username=username
	self.realname=realname
	self.date=date
	self.datestring=date.strftime('%A, %B %d')
	self.tweetid=tweetid
	

	
    def json_equivalent(self):
	    tweet={"text":self.tweet,"image":self.picture,"user":self.username,"name":self.realname,"date":self.datestring,"id":self.tweetid}
	    return tweet
