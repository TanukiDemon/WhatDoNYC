function hideShow() {
	if(window.innerWidth < 750) {
		document.getElementById("grid").style.visibility = "hidden";
	} else {
		document.getElementById("gridMobile").style.visibility = "hidden";
	}
}

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

function winClose() {
	window.close();
}
