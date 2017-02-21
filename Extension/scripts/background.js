chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
	console.log(response);
	if(response.error){
	   var views = chrome.extension.getViews({
                  type: "popup"
              });
       for (var i = 0; i < views.length; i++) {
        views[i].document.getElementById('loading').style.display='none';
        views[i].document.getElementById('error_div').style.display='block';
        views[i].document.getElementById('error_text').innerHTML = 'This page doesn\'t contain any problem';
       }
	}
	else{
      $.post( "http://127.0.0.1:5000/postData", response, function( data ) {
  //  			console.log(data);
  //  			alert(data.result)
              var views = chrome.extension.getViews({
                  type: "popup"
              });
              for (var i = 0; i < views.length; i++) {
  //				views[i].document.getElementById('result').innerHTML = '<h3>'+data.result+'</h3>';
                  views[i].document.getElementById('predict').style.visibility='hidden';
                  result = data.result+'';
                  views[i].drawGraph(result.split(','));
              }
          }, "json").fail(function(error) {
              var views = chrome.extension.getViews({
                  type: "popup"
              });
              for (var i = 0; i < views.length; i++) {
                  views[i].document.getElementById('loading').style.display='none';
                  views[i].document.getElementById('error_div').style.display='block';
              }
           });
	}
})
//chrome.runtime.onInstalled.addListener(function(details){
//    if(details.reason == "install"){
//        console.log("This is a first install!");
//    }else if(details.reason == "update"){
//        var thisVersion = chrome.runtime.getManifest().version;
//        console.log("Updated from " + details.previousVersion + " to " + thisVersion + "!");
//    }
//});

function createSetIconAction(path, callback) {
  chrome.browserAction.setTitle({title:'Suggest me some approaches for this !'});
  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext("2d");
  var image = new Image();
  image.onload = function() {
    ctx.drawImage(image,0,0,19,19);
    var imageData = ctx.getImageData(0,0,19,19);
    var action = new chrome.declarativeContent.SetIcon({imageData: imageData});

    callback(action);
  }
  image.src = chrome.runtime.getURL(path);
}

chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
  createSetIconAction("images/icon_2.png", function(setIconAction) {
    chrome.declarativeContent.onPageChanged.addRules([
      /* rule1, */
      {
        conditions : [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl : {hostEquals: 'www.codechef.com', pathContains: 'problems'}
          })
        ],
        actions    : [ setIconAction ]
      },
      /* rule2, */
      {
        conditions : [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl : {hostEquals: 'codeforces.com', pathContains: 'problemset/problem'}
          })
        ],
        actions    : [ setIconAction ]
      },
      /* rule3, */
      {
        conditions : [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl : {hostEquals: 'www.spoj.com', pathContains: 'problems'}
          })
        ],
        actions    : [ setIconAction ]
      }
    ]);
  });
});