// Asynchronous HTTP GET request for "theUrl" parameter provided to the function
function httpGetAsync(theUrl, callback) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200)
			callback(xmlHttp.responseText);
	}
	xmlHttp.open("GET", theUrl, true);
	xmlHttp.send(null);
}

// Empty callback function utilized by httpGetAsync function
// This is empty because we do not want to execute any JavaScript code after the GET request
function mycallback(data) {}

// getFeedback is called when a user clicks on the thumbs up or thumbs down icon below a recommendation to rate it
// The function creates a url by concatenating elements of the url with the rating and placeId values with which the function was called
// It then calls the httpGetAsync function to issue an HTTP GET request for the url
// The url is for the /feedback route in views.py which adds a relationship for the rating provided by the use between the user's node 
//   and the node of the activity/venue that was recommended in Neo4j
function getFeedback(rating, placeId) {
	url = "/feedback?rating=" + rating + "&placeId=" + placeId;
	httpGetAsync(url, mycallback);
}
      
function logout() {
	url = "/logout";
	httpGetAsync(url, mycallback);
}

// Creates pop-up window when user clicks on recommendation
function singleRec(placeId) {
	myWindow = window.open("singleRec?pid=" + placeId, "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

// This function is used for the close button on the pop-ups to close the pop-up when clicked
function winClose() {
	window.close();
}

