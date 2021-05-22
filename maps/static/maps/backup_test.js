window.onload = init;

function init() {
    var raster = new ol.layer.Tile({
        source: new ol.source.OSM(),
    });

    var source = new ol.source.Vector({
        wrapX: false
    });

    var vector = new ol.layer.Vector({
        source: source,
    });

    const map = new ol.Map({
    layers: [raster, vector],
    target: 'js-map',
    view: new ol.View({
        center: [12883683.599722689, -3725584.0232046843],
        zoom: 4,
        zoomFactor: 4,
        constrainRotation: 4,
        }),
    });

    var typeSelect = document.getElementById('type');

    var draw; // global so we can remove it later
    function addInteraction() {
        var value = typeSelect.value;
        if (value !== 'None') {
            draw = new ol.interaction.Draw({
            source: source,
            type: typeSelect.value,
            });
            map.addInteraction(draw);
        }
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

    // Set thumbnail interaction for images
    let image1 = false;
    let image2 = false;
    let image3 = false;
    let image4 = false;

    let image1File = null;
    let image2File = null;
    let image3File = null;
    let image4File = null;

    const formData = new FormData();

    // Cover Image
    const inputCover = document.getElementById("img-cover");
    const coverImage = document.getElementById("img-cover-picture");
    inputCover.addEventListener('change', function (e) {
        console.log(inputCover.files);
        const reader = new FileReader();
        reader.onload = function () {
            const img = new Image();
            img.src = reader.result;
            coverImage.src = img.src;
        }
        reader.readAsDataURL(inputCover.files[0]);
        image1 = true;
        image1File = inputCover.files[0];
        formData.append('image1', inputCover.files[0]);
    }, false)

    // Long Image
    const inputLong = document.getElementById("img-long");
    const longImage = document.getElementById("img-long-picture");
    inputLong.addEventListener('change', function (e) {
        console.log(inputLong.files);
        const reader = new FileReader();
        reader.onload = function () {
            const img = new Image();
            img.src = reader.result;
            longImage.src = img.src;
        }
        reader.readAsDataURL(inputLong.files[0]);
        image2 = true;
        image2File = inputLong.files[0];
        formData.append('image2', inputLong.files[0]);
    }, false)

    // Small Image 1
    const inputSmall1 = document.getElementById("img-small-1");
    const small1Image = document.getElementById("img-small-1-picture");
    inputSmall1.addEventListener('change', function (e) {
        console.log(inputSmall1.files);
        const reader = new FileReader();
        reader.onload = function () {
            const img = new Image();
            img.src = reader.result;
            small1Image.src = img.src;
        }
        reader.readAsDataURL(inputSmall1.files[0]);
        image3 = true;
        image3File = inputSmall1.files[0];
        formData.append('image3', inputSmall1.files[0]);
    }, false)

    // Small Image 2
    const inputSmall2 = document.getElementById("img-small-2");
    const small2Image = document.getElementById("img-small-2-picture");
    inputSmall2.addEventListener('change', function (e) {
        console.log(inputSmall2.files);
        const reader = new FileReader();
        reader.onload = function () {
            const img = new Image();
            img.src = reader.result;
            small2Image.src = img.src;
        }
        reader.readAsDataURL(inputSmall2.files[0]);
        image4 = true;
        image4File = inputSmall2.files[0];
        formData.append('image4', inputSmall2.files[0]);

        console.log("Sending the following form")
        for (var pair of formData.entries()) {
            console.log(pair);
        }
    }, false)

    

    /**
     * Add button interaction
     */

    save_button = document.getElementById('submit-button');

    save_button.addEventListener('click', function () {
        var writer = new ol.format.GeoJSON();
        var geojsonStr = writer.writeFeatures(vector.getSource().getFeatures(), {featureProjection: 'EPSG:3857'});

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');

        // Get images
        //
        //

        new_post_details = {
            "title": document.getElementById('title').value,
            "description": document.getElementById('description').value,
            "location": document.getElementById('location').value,
            "duration": document.getElementById('duration').value,
            "distance": document.getElementById('distance').value,
            "category": document.getElementById('category').value,
        };

        console.log("Found object of the following: ")
        console.log(new_post_details);

        // Error handling if no details input for form
        if (new_post_details["title"].length == 0 || 
            new_post_details["description"].length == 0 ||
            new_post_details["location"].length == 0 ||
            new_post_details["duration"].length == 0 ||
            new_post_details["distance"].length == 0 ||
            new_post_details["category"].length == 0
            ){
                // Display error on the screen
                alert('Please tell us more about your walk, make sure to fill out all the details!');
                return false
        };

        console.log("confirmed that lengths are not zero")

        // Error handling images
        if (image1 == false ||
            image2 == false ||
            image3 == false ||
            image4 == false
            ){
                // Display error on the screen
                alert('Please upload four images to show off your walk!');
                return false
        };

        //images_to_upload = {
        //    "image1": image1File,
        //    "image2": image2File,
        //    "image3": image3File,
        //    "image4": image4File
        //};

        console.log("confirmed that 4 images are uploaded")
      
        // Save the geoJSON
        fetch('./geojson', {
            method: 'PUT',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', 
                'X-CSRFToken': csrftoken,
            },
            body: 
                JSON.stringify({
                'geoJSON': geojsonStr,
                'map_details': new_post_details,
            }),
            
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 201){
                console.log(data.success)
                console.log(data.id);
                window.location.href = `/map/${data.id}`;
                return false;
            }
            if (data.status === 400){
                // Display error on the screen
                console.log("Error: No coordinates found.");
                alert("Please draw your walk on the map!");
                return false;
            }
            else {
                console.log(data.success)
                console.log(data.id)
                window.location.href = `/map/${data.id}`;
                return false;
            }
        })
        

        // Stop form from submitting
        return false;
    })

}