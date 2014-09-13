function getRouteColor(score) {
	
	// Green to red and into maroon
	 return parseInt(score) == 100 ? '#00FF00' : 
		 	parseInt(score >  90  ? '#80FF00' :
			parseInt(score >  80  ? '#FFFF00' :
			parseInt(score >  70  ? '#FF8000' :
			parseInt(score >  60  ? '#FF0000' :
			parseInt(score >  50  ? '#CC0000' :
									'#990000';
			
	/*
	 * 
	return score == 100 ? '#252525' :
		   score > 95 	? '#800026' :
		   score > 90 	? '#bd0026' :
		   score > 85 	? '#e31a1c' :
		   score > 80 	? '#fc4e2a' :
		   score > 75 	? '#fd8d3c' :
		   score > 70 	? '#feb24c' :
	       score > 60 	? '#fed976' :
	       score > 50 	? '#ffeda0' :
			              '#ffffcc';
	*/
	}


function getRouteStyle(feature) {
	return {
        fillColor: getRouteColor(feature.properties.score),
        weight: 5,
        opacity: 0.5
        };
}
