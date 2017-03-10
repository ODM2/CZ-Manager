/**
 * Created by lsetiawan on 2/10/17.
 */

/* Initalize map */
var mapOptions = {
    worldCopyJump:true
};
var myMap = L.map('map',mapOptions).setView(mapCenter, initZoom);
myMap.on({mousemove: displayCoords});
// myMap.attributionControl.setPrefix(''); // Turn off Leaflet attribution


/* Load Initial BaseMap */
makeBaseMaps(base_maps);

var markerClusters = L.markerClusterGroup(singleMarkerMode=true); //,maxClusterRadius=1

for (var i=0; i < features.length; i++) {
    var feat_obj = featureList.filter(
    function( obj ){
        return obj['feature_type'] == features[i]['sampling_feature_type']
    });
}

// // Initialize marker cluster groupings
// var markerClusters = L.markerClusterGroup(
//         singleMarkerMode=true
// ); //,maxClusterRadius=1
// {% for site in features|filter_coords %}
//     var feat_obj = featureList.filter(
//             function( obj ){
//                 return obj['feature_type'] == '{{ site.sampling_feature_type.name }}'
//             });
//     var popup = '';
//     done = false;
//     {% for externalidentifier in externalidentifiers %}
//         {% if  site.sampling_feature_type.name == "Site" and site.samplingfeatureid == externalidentifier.samplingfeatureid.samplingfeatureid and externalidentifier.externalidentifiersystemid.externalidentifiersystemname == "NSF" %}
//          popup = '<br><h2>CZO: <a href="{{ externalidentifier.samplingfeatureexternalidentifieruri }}">{{ site.samplingfeaturename }}</a></h2>'
//                 + '<hr />'
//                 + '<br> <iframe  width=600, height=600, src="{{prefixpath}}../mappopup/samplingfeature&#61;{{site.samplingfeatureid}}/popup=true" name="iframe_A"></iframe></p>';
//                 done= true;
//                 {% endif %}
//     {% endfor %}
//     if (done == false){
//         {% if not done == 1 and site.sampling_feature_type.name == "Site" or site.sampling_feature_type.name == "Observation well" or site.sampling_feature_type.name == "Stream gage" or site.sampling_feature_type.name == "Transect" or site.sampling_feature_type.name == "Weather station" %}
//                  popup = '<br><h2>Sampling Feature: {{ site.samplingfeaturename }}</h2>'
//                     + '<hr />'
//                     + '<p>Sampling Feature Code: {{ site.samplingfeaturecode }}'
//                     + '<br>Sampling Feature Type: {{ site.sampling_feature_type.name }}'
//                     + '<br>Coordinates: [{{ site.featuregeometry|get_lat_lng:'lat' }},{{ site.featuregeometry|get_lat_lng:'lon' }}]'
//                     + '<br> {{ site.sampling_feature_type.name}}'
//                     + '<br> </p><iframe  width=600, height=600, src="{{prefixpath}}../mappopup/samplingfeature&#61;{{site.samplingfeatureid}}/popup=true" name="iframe_A"></iframe></p>';
//         {% elif  site.sampling_feature_type.name == "Excavation" %}
//             popup = '<br><h2>Sampling Feature: {{ site.samplingfeaturename }}</h2>'
//                     + '<hr />'
//                     + '<p>Sampling Feature Code: {{ site.samplingfeaturecode }}'
//                     + '<br>Sampling Feature Type: {{ site.sampling_feature_type.name }}'
//                     + '<br>Coordinates: [{{ site.featuregeometry|get_lat_lng:'lat' }},{{ site.featuregeometry|get_lat_lng:'lon' }}]'
//                     + '<br> {{ site.sampling_feature_type.name}}'
//                     + '<br><a  target="_blank" href="{{prefixpath}}../profilegraph/samplingfeature&#61;{{site.samplingfeatureid}}/popup=true"> View soil profile data in new page</a></p><iframe  width=600, height=500, src="{{prefixpath}}../profilegraph/samplingfeature&#61;{{site.samplingfeatureid}}/popup=true" name="iframe_A"></iframe></p>';
//         {% elif  site.sampling_feature_type.name == "Field area" %}
//             popup = '<br><h2>Sampling Feature: {{ site.samplingfeaturename }}</h2>'
//                     + '<hr />'
//                     + '<p>Sampling Feature Code: {{ site.samplingfeaturecode }}'
//                     + '<br>Sampling Feature Type: {{ site.sampling_feature_type.name }}'
//                     + '<br>Coordinates: [{{ site.featuregeometry|get_lat_lng:'lat' }},{{ site.featuregeometry|get_lat_lng:'lon' }}]'
//                     + '<br> {{ site.sampling_feature_type.name}}'
//                     + '<br><a  target="_blank" href="{{prefixpath}}../profilegraph/selectedrelatedfeature&#61;{{site.samplingfeatureid}}/popup=true"> View data for this field area in new page</a></p><iframe  width=600, height=500, src="{{prefixpath}}../profilegraph/selectedrelatedfeature&#61;{{site.samplingfeatureid}}/popup=true" name="iframe_A"></iframe></p>';
//         {% else %}
//             popup = '<br><h2>Sampling Feature: {{ site.samplingfeaturename }}</h2>'
//                     + '<hr />'
//                     + '<p>Sampling Feature Code: {{ site.samplingfeaturecode }}'
//                     + '<br>Sampling Feature Type: {{ site.sampling_feature_type.name }}'
//                     + '<br>Coordinates: [{{ site.featuregeometry|get_lat_lng:'lat' }},{{ site.featuregeometry|get_lat_lng:'lon' }}]</p>';
//         {% endif %}
//     }
//     if (done ==true){
//     var iconDiv = new L.DivIcon({
//         className: 'awesome-marker-icon-purple awesome-marker leaflet-zoom-animated leaflet-interactive',
//         html: '<i class="fa fa fa-flag-o icon-white" aria-hidden="true"></i><p style="margin-top:20px;font-weight:bold;">{{ site.samplingfeaturecode }}</p>'
//     });
//     }else{
//      var iconDiv = new L.DivIcon({
//         className: feat_obj[0].style_class + ' awesome-marker leaflet-zoom-animated leaflet-interactive',
//         html: '<i class="fa '+  feat_obj[0].icon +' icon-white" aria-hidden="true"></i><p style="margin-top:20px;font-weight:bold;">{{ site.samplingfeaturecode }}</p>'
//     });
//     }
//     {% if  site.sampling_feature_type.name == "Site" or site.sampling_feature_type.name == "Observation well" or site.sampling_feature_type.name == "Field area" or site.sampling_feature_type.name == "Stream gage" or site.sampling_feature_type.name == "Transect" or site.sampling_feature_type.name == "Weather station"  %}
//         m = L.marker([{{ site.featuregeometry|get_lat_lng:'lat' }}, {{ site.featuregeometry|get_lat_lng:'lon' }}], {
//             icon: iconDiv, title: '{{ site.samplingfeaturename }}'
//         }).bindPopup( popup,{minWidth: 600, minHeight: 500,autoPanPadding: [10, 50],  autoPan: true, closeButton: true,offset: [0, 5]} );
//         {% if map_config.cluster_sites and  site.sampling_feature_type.name == "Site" %}
//             markerClusters.addLayer(m);
//         {% else %}
//             m.addTo(myMap);
//         {% endif %}
//     {% else %}
//         m = L.marker([{{ site.featuregeometry|get_lat_lng:'lat' }}, {{ site.featuregeometry|get_lat_lng:'lon' }}], {
//             icon: iconDiv, title: '{{ site.samplingfeaturename }}'
//         }).bindPopup( popup,{minWidth: 600, minHeight: 500, autoPanPadding: [10, 50], autoPan: true, closeButton: true,offset: [0, 5]} );
//         markerClusters.addLayer(m);
//     {% endif %}
// {% endfor %}
//
//
// // Make legend
// var legend = L.control({
//     position: 'bottomright'
// });
// legend.onAdd = function (myMap) {
//     var div = L.DomUtil.create('div', 'info legend');
//     div.innerHTML += '<h2>Sample Feature Types</h2>';
//     // loop through our density intervals and generate a label with a colored square for each interval
//     for (var i = 0; i < featureList.length; i++) {
//         div.innerHTML +=
//                 '<div class="legend-item">' +
//                 '      <div class="legend-icon ' + featureList[i]['style_class'] + '">' +
//                 '           <i class="fa ' + featureList[i]['icon'] + '" aria-hidden="true"></i>' +
//                 '      </div>' +
//                 '      <div class="legend-text">' + featureList[i]['feature_type'] + '</div>' +
//                 '</div>'
//     }
//         return div;
// };
//
//
// // https://github.com/mikeskaug/Leaflet.Legend
// var legend2 = new L.Control.Legend({
//                 position: 'topleft',
//                 collapsed: true,
//                 controlButton: {
//                     title: "Legend"
//                 }});
// myMap.addControl( legend2 );
//
// $(".legend-container").append( $("#legend") );
// $(".legend-toggle").append( "<i class='legend-toggle-icon fa fa-filter fa-2x' style='color: #000;margin-left:5px;'></i>" );
//
// //legend2.addTo(myMap);
// legend.addTo(myMap);
// // Basemaps Choices
//
// myMap.addLayer(markerClusters);
//
// // Overlay Choices
// overlayMaps = {};
// // Put Control on map
// L.control.groupedLayers(baseMaps, overlayMaps).addTo(myMap);
// L.control.scale({
//     position:'bottomleft'
// }).addTo(myMap);
