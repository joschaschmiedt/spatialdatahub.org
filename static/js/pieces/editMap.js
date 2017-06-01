'use strict';

// nominatim stuff

// (1) hide and show nominatim stuff (do this after I've gotten it working)
var findPlaceButton = document.getElementById('find_place_button');
var findPlaceContainer = document.getElementById('find_place_container');

findPlaceButton.addEventListener('click', function showPlaceContainer() {
  classToggle(findPlaceButton, 'active');

  findPlaceContainer.style.display === 'none' || findPlaceContainer.style.display === '' ? findPlaceContainer.style.display = 'block' : findPlaceContainer.style.display = 'none';
});

// (2) get elements
var placeInput = document.getElementById('place_input');
var placeButton = document.getElementById('place_button');
var placeToggle = document.getElementById('place_toggle');
var selector = document.getElementById('selector');
var selectButton = document.getElementById('select_button');
var possiblePlaceLayers = {}; // this is where i keep the layers to query the map with
var selectedPlace = [];
var saidPolygon = [];

activeDatasetButtons.push(placeButton, placeToggle, selectButton);

function makeSelectorOptions(array) {
  selector.innerHTML = '';
  array.forEach(function (place) {
    var option = document.createElement('option');
    option.value = place.display_name;
    var text = document.createTextNode(place.display_name);
    option.appendChild(text);
    selector.appendChild(option);

    var lyr = L.geoJson(place.geojson);
    possiblePlaceLayers[place.display_name] = lyr;
  });
}

// add place(s) to the selector
placeButton.addEventListener('click', function findPlace() {
  var val = placeInput.value;
  en.getPlaceData(val, makeSelectorOptions);
});

// select place to display
selectButton.addEventListener('click', function selectPlace() {

  Object.keys(possiblePlaceLayers).forEach(function (n) {
    var p = possiblePlaceLayers[n];
    myMap.removeLayer(p);
  });

  selectedPlace.length !== 0 ? (selectedPlace.pop(), selectedPlace.push(possiblePlaceLayers[selector.value])) : selectedPlace.push(possiblePlaceLayers[selector.value]);

  var selectedPlaceType = selectedPlace[0].toGeoJSON().features[0].geometry.type;
  if (selectedPlaceType === 'Polygon' || selectedPlaceType === 'MultiPolygon') {
    var p = selectedPlace[0];
    saidPolygon.push(p);
  }

  var lyr = selectedPlace[0];
  lyr.addTo(myMap);
  myMap.fitBounds(lyr.getBounds());
});

// map and layer should be arguements for a predefined function
placeToggle.addEventListener('click', function () {
  myMap.hasLayer(selectedPlace[0]) ? myMap.removeLayer(selectedPlace[0]) : myMap.addLayer(selectedPlace[0]);
});

// test URL stuff

// (1) hide and show nominatim stuff (do this after I've gotten it working)
var testUrlButton = document.getElementById('test_url_button');
var testUrlContainer = document.getElementById('test_url_container');

testUrlButton.addEventListener('click', function showTestUrlContainer() {

  classToggle(testUrlButton, 'active');

  testUrlContainer.style.display === 'none' || testUrlContainer.style.display === '' ? testUrlContainer.style.display = 'block' : testUrlContainer.style.display = 'none';
});

// (2) get elements
var testUrlInput = document.getElementById('test_url_input');
var getTestUrl = document.getElementById('get_test_url');
var toggleTestUrlsButton = document.getElementById('toggle_test_urls');
var testUrls = document.getElementById('test_urls');

var testDatasets = {};
var testDatasetCount = 0;

// pointMarkerOptions
var testUrlMarkerOptions = {
  radius: 6,
  color: 'white',
  weight: 1.5,
  opacity: 1,
  fillOpacity: 0.4
};

getTestUrl.addEventListener('click', function getDataFromTestUrl() {
  // get ext and url
  var ext = getExt(testUrlInput.value);
  var url = testUrlInput.value;

  // increment the color counter
  testDatasetCount++;
  var testDatasetColor = colors[testDatasetCount % colors.length];

  // get the data with the correct ext, why is this stuff different than
  // the  functions we already have? I'll refactor later
  extSelect(ext, url).then(function handleResponse(response) {
    // make this into a layer
    var layerMod = L.geoJson(null, {
      // set the points to little circles
      pointToLayer: function pointToLayer(feature, latlng) {
        return L.circleMarker(latlng, markerOptions);
      },
      onEachFeature: function onEachFeature(feature, layer) {
        // make sure the fill is the color
        layer.options.fillColor = testDatasetColor;
        // and make sure the perimiter is black (if it's a point) and the color otherwise
        feature.geometry.type === 'Point' ? layer.options.color = 'white' : layer.options.color = testDatasetColor;
        // add those popups
        addPopups(feature, layer); // this comes from the index_maps.js file
      }
    });

    // if the response is good then add abutton for it
    // Ugh, I'm using the 'this' keyword. Not cool.
    // refactor later
    var btn = addButton(testDatasetCount, testDatasetColor, testUrls);

    activeDatasetButtons.push(btn);

    btn.addEventListener('click', function () {
      classToggle(btn, 'active');
      var val = btn.getAttribute('value');
      myMap.hasLayer(testDatasets[val]) ? myMap.removeLayer(testDatasets[val]) : myMap.addLayer(testDatasets[val]);
    });

    // modify data here
    layerMod.addData(response.toGeoJSON());

    testDatasets[testDatasetCount] = layerMod;

    myMap.addLayer(layerMod).fitBounds(layerMod.getBounds());
  }, function handleError(error) {
    console.log(error);
  });
});

