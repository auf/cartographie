var AUF = {};

AUF.home = function(){
    return {
        init: function(){
            console.log("AUF.home.init()");
            this.searchForm();
            this.beautifulSelects(); 
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
                maxBounds: [[-85, -180], [85, 180]],
                attributionControl: false,
            }).setView([51.505, -15.09], 13);

            map.setView(new L.LatLng(34.0, 0.7), 2);

            var osmUrl='/static/tiles/{z}/{x}/{y}.png';
            var osm = new L.TileLayer(osmUrl, {
                attributionControl: false,
                minZoom: 2,
                maxZoom: 5
            });

            map.addLayer(osm);
            $.getJSON('/geojson/', function(data) {
                  L.geoJson(data, {
                    pointToLayer: function(feature, latlng) {
                        var marker =  L.marker(latlng);
                        marker.on('click', function(evt) {
                                window.location.href = feature.properties.url;
                        });
                        marker.on('mouseover', function(evt) {
                                evt.target.bindPopup(feature.properties.tooltip).openPopup();
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
        switch ($(this).attr('name')) {
        case "region":
            $("#id_pays").val("");
            $("#id_etablissement").val("");
            break;
        case "pays": 
            $("#id_etablissement").val("");

            if ($(this).val() != "") {
                $("#id_region").val("");
            }
            break;
        case "etablissement":
            $("#id_region").val("");

            if ($(this).val() != "") {
                $("#id_pays").val("");
            }
            break;
        }
        $("#recherche").submit();
    });

    if ($('#map').length) {
	AUF.home.initMap();
    }

});
