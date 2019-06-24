<script>
console.log('what model?');
//$('#samplingfeatures_form').bind('submit', function (e) {



//console.log(document.getElementsByClassName('submit-row'))

//var submitels = document.getElementsByClassName('submit-row');
//console.log('loop throuth submit');
//console.log(submitels);
//console.log(submitels.length);
//for (let item of submitels) {
//    console.log(item.id);
//    item.type = "button";
//};
//console.log('here');

window.onclick = function(e) {
   console.log('on click');
   console.log(e.target.parentNode);

   if(e.target.localName=='a'){
                e.preventDefault();
                myMap.openSidebar();
                window.globalurl = e.target.href; //window.location.protocol + "//" + window.location.host +path;
                url = window.globalurl + " #content";
                //console.log('load divs');
                $( "#insidebar" ).load(url); //odm2admin_content document.getElementById("sidebar")

                var url = '{% static "js/samplingfeaturesmap.js" %}';
                //console.log(url);
                $( "#jsholder" ).load(url); //odm2admin_content document.getElementById("sidebar")
                //console.log('loaded');

                };


   if(e.target.parentNode.classList[0]=='submit-row'){
     e.preventDefault();
     console.log('stopped');
     var submitels = document.getElementsByClassName('submit-row');
     console.log(document.getElementsByClassName('submit-row'));
     for (let item of submitels) {
         //console.log('change to button');
         //console.log(item.id);
         item.type = "button";
     };
     var frm = $('#samplingfeatures_form');
     //console.log('submit');

     //var ref = globalurl;
     //console.log(globalurl);
     frmserial = frm.serialize();
     //console.log(frmserial);
     //frmserial['url'] =globalurl;
     //console.log(frm.attr('method'));
     $.ajax({
         type: frm.attr('method'),
         url: window.prefixpath + "../save_sf/",
         data: frmserial,
         success: function (data) {
                var url = window.globalurl; //data.url; //window.location.protocol + "//" + window.location.host +path;
                url += " #content";
                //console.log(url);
                $( "#insidebar" ).load(url);
             //console.log('success');
         },
         error: function(data) {
             $("#insidebar").html("Something went wrong!");
             //console.log('error');
         }
     });
    //return false;
};
};
</script>