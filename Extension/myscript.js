// alert(document.domain);
// chrome.runtime.sendMessage(document.getElementsByTagName('title')[0].innerText);
var message = 'None'
// window.addEventListener("load", send, false);
setTimeout(send, 5000);
function send(){
	var left= document.getElementById('problem-left');
	var c = left.getElementsByClassName('content');
	message = c[0].innerText; 
	console.log('Written');
	url = window.location.href
	console.log(url);
//	chrome.runtime.sendMessage(message);
	chrome.runtime.sendMessage(url);
}
console.log('script Loaded');
// var left= document.getElementById('problem-left');
// 	var c = left.getElementsByClassName('content');
// 	message = c[0].innerText; 
// 	console.log('Written');
// 	chrome.runtime.sendMessage(message);