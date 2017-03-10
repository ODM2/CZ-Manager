/**
 * Created by lsetiawan on 2/24/17.
 */
function AjaxRequest() {}

AjaxRequest.prototype.initRequest = function() {
    this.xhttp = new XMLHttpRequest();
};

AjaxRequest.prototype.sendAndLoad = function(url, callback) {
    this.xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
				var response = this.responseText;
				callback(response);
		}
	};
	this.xhttp.open("GET", url, true);
	this.xhttp.send();
};