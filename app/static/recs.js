function single() {
	myWindow=window.open("singlerec.html", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

function validate() {
	var x = document.forms["feedback"]["rating"].value;
	if (x == "") {
		alert("Please rate the suggestion to continue. Feedback will make your recommendations better!");
		return false;
	} else {
		window.close();
	}
}


