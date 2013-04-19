var AUF = {};

AUF.home = function(){
    return {
        init: function(){
            console.log("AUF.home.init()");
            this.searchForm();
            this.beautifulSelects(); 
            this.initMap();
        },

        initMap: function() {
          var getColor = function(f) {
              if (f) {
                  return 'blue';
              }
              return 'white';
          };


          var style = function(feature) {
            return {
                fillColor: getColor(feature.properties.formations),
                weight: 2,
                opacity: 0,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.1 
            };
          };
            var map = L.map('map', {
                maxBounds: [[-85, -180], [85, 180]]
            }).setView([51.505, -15.09], 13);
            map.setView(new L.LatLng(41.3, 0.7),3);
            var osmUrl='/static/tiles/{z}/{x}/{y}.png';
            var osm = new L.TileLayer(osmUrl, {
                minZoom: 2,
                maxZoom: 4,
            });

            map.addLayer(osm);
            $.getJSON('/geojson/', function(data) {
                  L.geoJson(data, {
                    pointToLayer: function(feature, latlng) {
                        var marker =  L.circleMarker(latlng, {radius: 8, color: 'black' });
                        console.log(feature);
                        marker.on('mouseover', function(evt) {
                                evt.target.bindPopup(feature.properties.tooltip).openPopup();
                        });

                        marker.on('click', function(evt) {
                                console.log('click!');
                        });
                        return marker;
                   }}).addTo(map);
            });
        },

        beautifulSelects : function(){
            /*  
                Utilisation de chosen pour augmenter l'utilisabilité
                des SELECT à choix unique et multiple
             */
            console.log("AUF.formation.beautifulSelects()");

            if (typeof $.fn.chosen !== "undefined") {
                $(".form-auf select").chosen({
                    placeholder_text_multiple: "Veuillez choisir une ou plusieurs options"                             
                });
            }
        },


        searchForm: function(){
            console.log("AUF.home.searchForm()");

            $(".actions .btn").click(function(){
                $(this).parents("form").submit();
                return false;
            });
        }
    };
}();

$(document).ready(function(){
    AUF.home.init();

    $("#recherche select").change(function() {
        $("#recherche").submit();
    });
});
