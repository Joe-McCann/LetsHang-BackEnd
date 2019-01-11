import letshang.Map_API.gmaps as gmaps
import letshang.Map_API.mapPoints as mapPoints
import letshang.Map_API.graphFunctions as graph
from googleplaces import GooglePlaces, types, lang

class mapMaker:
    def __init__(self, jsonReq):
        self.gm = gmaps.GMaps('AIzaSyBCOPpz9nItjNrXMrTbA71B0pCX2o5P1E8')
        self.google_places = GooglePlaces('AIzaSyBCOPpz9nItjNrXMrTbA71B0pCX2o5P1E8')
        self.points = []
        self.nearbyPOI = []
        for key, values in jsonReq["mapData"].items():
            self.points.append(mapPoints.Point(key, values["address"], values["color"], self.gm))

    def getCenterPoint(self):
        return graph.centroid([(p.getLat(), p.getLong()) for p in self.points])

    def getNearbyPlaces(self):
        center = self.gm.address_to_longlat(self.gm.longlat_to_addres(self.getCenterPoint()))
        cenDict = {"lat": center[0], "lng": center[1]}
        query_result = self.google_places.nearby_search(lat_lng=cenDict, radius=4000)
        for place in query_result.places:
            place.get_details()
            name = place.name
            LL = place.geo_location
            purl = place.url
            print(purl)
            self.points.append(mapPoints.Point(name, "", "e6edeb", self.gm, lt=float(LL['lat']), lg=float(LL['lng']), url=purl))

    def getDict(self):
        center = self.gm.address_to_longlat(self.gm.longlat_to_addres(self.getCenterPoint()))
        self.getNearbyPlaces()
        p = mapPoints.Point("center", "", "4286f4", self.gm, lt=center[0], lg=center[1])
        jsonDict = {"center":{"lat": center[0], "lng": center[1]}, "markers":[x.getDict() for x in self.points]}
        jsonDict["markers"].append(p.getDict())
        return jsonDict

    def __str__(self):
        return "\n".join([str(x) for x in self.points])