// within polygon stuff
//const saidPolygon = []
var fileContainer = [];

// (1) hide and show nominatim stuff (do this after I've gotten it working)
var withinPolygonButton = document.getElementById('within_polygon_button');
var withinPolygonContainer = document.getElementById('within_polygon_container');

// (2) make buttons that will get the data
var getDataWithinPolygonButton = addButton('Get data within polygon', 'black', withinPolygonContainer);
getDataWithinPolygonButton.setAttribute('class', 'btn btn-default');

function showWithinPolygonContainer() {
  classToggle(withinPolygonButton, 'active');

  if (saidPolygon[0]) {
    withinPolygonContainer.innerHTML = ''; // why doesn't this clear everything in the container?
    withinPolygonContainer.appendChild(getDataWithinPolygonButton);
  } else {
    withinPolygonContainer.innerHTML = '<h4>You need a polygon first, get one with the' + ' place selector or draw one.</h4>';
  }

  withinPolygonContainer.style.display === 'none' || withinPolygonContainer.style.display === '' ? withinPolygonContainer.style.display = 'block' : withinPolygonContainer.style.display = 'none';
}

function saveFile(layer, fileNameInput) {
  var filename = fileNameInput.value;
  var data = JSON.stringify(layer.toGeoJSON());
  var blob = new Blob([data], { type: 'text/plain; charset=utf-8' });
  saveAs(blob, filename + '.geojson');
}

function getDataWithinPolygon() {
  // check if the buttons and containers are already here, and if they are clear them,
  // if they are not then create them for the first time, or something. Don't make them
  // twice.

  // this doesn't work
  //  if (withinPolygonContainer.childElementCount > 1) {
  //    console.log(withinPolygonContainer.childElementCount)
  //    showWithinPolygonContainer()
  //  }

  // polygon
  var poly = saidPolygon[0].toGeoJSON();

  var pointsLayers = Object.keys(testDatasets).map(function (k) {
    var v = testDatasets[k];
    if (myMap.hasLayer(v)) {
      var l = v.toGeoJSON().features[0].geometry.type;
      if (l === 'Point' || l === 'MultiPoint') {
        return v.toGeoJSON();
      }
    }
  });

  var pointsWithinLayer = L.geoJSON(null).addTo(myMap);

  // run the turf.within function, and add the data to the layer that will
  // be added to the map, and also converted to geojson and saved.
  pointsLayers.forEach(function (l) {
    var n = turf.within(l, poly);
    pointsWithinLayer.addData(n);
  });

  // make file name input
  var fileNameInput = document.createElement('input');
  fileNameInput.setAttribute('class', 'form-control');
  fileNameInput.setAttribute('placeholder', 'Enter the file name here');
  fileNameInput.setAttribute('type', 'text');
  withinPolygonContainer.appendChild(fileNameInput);

  var saveButton = addButton('Save to geojson file', 'black', withinPolygonContainer);

  saveButton.classList.remove('active');

  saveButton.addEventListener('click', function () {
    return saveFile(pointsWithinLayer, fileNameInput);
  });
}

withinPolygonButton.addEventListener('click', showWithinPolygonContainer);
getDataWithinPolygonButton.addEventListener('click', getDataWithinPolygon);

// (3) add event listener to button that gets the data

// should this function be defined separately, and have arguements?

////////////////////////////////////////////////////////////////////////
// This button/function converts the polygon stored in the 'saidPolygon'
// container and coverts it to geojson. It then gets all the active points
// layers from the map and checks if they fall within a polygon. If they
// are in the polygon, then they are added to a leaflet geojson layer
// which is added to the map. This layer can then be saved to a file
// using the 'filesaver' javascript script functionality. The function
// creates buttons that save the data to a file, and clears the data
// from the saved 
////////////////////////////////////////////////////////////////////////


// clear map
// get button and add click event

var clearMapButton = document.getElementById('clear_map');

clearMapButton.addEventListener('click', function clearMap() {
  // toggle 'active' class off
  activeDatasetButtons.forEach(function deactivate(link) {
    link.classList.remove('active');
  });

  // get all layers from map
  myMap.eachLayer(function clearLayers(layer) {
    // make sure not to remove tile layers
    if (layer !== osm && layer !== stamenToner && layer !== esriWorldImagery) {
      // remove layers
      myMap.removeLayer(layer);
    }
  });
});

//}