// There are two different grids of images on the template index.html: gird and gridMobile
// This function detects the size of the user's screen and hides one grid accordingly
function hideShow() {
	if(window.innerWidth < 750) {
		document.getElementById("grid").style.visibility = "hidden";
	} else {
		document.getElementById("gridMobile").style.visibility = "hidden";
	}
}

// These functions open a pop-up window of fixed height for each of the spotlight sites

function spotMHP() {
	myWindow=window.open("MHP", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=650");
}

function spotCP() {
	myWindow=window.open("CP", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

function spotHG() {
	myWindow=window.open("HG", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

function spotCI() {
	myWindow=window.open("CI", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

function spotBH() {
	myWindow=window.open("BH", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600")
}

function spotLI() {
	myWindow=window.open("LI", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=100,left=300,width=800,height=600");
}

// This function is used for the close button on the pop-ups to close the pop-up when clicked
function winClose() {
	window.close();
}
