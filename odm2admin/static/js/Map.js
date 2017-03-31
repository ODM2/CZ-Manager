/**
 * Created by lsetiawan on 2/24/17.
 */
function MAP() {}

MAP.prototype.initMap = function (map_id, initCenter, initZoom, legends, display_titles){
	this.map_id = map_id;
	this.initCenter = initCenter;
	this.initZoom = initZoom;
	this.markers = L.markerClusterGroup();
	this.basemaps = {};
	this.legends = legends;
	this.display_titles = display_titles;



	var mapOptions = {
	    center: this.initCenter,
		zoom: this.initZoom,
		scrollWheelZoom: false,
		worldCopyJump: true,
        zoomControl: false
	};

	this.webmap = L.map(map_id, mapOptions);

	this.zoomControl = L.control.zoom({position: 'topleft'}).addTo(this.webmap);

	this.scale = L.control.scale().addTo(this.webmap);

	this.webmap.on({
        mousemove: displayCoords
    });

	this.makeLegend(legends);

};

MAP.prototype.addBaseMap = function(basemaps) {
    _this = this;
    basemaps.forEach(function(basemap){_this.makeBaseMap(basemap)});

	L.control.layers(this.basemaps).addTo(this.webmap);
};

MAP.prototype.makeBaseMap = function (basemap) {
    if (basemap.name == 'MapBox_RunBikeHike'){
        this.basemaps[basemap.name] = L.tileLayer(basemap.url,basemap.options).addTo(this.webmap);
    } else {
        this.basemaps[basemap.name] = L.tileLayer(basemap.url,basemap.options)
    }
};

makeURL = function (parameters) {
    var baseurl = '/' + url_path +'features';
    var params_arr = [];
    params_arr.push('type=' + parameters.type);
    params_arr.push('datasets=' + parameters.datasets);

    var params = params_arr.join('&');
    return baseurl + '/' + params;
};

MAP.prototype.getData = function (url) {
    _this = this;
    var Ajax = new AjaxRequest;
	var featureList = this.legends;
	console.log(featureList);
    var style_class = '';
	Ajax.initRequest();
    Ajax.sendAndLoad(url, function (response) {
        var samplingFeatures = JSON.parse(response);
        samplingFeatures.forEach(function (sf) {
			for (var i = 0; i < featureList.length; i++) {
				console.log(featureList['feature_type']);
				if(featureList[i]['feature_type'] ==  sf['sampling_feature_type']){
					style_class = featureList[i]['style_class'];
				}
			}
			console.log(sf['sampling_feature_type']);
            var marker = _this.drawMarker(sf,style_class);
            makeMarkerPopup(marker, sf);
            if(!clustersites && sf['sampling_feature_type'] == 'Site'){
                marker.addTo(_this.webmap);
            } else {
                _this.markers.addLayer(marker);
            }
        });
        _this.markers.addTo(_this.webmap);
    })
};

createMarker = function (markerIcon, color, sfname,style_class) {
    if(this.display_titles){
			var iconDiv = new L.DivIcon({
			className: style_class + ' awesome-marker leaflet-zoom-animated leaflet-interactive',
			html: '<i class="fa fa fa-flag-o icon-white" aria-hidden="true"></i><p style="margin-top:20px;font-weight:bold;">'+sfname + '</p>'
            });
		return L.AwesomeMarkers.icon({
        icon: iconDiv,
        markerColor: color,
        prefix: 'fa'
    });
	}else{
	return L.AwesomeMarkers.icon({
        icon: markerIcon,
        markerColor: color,
        prefix: 'fa'
    });
	}
};

MAP.prototype.drawMarker = function(obs,style_class) {
    var latlng = [obs.featuregeometry.lat, obs.featuregeometry.lng];
    var featType = obs.sampling_feature_type;
    var sfname = obs.samplingfeaturecode;
    //console.log(obs);

    return this.getMarker(latlng, featType, sfname,style_class);
};

MAP.prototype.getMarker = function (latlng, featType, sfname,style_class) {
    var markerIcon = null;
    this.legends.forEach(function (l) {
        if (l.feature_type == featType){
            markerIcon = createMarker(l.icon, l.color, sfname,style_class);
			
		}
    });

    var markerProps = {
        icon: markerIcon
    };

    var tooltipProps = {
        interactive: true,
        offset: L.point(15, -25),
        direction: 'right'
    };

    return L.marker(latlng, markerProps).bindTooltip(sfname, tooltipProps);
};

