/**
 * Moves the map to display over Berlin
 *
 * @param  {H.Map} map      A HERE Map instance within the application
 */
//function moveMapToBerlin(map){
//  map.setCenter({lat:55.5807481, lng:36.8251304});
//  map.setZoom(4);
//}
//
///**
// * Boilerplate map initialization code starts below:
// */
//
////Step 1: initialize communication with the platform
//// In your own code, replace variable window.apikey with your own apikey
//var platform = new H.service.Platform({
//  apikey: 'QLfbKK42WjNTlJm--s_6ZnFwYgX9iZSLW14-woQlSMQ'
//});
//var defaultLayers = platform.createDefaultLayers();
//
////Step 2: initialize a map - this map is centered over Europe
//var map = new H.Map(document.getElementById('map'),
//  defaultLayers.vector.normal.map,{
//  center: {lat:50, lng:5},
//  zoom: 4,
//  pixelRatio: window.devicePixelRatio || 1
//});
//// add a resize listener to make sure that the map occupies the whole container
//window.addEventListener('resize', () => map.getViewPort().resize());
//
////Step 3: make the map interactive
//// MapEvents enables the event system
//// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
//var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
//
//// Create the default UI components
//var ui = H.ui.UI.createDefault(map, defaultLayers);
//
//// Now use the map as required...
//window.onload = function () {
//  moveMapToBerlin(map);
//}


<html>
  <head>
  <meta name="viewport" content="initial-scale=1.0, width=device-width" />
  <script src="https://js.api.here.com/v3/3.1/mapsjs-core.js"
  type="text/javascript" charset="utf-8"></script>
  <script src="https://js.api.here.com/v3/3.1/mapsjs-service.js"
  type="text/javascript" charset="utf-8"></script>
  </head>
  <body>
  <div style="width: 640px; height: 480px" id="mapContainer"></div>
  <script>
    // Initialize the platform object:
    var platform = new H.service.Platform({
    'apikey': 'QLfbKK42WjNTlJm--s_6ZnFwYgX9iZSLW14-woQlSMQ'
    });

    // Obtain the default map types from the platform object
    var maptypes = platform.createDefaultLayers();

    // Instantiate (and display) a map object:
    var map = new H.Map(
    document.getElementById('mapContainer'),
    maptypes.vector.normal.map,
    {
      zoom: 10,
      center: { lng: 13.4, lat: 52.51 }
    });
  </script>
  </body>
</html>