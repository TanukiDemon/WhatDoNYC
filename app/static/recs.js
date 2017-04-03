function validate() {
	var x = document.forms["feedback"]["rating"].value;
	if (x == "") {
		alert("Please rate the suggestion to continue.");
		return false;
	} else {
		window.close();
	}
}
