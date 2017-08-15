var images = 13;      	// number of images
var initWait = 1500; // ms before first change
var fadeWait = 3000; // ms between subsequent changes

var counter = parseInt(Math.random() * images);      


$("#slideshow_images").ready(
	function() {                
	var url = "url(\"images/slideshow/image" + counter + ".png\")";                
	$("#slideshow_images").css("background-image", url).fadeIn("slow");
	setTimeout("fadePicOut();", initWait);        }
); 

function fadePicIn() {                
	var url = "url(\"images/slideshow/image" + counter + ".png\")";                
	$("#slideshow_images").css("background-image", url).fadeIn("slow");
	setTimeout("fadePicOut();", fadeWait);        
}        
		
function fadePicOut() {                
	$("#slideshow_images").fadeOut("slow");                
	counter++;
	if (counter == images) counter = 0;
	setTimeout("fadePicIn();", 500);
}

function set_slideshow_display(item_display) {
	
	document.getElementById(item_display).style.display = "block";	
	
	if (item_display!="slideshow_content") {
		document.getElementById("slideshow_content").style.display = "none";
		document.getElementById("visualizations").className = "on";
	} else {
		document.getElementById("visualizations").className = "off";
	}
	
	if (item_display!="about_code_content") {
		document.getElementById("about_code_content").style.display = "none";
		document.getElementById("about_code").className = "on";
	} else {
		document.getElementById("about_code").className = "off";
	}
	
	if (item_display!="cite_us_content") {
		document.getElementById("cite_us_content").style.display = "none";
		document.getElementById("cite_us").className = "on";
	} else {
		document.getElementById("cite_us").className = "off";
	}
		
}


