function hello() {
  document.getElementsByTagName('body')[0].style.width = "400px" ;
  document.getElementById('predict').style.display = "none";
  document.getElementById('loading').style.display = "block";
  chrome.tabs.executeScript({
    file: 'scripts/myscript.js'
  });
}

document.getElementById('predict').addEventListener('click', hello);

function drawGraph(result) {
	document.getElementById('loading').style.display = "none";
    document.getElementsByTagName('body')[0].style.height = "400px" ;
    document.getElementsByTagName('body')[0].style.width = "400px" ;
    document.getElementById('chartContainer').style.height = "100%" ;
    document.getElementById('chartContainer').style.width = "100%" ;
    document.getElementById('predict').style.width = "0%" ;
    document.getElementById('predict').style.height = "0%" ;
	var chart = new CanvasJS.Chart("chartContainer",
			{
				title:{
					text: "Category Probability"
				},
				axisX: {
					interval: 10
				},
				dataPointWidth: 60,
				data: [{
					type: "column",
					indexLabelLineThickness: 2,
					dataPoints: [
						  { x: 10, y: parseFloat(result[1]), label: result[0]},
						  { x: 20, y: parseFloat(result[3]), label: result[2]},
						  { x: 30, y: parseFloat(result[5]), label: result[4]}
					]
				}]
			});
			chart.render();
}

window.onload = hello;