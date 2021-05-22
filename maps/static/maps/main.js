window.onload = init;

function init() {

    // Prepare starting coordinates for inital map zoom to center on
    starting_location_1 = document.getElementById('js-map').dataset.mapStart1;
    starting_location_2 = document.getElementById('js-map').dataset.mapStart2;
    starting_coordinates = [starting_location_1, starting_location_2];
    var conv_coordinates = ol.proj.transform(starting_coordinates,'EPSG:4326','EPSG:3857');

    const view = new ol.View({
        center: conv_coordinates,
        zoom: 7.5,
        zoomFactor: 4,
        constrainRotation: 4,
        maxZoom: 10
    });

    const map = new ol.Map({
        view: view,
        target: 'js-map'
    });

    map.on('click', function(e){
        //console.log(e.coordinate);
    });

    // Basemap Layers
    const openStreetMapStandard = new ol.layer.Tile({
        source: new ol.source.OSM(),
        visible: false,
        title: 'OSMStandard'
    })

    const stamenToner = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'http://tile.stamen.com/toner/{z}/{x}/{y}.png',
            attributions: 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
        }),
        visible: true,
        title: 'StamenToner'
    })

    // Layer Group
    const baseLayerGroup = new ol.layer.Group({
        layers: [
            openStreetMapStandard, stamenToner
        ]
    })
    map.addLayer(baseLayerGroup);

    // Vector Layers
    const fillStyle = new ol.style.Fill({
        color: [0, 166, 255, 1]  
    })

    const strokeStyle = new ol.style.Stroke({
        color: [0, 166, 255, 1],
        width: 5
    })

    const circleStyle = new ol.style.Circle({
        fill: new ol.style.Fill({
            color: [0, 166, 255, 1]
        }),
        radius: 10,
        stroke: strokeStyle
    })

    map_id = document.getElementById('js-map').dataset.mapId
    console.log("Found map id of...")
    console.log(map_id)

    const textStyle = new ol.style.Text({
        font: '20px Calibri,sans-serif',
        overflow: true,
        fill: new ol.style.Fill({
            color: '#000'
        }),
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
        })
    })

    var style = new ol.style.Style({
        fill: fillStyle,
        stroke: strokeStyle,
        image: circleStyle,
        text: textStyle,
    })

    // fetch geoJSON from url and read the features as source
    fetch(`/geojson/${map_id}`)
    .then(response => response.json())
    .then(object => {
        console.log(object);
        geojsonObject = object;

        // Set new vector layer
        const JSONFile = new ol.layer.VectorImage({
            source: new ol.source.Vector({
                features: new ol.format.GeoJSON().readFeatures(geojsonObject, { featureProjection: "EPSG:3857", dataProjection: 'EPSG:4326' })
            }),
            visible: true,
            title: "Test Vectors",
            style: function(feature) {
                style.getText().setText(feature.get('name'));
                return style;
            }
            //
            // working
            //
            //style: new ol.style.Style({
            //    fill: fillStyle,
            //    stroke: strokeStyle,
            //    image: circleStyle,
            //    text: textStyle,
            //}),
            //
            // working
            //
        })

        map.addLayer(JSONFile);
    })

    // TESTING INTEGRATION OF GEOPOSITIONING

    // view.getProjection may offer trouble

    var geolocation = new ol.Geolocation({
        // enableHighAccuracy must be set to true to have the heading value.
        trackingOptions: {
            enableHighAccuracy: true,
        },
        projection: view.getProjection(),
    });

    track = document.getElementById('track');

    track.addEventListener('change', function () {
        geolocation.setTracking(this.checked);
    })

    // handle geolocation error.
    geolocation.on('error', function (error) {
        var info = document.getElementById('info');
        info.innerHTML = error.message;
        info.style.display = '';
    });

    var accuracyFeature = new ol.Feature();
    geolocation.on('change:accuracyGeometry', function () {
        accuracyFeature.setGeometry(geolocation.getAccuracyGeometry());
    });

    var positionFeature = new ol.Feature();
    positionFeature.setStyle(
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: 6,
                fill: new ol.style.Fill({
                    color: '#3399CC',
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 2,
                }),
            }),
        })
    );

    geolocation.on('change:position', function () {
        var coordinates = geolocation.getPosition();
        positionFeature.setGeometry(coordinates ? new ol.geom.Point(coordinates) : null);
    });

    new ol.layer.Vector({
        map:map,
        source: new ol.source.Vector({
            features: [accuracyFeature, positionFeature],
        })
    })

}