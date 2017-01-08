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
  			var advertising = new RadarChart("advertising", {
			data: [[100000, 200000, 175000, 100000, 100000],
				   [200000, 125000, 105000, 100000, 100000]],

			maxValue: 250000,

			categories: ["Internet", "Television", "Radio",
						 "Newspaper", "Magazine"],

			legend: true,
			legendTitle: "Advertising",
			legendLabels: ["Year 1", "Year 2"],
		});
  			console.log(data); // 2pm
  			alert(data.result)
		}, "json");
})
