window.onload = init;

function init() {

    state_selection = document.getElementById("state_choice");
    removeOptions(state_selection);

    var raster = new ol.layer.Tile({
        source: new ol.source.OSM(),
    });

    var source = new ol.source.Vector({
        wrapX: false
    });

    var vector = new ol.layer.Vector({
        source: source,
        style: new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.2)',
            }),
            stroke: new ol.style.Stroke({
                color: '#ffcc33',
                width: 2,
            }),
            image: new ol.style.Circle({
                radius: 7,
                fill: new ol.style.Fill({
                    color: '#ffcc33',
                }),
            }),
        }),
    });

    /**
     * Currently drawn feature.
     * @type {import("../src/ol/Feature.js").default}
     */
    var sketch;

    /**
     * The help tooltip element.
     * @type {HTMLElement}
     */
    var helpTooltipElement;

    /**
     * Overlay to show the help messages.
     * @type {Overlay}
     */
    var helpTooltip;

    /**
     * The measure tooltip element.
     * @type {HTMLElement}
     */
    var measureTooltipElement;

    /**
     * Overlay to show the measurement.
     * @type {Overlay}
     */
    var measureTooltip;

    /**
     * Message to show when the user is drawing a polygon.
     * @type {string}
     */
    var continuePolygonMsg = 'Click to continue drawing the polygon';

    /**
     * Message to show when the user is drawing a line.
     * @type {string}
     */
    var continueLineMsg = 'Click to continue drawing the line';

    /**
     * Handle pointer move.
     * @param {import("../src/ol/MapBrowserEvent").default} evt The event.
     */

    var pointerMoveHandler = function (evt) {
        if (evt.dragging) {
            return;
        }
        /** @type {string} */
        var helpMsg = 'Click to start drawing';
    
        if (sketch) {
            var geom = sketch.getGeometry();
            if (geom instanceof ol.geom.Polygon) {
                helpMsg = continuePolygonMsg;
            } else if (geom instanceof ol.geom.LineString) {
                helpMsg = continueLineMsg;
            }
        }
    
        helpTooltipElement.innerHTML = helpMsg;
        helpTooltip.setPosition(evt.coordinate);
    
        helpTooltipElement.classList.remove('hidden');
    };

    const map = new ol.Map({
    layers: [raster, vector],
    target: 'js-map',
    view: new ol.View({
        center: [0, 0],
        zoom: 0,
        zoomFactor: 4,
        constrainRotation: 4,
        }),
    });

    map.on('pointermove', pointerMoveHandler);

    map.getViewport().addEventListener('mouseout', function () {
        helpTooltipElement.classList.add('hidden');
    });

    var typeSelect = document.getElementById('type');

    var draw; // global so we can remove it later

    /**
    * Format length output.
    * @param {LineString} line The line.
    * @return {string} The formatted length.
    */
    var formatLength = function (line) {
        var length = ol.sphere.getLength(line);
        var output;
        if (length > 100) {
                output = Math.round((length / 1000) * 100) / 100 + ' ' + 'km';
            } else {
                output = Math.round(length * 100) / 100 + ' ' + 'm';
            }
            return output;
    };

    /**
    * Format area output.
    * @param {Polygon} polygon The polygon.
    * @return {string} Formatted area.
    */
    var formatArea = function (polygon) {
        var area = ol.sphere.getArea(polygon);
        var output;
        if (area > 10000) {
            output = Math.round((area / 1000000) * 100) / 100 + ' ' + 'km<sup>2</sup>';
        } else {
            output = Math.round(area * 100) / 100 + ' ' + 'm<sup>2</sup>';
        }
        return output;
    };

    var total_distance;
    var total_distance_final = 0;
    var unit = "";

    var property_value = 0;

    var feature = new ol.Feature({
        name: property_value,
    });

    feature.setProperties({'name':'test', 'description':'testing'});

    function addInteraction() {
        //var type = typeSelect.value == 'area' ? 'Polygon' : 'LineString';
        var type = typeSelect.value;
        draw = new ol.interaction.Draw({
            source: source,
            type: type,
            feature: feature,
            style: new ol.style.Style({
                fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.2)',
                }),
                stroke: new ol.style.Stroke({
                    color: 'rgba(0, 0, 0, 0.5)',
                    lineDash: [10, 10],
                    width: 2,
                }),
                image: new ol.style.Circle({
                    radius: 5,
                    stroke: new ol.style.Stroke({
                    color: 'rgba(0, 0, 0, 0.7)',
                    }),
                    fill: new ol.style.Fill({
                        color: 'rgba(255, 255, 255, 0.2)',
                    }),
                }),
                //text: new ol.style.Text({
                //    text: "Test text",
                //    scale: 1.2,
                //    fill: new ol.style.Fill({
                //        color: "#fff"
                //    }),
                //     stroke: new ol.style.Stroke({
                //        color: "0",
                //        width: 3
                //    })
                //})
            }),
        });

        draw.setProperties({'name':'abcd', 'description':'xyz'});
        
        map.addInteraction(draw);

        createMeasureTooltip();
        createHelpTooltip();

        var listener;
        draw.on('drawstart', function (evt) {
            // set sketch
            sketch = evt.feature;
    
            /** @type {import("../src/ol/coordinate.js").Coordinate|undefined} */
            var tooltipCoord = evt.coordinate;
    
            listener = sketch.getGeometry().on('change', function (evt) {
                var geom = evt.target;
                var output;
                if (geom instanceof ol.geom.Polygon) {
                    output = formatArea(geom);
                    tooltipCoord = geom.getInteriorPoint().getCoordinates();
                } else if (geom instanceof ol.geom.LineString) {
                    output = formatLength(geom);
                    tooltipCoord = geom.getLastCoordinate();
                }
                measureTooltipElement.innerHTML = output;
                total_distance = measureTooltipElement.innerHTML;
                measureTooltip.setPosition(tooltipCoord);
            });
        });

        draw.on('drawend', function () {
            measureTooltipElement.className = 'ol-tooltip ol-tooltip-static';
            measureTooltip.setOffset([0, -7]);
            // unset sketch
            sketch = null;
            // unset tooltip so that a new one can be created
            measureTooltipElement = null;
            createMeasureTooltip();
            ol.Observable.unByKey(listener);

            if (type === "LineString") {
                // get distance to save
                const NUMERIC_REGEXP = /[-]{0,1}[\d]*[.]{0,1}[\d]+/g;
                var distance_numbers = total_distance.match(NUMERIC_REGEXP);
                const UNIT_CHECK = /[a-zA-Z]+/g;
                unit = total_distance.match(UNIT_CHECK);
                console.log(distance_numbers[0]);
                console.log(unit[0]);
                if (unit[0] === "m") {
                    // convert to meters
                    total_distance_final = total_distance_final + (parseFloat(distance_numbers[0]) / 1000);
                } else {
                    total_distance_final = total_distance_final + parseFloat(distance_numbers[0]);
                }
                console.log("Updated total distance =");
                console.log(total_distance_final);
            }
        });
    }

    function createHelpTooltip() {
        if (helpTooltipElement) {
            helpTooltipElement.parentNode.removeChild(helpTooltipElement);
        }
        helpTooltipElement = document.createElement('div');
        helpTooltipElement.className = 'ol-tooltip hidden';
        helpTooltip = new ol.Overlay({
            element: helpTooltipElement,
            offset: [15, 0],
            positioning: 'center-left',
        });
        map.addOverlay(helpTooltip);
      }
      
    /**
    * Creates a new measure tooltip
    */
    function createMeasureTooltip() {
        if (measureTooltipElement) {
            measureTooltipElement.parentNode.removeChild(measureTooltipElement);
        }
        measureTooltipElement = document.createElement('div');
        measureTooltipElement.className = 'ol-tooltip ol-tooltip-measure';
        measureTooltip = new ol.Overlay({
            element: measureTooltipElement,
            offset: [0, -15],
            positioning: 'bottom-center',
        });
        map.addOverlay(measureTooltip);
    }
    
    /**
     * Handle change event.
     */
    typeSelect.onchange = function () {
        map.removeInteraction(draw);
        addInteraction();
    };

    document.getElementById('undo-button').addEventListener('click', function () {
        draw.removeLastPoint();
    });

    addInteraction();

    /**
    Control country and state drop down options that are selectable
    */ 

    country_selection = document.getElementById("country_choice");

    country_selection.addEventListener('change', function() {

        // remove any entries in the state selection dropdown box
        removeOptions(state_selection);

        country_name = this.options[this.selectedIndex].text;
        console.log(country_name)

        fetch(`/maps/${country_name}`)
        .then(response => response.json())
        .then(object => {
            console.log(object);
            state_names = object;
            
            length = state_names[0].length;
            for (i = 0; i < length; i++) {
                new_option = document.createElement('option');
                new_option.value = state_names[1][i];
                new_option.innerHTML = state_names[0][i];
                state_selection.append(new_option)
            }

        })
    }, false);

    /**
     Save map data before sending form
    */    

    const myForm = document.getElementById('map-form');

    myForm.addEventListener('submit', function (e) {

        // save the distance data
        if (total_distance_final >= 1) {
            // Show 1 decimal points for kilometers
            total_distance_final = total_distance_final.toFixed(1);
            console.log("recognised as 'km'");
            console.log("saved distance as:");
            console.log(total_distance_final);
        } else {
            // Show 3 decimal points for meters
            total_distance_final = total_distance_final.toFixed(3);
            console.log("recognised as 'm'");
            console.log("saved distance as:");
            console.log(total_distance_final);
        }
        const distance = document.getElementById('id_distance');
        distance.value = total_distance_final;

        // save the geoJSON data
        var writer = new ol.format.GeoJSON();
        var geojsonStr = writer.writeFeatures(vector.getSource().getFeatures(), {featureProjection: 'EPSG:3857'});
        const geoJSONField = document.getElementById('id_map_data');
        geoJSONField.value = geojsonStr;
        console.log(geojsonStr);

    })
}

function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
}
