chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
	console.log(response);
	var val = 1;
    var entry1 = 3;

    $.getJSON({
    url: "http://127.0.0.1:5000/getData",
    data: { entry2_id: val, entry1_id: entry1 },
	    
	    success: function(data){
	        // $("#varID").html(data.var1);
	        console.log(data)
	    }

    });

    $.post( "http://127.0.0.1:5000/postData", { page: response }, function( data ) {
  			// console.log( data.name ); // John
  			console.log(data); // 2pm
		}, "json");
})
