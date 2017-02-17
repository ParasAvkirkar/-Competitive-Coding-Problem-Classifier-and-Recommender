function hello() {
  document.getElementsByTagName('body')[0].style.width = "400px" ;
  document.getElementById('predict').style.display = "none";
  document.getElementById('loading').style.display = "block";
  chrome.tabs.executeScript({
    file: 'myscript.js'
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
//
//				data: [
//				{
//					type: "bar",
//
//					dataPoints: [
//					{ x: 10, y: parseFloat(result[1]), label:result[0] },
//					{ x: 20, y: parseFloat(result[3]), label:result[2] },
//					{ x: 30, y: parseFloat(result[5]), label:result[4] }
//					]
//				}
//				]
//			});
//
//			chart.render();
				axisX: {
					interval: 10
				},
				dataPointWidth: 60,
				data: [{
					type: "column",
					indexLabelLineThickness: 2,
					dataPoints: [
						  { x: 10, y: parseFloat(result[1]), indexLabel: result[0] },
						  { x: 20, y: parseFloat(result[3]), indexLabel: result[2] },
						  { x: 30, y: parseFloat(result[5]), indexLabel: result[4]  }
					]
				}]
			});
			chart.render();
}

//window.onload = drawGraph(result.split(','));
//var data = {
//    size: 230,
//    sectors: [
//        {
//            percentage: 0.45,
//            label: 'Thing 1'
//        },
//        {
//            percentage: 0.21,
//            label: "Thing Two"
//        },
//        {
//            percentage: 0.11,
//            label: "Another Thing"
//        },
//        {
//            percentage: 0.23,
//            label: "Pineapple"
//        }
//    ]
//}
//function calculateSectors( data ) {
//    var sectors = [];
//    var colors = [
//        "#61C0BF", "#DA507A", "#BB3D49", "#DB4547"
//    ];
//
//    var l = data.size / 2
//    var a = 0 // Angle
//    var aRad = 0 // Angle in Rad
//    var z = 0 // Size z
//    var x = 0 // Side x
//    var y = 0 // Side y
//    var X = 0 // SVG X coordinate
//    var Y = 0 // SVG Y coordinate
//    var R = 0 // Rotation
//
//    data.sectors.map( function(item, key ) {
//        a = 360 * item.percentage;
//        aCalc = ( a > 180 ) ? 360 - a : a;
//        aRad = aCalc * Math.PI / 180;
//        z = Math.sqrt( 2*l*l - ( 2*l*l*Math.cos(aRad) ) );
//        if( aCalc <= 90 ) {
//            x = l*Math.sin(aRad);
//        }
//        else {
//            x = l*Math.sin((180 - aCalc) * Math.PI/180 );
//        }
//
//        y = Math.sqrt( z*z - x*x );
//        Y = y;
//
//        if( a <= 180 ) {
//            X = l + x;
//            arcSweep = 0;
//        }
//        else {
//            X = l - x;
//            arcSweep = 1;
//        }
//
//        sectors.push({
//            percentage: item.percentage,
//            label: item.label,
//            color: colors[key],
//            arcSweep: arcSweep,
//            L: l,
//            X: X,
//            Y: Y,
//            R: R
//        });
//
//        R = R + a;
//    })
//
//
//    return sectors
//}
//sectors = calculateSectors(data);
//var newSVG = document.createElementNS( "http://www.w3.org/2000/svg","svg" );
//newSVG.setAttributeNS(null, 'style', "width: "+data.size+"px; height: " + data.size+ "px");
//document.getElementsByTagName("body")[0].appendChild(newSVG)
//
//
//sectors.map( function(sector) {
//
//    var newSector = document.createElementNS( "http://www.w3.org/2000/svg","path" );
//    newSector.setAttributeNS(null, 'fill', sector.color);
//    newSector.setAttributeNS(null, 'd', 'M' + sector.L + ',' + sector.L + ' L' + sector.L + ',0 A' + sector.L + ',' + sector.L + ' 1 0,1 ' + sector.X + ', ' + sector.Y + ' z');
//    newSector.setAttributeNS(null, 'transform', 'rotate(' + sector.R + ', '+ sector.L+', '+ sector.L+')');
//
//    newSVG.appendChild(newSector);
//})
//
////var midCircle = document.createElementNS( "http://www.w3.org/2000/svg","circle" );
////midCircle.setAttributeNS(null, 'cx', data.size * 0.5 );
////midCircle.setAttributeNS(null, 'cy', data.size * 0.5);
////midCircle.setAttributeNS(null, 'r', data.size * 0.28 );
////midCircle.setAttributeNS(null, 'fill', '#42495B' );
//
//newSVG.appendChild(midCircle);


