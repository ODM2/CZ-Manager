/**
 * Created by lsetiawan on 2/10/17.
 */

/* Display coords function */
function displayCoords(e){
    document.getElementById("lat").innerHTML = e.latlng['lat'].toFixed(4);
    document.getElementById('lng').innerHTML = e.latlng['lng'].toFixed(4);
}

/* Make Basemaps */
function makeBaseMaps(basemaps) {
    for (var i = 0; i < basemaps.length; i++) {
        if (basemaps[i]['name'] == 'MapBox_RunBikeHike') {
            baseMaps[basemaps[i]['name']] = L.tileLayer(basemaps[i]
                ['url'],basemaps[i]['options']).addTo(myMap);
        } else {
            baseMaps[basemaps[i]['name']] = L.tileLayer(basemaps[i]
                ['url'],basemaps[i]['options']);
        }
    }
}

/* Function for Ajax Request */
function AjaxRequest(url, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = this.responseText;
            callback(response);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

getSamplingFeatures = function (response) {
    console.log(JSON.parse(response));
    AjaxRequest('get_legend', getLegends);
};

getLegends = function (response) {
    var featureList = JSON.parse(response);
    console.log(featureList);
};

loadBaseMaps = function (response) {
    var base_maps = JSON.parse(response);
    // Create Base maps
    makeBaseMaps(base_maps);
};