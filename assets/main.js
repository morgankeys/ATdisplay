function ajaxObject(url, callbackFunction) {
    var that=this;      
    this.updating = false;
    this.abort = function() {
	if (that.updating) {
	    that.updating=false;
	    that.AJAX.abort();
	    that.AJAX=null;
	}
    }
    this.update = function(passData,postMethod) { 
	if (that.updating) { return false; }
	that.AJAX = null;                          
	if (window.XMLHttpRequest) {              
	    that.AJAX=new XMLHttpRequest();              
	} else {                                  
	    that.AJAX=new ActiveXObject("Microsoft.XMLHTTP");
	}                                             
	if (that.AJAX==null) {                             
	    return false;                               
	} else {
	    that.AJAX.onreadystatechange = function() {  
		if (that.AJAX.readyState==4) {             
		    that.updating=false;                
		    that.callback(that.AJAX.responseText,that.AJAX.status,that.AJAX.responseXML);        
		    that.AJAX=null;                                         
		}                                                      
	    }                                                        
	    that.updating = new Date();                              
	    if (/post/i.test(postMethod)) {
		var uri=urlCall+'?'+that.updating.getTime();
		that.AJAX.open("POST", uri, true);
		that.AJAX.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		that.AJAX.send(passData);
	    } else {
		var uri=urlCall+'?'+passData+'&timestamp='+(that.updating.getTime()); 
		that.AJAX.open("GET", uri, true);                             
		that.AJAX.send(null);                                         
	    }              
	    return true;                                             
	}                                                                           
    }
    var urlCall = url;        
    this.callback = callbackFunction || function () { };
}

var counter = 0;
var mainIntervalId = 0;
var jsonData = "";
var tweets = new Array();

function findBitly(paneltext){
   var patt = /http:\/\/bit.ly\/([A-Za-z0-9]+)/;
    
    //new_paneltext = paneltext.replace(patt,"<br /><img src='http://bit.ly/$1.qrcode' width='249' height='249'/>");

    links = paneltext.match(patt);
    if (links){
	new_paneltext = paneltext + "<br /><img src='http://bit.ly/" + links[1] +".qrcode' width='200' height='200'/>";
    }

    if (new_paneltext == paneltext){
	patt = /(http:\/\/[A-Za-z0-9\/_.]+)/
	}

    return new_paneltext;
}

function findImage(paneltext){
    var patt = /http:\/\/twitpic.com\/([A-Za-z0-9]+)/;
    
    new_paneltext = paneltext.replace(patt,"<br /><img src='http://twitpic.com/show/thumb/$1.jpg' width='150' height='150'/>");

    if (new_paneltext == paneltext){
	patt = /(http:\/\/[a-z0-9\/_.]+)/
	}

    return new_paneltext;
}

function renderPanel(tweet){
    if (tweet.name != ""){
	document.getElementById("mainpanel").innerHTML = "<div id='paneltweet'>"+findBitly(findImage(cleanTweet(tweet.text)))+"</div><div class='authorinfo'><div class='authorimage'><img src='"+tweet.image+"'/></div><div id='panelnames'>"+tweet.name+" ("+tweet.user+")</div><div id='paneldate'>"+tweet.date+"</div></div>";
    }else{
	document.getElementById("mainpanel").innerHTML = "<div id='paneltweet'>"+findImage(cleanTweet(tweet.text))+"</div><div class='authorinfo'><div class='authorimage'><img src='"+tweet.image+"'/></div><div id='panelnames'>"+tweet.user+"</div><div id='paneldate'>"+tweet.date+"</div></div>";
    }
}

function resizePanel(){
    document.getElementById("tweetlist").style.height = String(window.innerHeight)+"px";
    document.getElementById("mainpanel").style.height = String(window.innerHeight)+"px";
    document.getElementById("mainpanel").style.width = String(document.body.clientWidth-250)+"px";
}

function cleanTweet(paneltext){
    if (paneltext.slice(0,10).toLowerCase() == "@sidisplay"){paneltext = paneltext.slice(10);}
    else if (paneltext.slice(0,11).toLowerCase() == ".@sidisplay"){paneltext = paneltext.slice(11);};

    return paneltext;
};

function incrementTweet(){
    // check if in range
    if (counter < tweets.length-1){
	// if yes, set panel, adjust style in list
	counter = counter + 1;
	renderPanel(tweets[counter]);
	document.getElementById("tweet_"+String(counter)).setAttribute("class","activetweet");
	document.getElementById("tweet_"+String(counter-1)).setAttribute("class","inactivetweet");
    }else{
	// if not, clear interval and begin cycle
	clearInterval(mainIntervalId);
	jsonLoads();
    }
}

function goToTweet(tweetid){
        document.getElementById("tweet_"+String(counter)).setAttribute("class","inactivetweet");
	counter = tweetid;
	renderPanel(tweets[counter]);
        document.getElementById("tweet_"+String(counter)).setAttribute("class","activetweet");
}

function beginCycle(jsonData){
    var tweetlisthtml = "";
    if (jsonData.tweets.length < 1){
	tweetlisthtml = tweetlisthtml + "<div id='notweets'>Sorry, no tweets available.</div>";
	document.getElementById("mainpanel").innerHTML = "<div id='notweet'>Sorry, no tweet available.</div>";
    }else{
	for (var i = 0; i < jsonData.tweets.length; i++){
	    tweetlisthtml = tweetlisthtml + "<div id='tweet_"+String(i)+"' onclick='goToTweet("+String(i)+")' class='inactivetweet'>"+cleanTweet(jsonData.tweets[i].text)+"</div>";
	};
	counter = 0;
	renderPanel(jsonData.tweets[0]);
    };
    // set timer w/ markers
    tweets = jsonData.tweets
    mainIntervalId = setInterval("incrementTweet();",10000);

    document.getElementById("tweetlist").innerHTML=tweetlisthtml;
    document.getElementById("tweet_"+String(counter)).setAttribute("class","activetweet");
}

function jsonLoads(){
    var ajaxRequest = new ajaxObject('sidisplay2.py');
    ajaxRequest.callback = function (responseText) {
	jsonData = eval("("+responseText+")");
	beginCycle(jsonData);
    }
    ajaxRequest.update();
}

function load(){
    resizePanel();
    jsonLoads();
}
