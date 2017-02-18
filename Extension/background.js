chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
	console.log(response);
	var val = 1;
    var entry1 = 3;

//    $.getJSON({
//    url: "http://127.0.0.1:5000/getData",
//    data: { entry2_id: val, entry1_id: entry1 },
//
//	    success: function(data){
//	        // $("#varID").html(data.var1);
//	        console.log(data)
//	    }
//
//    });

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
})
chrome.runtime.onInstalled.addListener(function(details){
    if(details.reason == "install"){
        console.log("This is a first install!");
    }else if(details.reason == "update"){
        var thisVersion = chrome.runtime.getManifest().version;
        console.log("Updated from " + details.previousVersion + " to " + thisVersion + "!");
    }
});