//setTimeout(send, 5000);
function send(){
	var left= document.getElementById('problem-left');
	var c = left.getElementsByClassName('content');
	var problemPage = document.getElementById('problem-page-complete');
//	message = c[0].innerText;
	message = problemPage.innerText;
	console.log('Written');
	url = window.location.href;
	console.log(url);
	chrome.runtime.sendMessage(message);
//	chrome.runtime.sendMessage(url);
}
console.log('script Loaded');
send();