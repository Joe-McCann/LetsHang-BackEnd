class Map(object):
    def __init__(self):
        self._points = []
    def add_point(self, coordinates, color="FE7569"):
        self._points.append(Point(*coordinates, color))
    def __str__(self):
        centerLat = sum(( x.getLat() for x in self._points )) / len(self._points)
        centerLon = sum(( x.getLong() for x in self._points )) / len(self._points)
        markersCode = "\n".join(
            [ x.createMarkerCode() for x in self._points
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;

                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 8,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)

class Point:
    def __init__(self, lat, lon, color):
        self.latitude = lat
        self.longitude = lon
        self.color = color

    def createMarkerCode(self):
        code = """
                new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map,
                icon: (new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|"+"{col}",
                    new google.maps.Size(21, 34),
                    new google.maps.Point(0,0),
                    new google.maps.Point(10, 34))),
                shadow: (new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
                    new google.maps.Size(40, 37),
                    new google.maps.Point(0, 0),
                    new google.maps.Point(12, 35)))
                }});""".format(lat=self.latitude, lon=self.longitude, col=self.color)
        
        return code

    def getLat(self):
        return self.latitude

    def getLong(self):
        return self.longitude
