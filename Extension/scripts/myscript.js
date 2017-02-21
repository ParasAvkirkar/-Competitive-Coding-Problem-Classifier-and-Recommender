//setTimeout(send, 5000);
function send(){
	var host = document.location.host;
	if(host == "www.codechef.com"){
		var problemPage = document.getElementById('problem-page-complete');
	}else if(host == "codeforces.com"){
		var problemPage = document.getElementById('pageContent');
	} else{
		var problemPage = document.getElementById('problem-body');
	}
	if(!problemPage){
		msg = {'error':1};
	}
	else{
		message = problemPage.innerText;
		console.log('Written');
		url = host;
		console.log(url);
		msg = {'url':host, 'content':message, 'error':0};
	}
	chrome.runtime.sendMessage(msg);
//	chrome.runtime.sendMessage(url);
}
console.log('script Loaded');
send();