makeMarkerPopup = function (marker, obs) {
    var popup = "<br><h2>"+ obs.samplingfeaturename + "</h2>"
            + "<hr />"
            + "<table class='table table-bordered table-hover'>"
            + "<tbody>"
            + "<tr>"
            + "<td class='title'>Sampling Feature Code</td>"
            + "<td>" + obs.samplingfeaturecode + "</td>"
            + "</tr>"
            + "<tr>"
            + "<td class='title'>Sampling Feature Type</td>"
            + "<td>" + obs.sampling_feature_type + "</td>"
            + "</tr>"
            + "<tr>"
            + "<td class='title'>Coordinates</td>"
            + "<td>" + obs.featuregeometry.lat + ", " + obs.featuregeometry.lng + "</td>"
            + "</tr>"
            + "<tr>"
            + "<td class='title'>Description</td>"
            + "<td>" + obs.samplingfeaturedescription + "</td>"
            + "</tr>"
            + "</tbody>"
            + "</table>";
    var api = 'mappopup';
    var link = null;
    if (obs.sampling_feature_type == "Site" || obs.sampling_feature_type == "Observation well" ||
        obs.sampling_feature_type == "Stream gage" || obs.sampling_feature_type == "Transect" ||
        obs.sampling_feature_type == "Weather station") {
        markerpopup = popup
            + "<iframe width=900, height=300px, "
            + "src='/" + url_path + api + "/samplingfeature=" + obs.samplingfeatureid
            + "/popup=true/' name='iframe_A'></iframe>";
    } else if (obs.sampling_feature_type == "Excavation") {
        api = 'profilegraph';

        link = "/" + url_path + api + "/samplingfeature=" + obs.samplingfeatureid
            + "/popup=true/";

        markerpopup = popup
            + "<a  target='_blank' "
            + "href='" + link + "'> View soil profile data in new page</a>"
            + "<iframe width=900, height=300px, "
            + "src='" + link + "' name='iframe_A'></iframe>";

    } else if (obs.sampling_feature_type == "Field area") {
        api = 'profilegraph';

        link = "/" + url_path + api + "/selectedrelatedfeature=" + obs.samplingfeatureid
            + "/popup=true/";

        markerpopup = popup
            + "<a  target='_blank' "
            + "href='" + link + "'> View data for this field area in new page</a>"
            + "<iframe width=900, height=300px, "
            + "src='" + link + "' name='iframe_A'></iframe>";
    } else {
        markerpopup = popup;
    }

	marker.bindPopup(markerpopup, {
	    maxWidth : 900
    });
};

MAP.prototype.makeFilter = function () {
    var filterlegend = new L.Control.Legend({
                        position: 'topleft',
                        controlButton: {
                            title: "Filter"
                        }});
    this.webmap.addControl( filterlegend );

    $(".legend-container").append( $("#dataset-filter") );
    $(".legend-toggle").append( "<i class='legend-toggle-icon fa fa-filter fa-2x' style='color: #000;margin-left:5px;'></i>" );
};


MAP.prototype.makeLegend = function (featureList) {
    // Make legend
    var legend = this.legend = L.control({
        position: 'bottomright'
    });
    legend.onAdd = function () {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += '<h2>Sample Feature Types <div id="minimize-toggle"><i ' +
            'class="fa fa-minus" aria-hidden="true"></i></div></h2>' + '<div id="box"></div>';
        // loop through our density intervals and generate a label with a colored square for each interval

        return div;
    };

    legend.addTo(this.webmap);

    var box = L.DomUtil.get("box");
    for (var i = 0; i < featureList.length; i++) {
        box.innerHTML +=
                '<div class="legend-item">' +
                '      <div class="legend-icon ' + featureList[i]['style_class'] + '">' +
                '           <i class="fa ' + featureList[i]['icon'] + '" aria-hidden="true"></i>' +
                '      </div>' +
                '      <div class="legend-text">' + featureList[i]['feature_type'] + '</div>' +
                '</div>'
    }

    $("#minimize-toggle").click(function(){
    if($(this).html() == '<i class="fa fa-minus" aria-hidden="true"></i>'){
        $(this).html(' <i class="fa fa-plus" aria-hidden="true"></i>');
    }
    else{
        $(this).html('<i class="fa fa-minus" aria-hidden="true"></i>');
    }
    $("#box").slideToggle();
    });

};

MAP.prototype.getUrl = function (filterByDataset, filterBySFType) {
    var url = null;

    if (filterByDataset.join(',')){
        url = makeURL({
            type: "filtered",
            datasets: filterByDataset.join(',')
        });
    }

    if (filterBySFType.join(',')){
        url = makeURL({
            type: filterBySFType.join(','),
            datasets: "filtered"
        });

    }

    if (!filterByDataset.join(',') && !filterBySFType.join(',')){
        url = makeURL({
            type: "all",
            datasets: "all"
        });
    }

    return url
};


displayCoords = function (e){
	document.getElementById("lat").innerHTML = e.latlng['lat'].toFixed(4);
	document.getElementById('lng').innerHTML = e.latlng['lng'].toFixed(4);
};