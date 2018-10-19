/**
 * Created by lsetiawan on 2/24/17.
 */
function MAP() {}

MAP.prototype.initMap = function (map_id, initCenter, initZoom, legends, cluster_feature_types, display_titles){
	this.map_id = map_id;
	this.initCenter = initCenter;
	this.initZoom = initZoom;
	this.markers = L.markerClusterGroup();
	this.cluster_feature_types = cluster_feature_types;
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

	this.webmap.on('popupopen', function (e) {
	    // console.log(e.popup);
        var acc = document.getElementsByClassName("accordion");
        var i;

        for (i = 0; i < acc.length; i++) {
          acc[i].onclick = function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight){
              panel.style.maxHeight = null;
            } else {
              panel.style.maxHeight = panel.scrollHeight + "px";
            }
          }
        }
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
MAP.prototype.getData = function (url,spinner) {
    _this = this;
    var Ajax = new AjaxRequest;
	var featureList = this.legends;
    var cluster_feature_types = this.cluster_feature_types;
    var style_class = '';
	var icon_str = '';
	var done = false;
	Ajax.initRequest();
    Ajax.sendAndLoad(url, function (response) {
        var samplingFeatures = JSON.parse(response);
        samplingFeatures.forEach(function (sf) {
			for (var i = 0; i < featureList.length; i++) {
				
				if(featureList[i]['feature_type'] ==  sf['sampling_feature_type']){
					style_class = featureList[i]['style_class'];

					icon_str =  featureList[i]['icon'];
				}
			}

			// For debugging
			// console.log(sf.featuregeometry);
			// console.log(sf.sampling_feature_type);
            var marker = _this.drawMarker(sf,style_class,icon_str);
            makeMarkerPopup(marker, sf);
            done = false;

            if(cluster_feature_types.includes(sf['sampling_feature_type'])){
                _this.markers.addLayer(marker);
                done=true
            }
            if(!done){
				marker.addTo(_this.webmap);
			}
        });
        _this.markers.addTo(_this.webmap);
        console.log('here');
		spinner.stop();
    })

};


createMarker = function (latlng, markerIcon, color, sfname,style_class,icon_str) {
	if(this.display_titles){
		var iconDiv = new L.DivIcon({
		className: style_class + ' awesome-marker leaflet-zoom-animated leaflet-interactive awesome-marker-labeled',
		html: '<i class="fa '+ icon_str +' icon-white" aria-hidden="true"></i><p ' +
        'style="background-color:rgba(255,255,255,0.8);width:75px;margin-top:25px;font-weight:bold;">'+sfname + '</p>'
		});
		marker = L.marker([latlng[0],latlng[1]], {
            icon: iconDiv,
            markerColor: color,
            prefix: 'fa',
            riseOnHover: true
		});
		return marker; 
	} else {
        return L.AwesomeMarkers.icon({
            icon: markerIcon,
            markerColor: color,
            prefix: 'fa'
        });
	}
};

MAP.prototype.drawMarker = function(obs,style_class,icon_str) {
    var latlng = [obs.featuregeometry.lat, obs.featuregeometry.lng];
    var featType = obs.sampling_feature_type;
    var sfname = obs.samplingfeaturecode;
    //console.log(obs);

    return this.getMarker(latlng, featType, sfname,style_class,icon_str);
};

MAP.prototype.getMarker = function (latlng, featType, sfname,style_class,icon_str) {
    var markerIcon = null;
    this.legends.forEach(function (l) {
        if (l.feature_type == featType){
            markerIcon = createMarker(latlng, l.icon, l.color, sfname,style_class,icon_str);
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
    if(this.display_titles){
		return markerIcon.bindTooltip(sfname, tooltipProps);
    } else {
        mark = L.marker(latlng, markerProps).bindTooltip(sfname, tooltipProps);
        return L.marker(latlng, markerProps).bindTooltip(sfname, tooltipProps);
    }
};


makerelation = function(relationobs) {
        var c = '<button class="accordion">Children</button>';
        var p = '<button class="accordion">Parent</button>';
        var s = '<button class="accordion">Siblings</button>';
        if (relationobs.children) {
            c = c + "<div class='panel'>" + "<p><ul>";
            relationobs.children.forEach(function (child) {
                c = c + "<li><a href='/" + url_path + "odm2admin/samplingfeatures/" +
                    child['samplingfeatureid__samplingfeatureid'] +
                    "/change/'>"+
                    child['samplingfeatureid__samplingfeaturecode'] +
                    "</a>, Link: <a target='_blank' href='" +
                    child['samplingfeatureexternalidentifieruri'] + "'>" +
                    child['samplingfeatureexternalidentifier'] +"</a></li>";
            });
            c = c + "</ul></p></div>";
        } else {
            c = c + "<div class='panel'><p>No Children</p></div>";
        }
        if (relationobs.parents) {
            p = p + "<div class='panel'>" + "<p><ul>";
            relationobs.parents.forEach(function (child) {
                p = p + "<li><a href='/" + url_path + "odm2admin/samplingfeatures/" +
                    child['samplingfeatureid__samplingfeatureid'] +
                    "/change/'>"+
                    child['samplingfeatureid__samplingfeaturecode'] +
                    "</a>, Link: <a target='_blank' href='" +
                    child['samplingfeatureexternalidentifieruri'] + "'>" +
                    child['samplingfeatureexternalidentifier'] +"</a></li>";
            });
            p = p + "</ul></p></div>";
        } else {
            p = p + "<div class='panel'><p>No Parent</p></div>";
        }
        if (relationobs.siblings) {
            s = s + "<div class='panel'>" + "<p><ul>";
            relationobs.siblings.forEach(function (child) {
                s = s + "<li><a href='/" + url_path + "odm2admin/samplingfeatures/" +
                    child['samplingfeatureid__samplingfeatureid'] +
                    "/change/'>"+
                    child['samplingfeatureid__samplingfeaturecode'] +
                    "</a>, Link: <a target='_blank' href='" +
                    child['samplingfeatureexternalidentifieruri'] + "'>" +
                    child['samplingfeatureexternalidentifier'] +"</a></li>";
            });
            s = s + "</ul></p></div>";
        } else {
            s = s + "<div class='panel'><p>No Siblings</p></div>";
        }

        return p + s + c;
    };

maketablecontent = function (obs) {
    var sfcode = '',
        sftype = '',
        sfcoords = '',
        sfdesc = '',
        sfigsn = '',
        sfsdr = '',
        sfrel = '',
        sitetype = '',
        sptype = '',
        spmed = '',
	sfelev = '';

    if (obs.samplingfeaturecode) {
        sfcode = "<tr>"
            + "<td class='title'>Sampling Feature Code</td>"
            + "<td><a href='" + obs.samplingfeatureurl + "'>" + obs.samplingfeaturecode + "</a></td>"
            + "</tr>";
    }
    if (obs.sampling_feature_type) {
        sftype = "<tr>"
            + "<td class='title'>Sampling Feature Type</td>"
            + "<td><a target='_blank' href='" + obs.samplingfeaturetypeurl + "'>" + obs.sampling_feature_type + "</a></td>"
            + "</tr>";
    }
    if (obs.featuregeometry) {
        sfcoords = "<tr>"
            + "<td class='title'>Coordinates</td>"
            + "<td>" + obs.featuregeometry.lat + ", " + obs.featuregeometry.lng
            + " (EPSG:<a target='_blank' href='http://epsg.io/" + obs.featuregeometry.crs + "'>"
            + obs.featuregeometry.crs + "</a>)</td>"
            + "</tr>";
    }
    if (obs.elevation_m) {
        sfelev = "<tr>"
            + "<td class='title'>Elevation</td>"
            + "<td>" + obs.elevation_m + " m</td>"
            + "</tr>";
    }
    if (obs.samplingfeaturedescription) {
        sfdesc = "<tr>"
            + "<td class='title'>Description</td>"
            + "<td>" + obs.samplingfeaturedescription + "</td>"
            + "</tr>";
    }
    if (obs.igsn && obs.igsnurl) {
        sfigsn = "<tr>"
            + "<td class='title'>IGSN</td>"
            + "<td><a target='_blank' href='" + obs.igsnurl + "'>" + obs.igsn + "</a></td>"
            + "</tr>";
    }
    if (obs.soil_top_depth && obs.soil_bottom_depth &&
        obs.soil_top_depth_units && obs.soil_bottom_depth_units) {
        sfsdr = "<tr>"
            + "<td class='title'>Soil Depth Range</td>"
            + "<td>" + obs.soil_top_depth + " " + obs.soil_top_depth_units + " - " +
            obs.soil_bottom_depth + " " + obs.soil_bottom_depth_units + "</td>"
            + "</tr>";
    }
    if (obs.relationships) {
        sfrel = makerelation(obs.relationships);
    }
    if (obs.sitetype) {
        sitetype = "<tr>"
            + "<td class='title'>Site Type</td>"
            + "<td><a target='_blank' href='" + obs.sitetypeurl + "'>" + obs.sitetype + "</a></td>"
            + "</tr>";
    }
    if (obs.specimentype) {
        sptype = "<tr>"
            + "<td class='title'>Specimen Type</td>"
            + "<td><a target='_blank' href='" + obs.specimentypeurl + "'>" + obs.specimentype + "</a></td>"
            + "</tr>";
    }
    if (obs.specimenmedium) {
        spmed = "<tr>"
            + "<td class='title'>Specimen Medium</td>"
            + "<td>" + obs.specimenmedium + "</td>"
            + "</tr>";
    }

    var tablecontent = sfcode + sftype + sitetype + sptype + spmed + sfcoords + sfelev + sfdesc + sfigsn + sfsdr;
    var relationshiptree = sfrel;
    return {
        'tablecontent': tablecontent,
        'relationshiptree': sfrel
    };
};

makeMarkerPopup = function (marker, obs) {
    // console.log(obs.relationships);
    var header = "<br><h2>"+ obs.samplingfeaturename + "</h2>"
            + "<hr />";
    var tablestart = "<table class='table table-bordered table-hover'>"
            + "<tbody>";

    var content = maketablecontent(obs);
    var tablecontent = content.tablecontent;
    var reltree = content.relationshiptree;


    var tableend = "</tbody>"
            + "</table>";

    var popup = tablestart + tablecontent + tableend + reltree;

    var api = 'mappopup';
    var link = null;
    if (obs.sampling_feature_type == "Site" || obs.sampling_feature_type == "Observation well" ||
        obs.sampling_feature_type == "Stream gage" || obs.sampling_feature_type == "Transect" ||
        obs.sampling_feature_type == "Weather station" || obs.sampling_feature_type == "Profile" ||
        obs.sampling_feature_type == "Specimen") {
        markerpopup = header + "<div style='height: 500px; overflow: scroll;'>" + popup
            + "<iframe width=600 height=400 "
            + "src='/" + url_path + api + "/samplingfeature=" + obs.samplingfeatureid
            + "/popup=true/' name='iframe_A'></iframe>" + "</div>";
    } else if (obs.sampling_feature_type == "Excavation") {
        api = 'profilegraph';

        link = "/" + url_path + api + "/samplingfeature=" + obs.samplingfeatureid
            + "/popup=true/";

        markerpopup = header + "<div style='height: 500px; overflow: scroll;'>"
            + popup
            + "<a  target='_blank' "
            + "href='" + link + "'> View soil profile data in new page</a>"
            + "<iframe width=600 height=400 "
            + "src='" + link + "' name='iframe_A'></iframe>" + "</div>";

    } else if (obs.sampling_feature_type == "Field area") {
        api = 'profilegraph';

        link = "/" + url_path + api + "/selectedrelatedfeature=" + obs.samplingfeatureid
            + "/popup=true/";

        markerpopup = header + "<div style='height: 500px; overflow: scroll;'>"
            + popup
            + "<a  target='_blank' "
            + "href='" + link + "'> View data for this field area in new page</a>"
            + "<iframe width=600 height=400 "
            + "src='" + link + "' name='iframe_A'></iframe>" + "</div>";
    } else {
        markerpopup = header
            + "<div style='height: 500px; overflow: scroll;'>"
            + popup + "</div>";
    }

	marker.bindPopup(markerpopup, {
	    maxWidth : 620
    });
    return markerpopup;
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