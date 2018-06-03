import gmaps

class Point:
    def __init__(self, uid, address, color, googleMapsCall, lt=None, lg=None):
        if(lt == None and lg == None):
            self.id = uid
            self.address = address
            lat, lon = googleMapsCall.address_to_longlat(address)
            self.latitude = lat
            self.longitude = lon
            self.color = color
        else:
            self.latitude = lt
            self.longitude = lg
            self.color = color

    def getDict(self):
        return {"position": {"lat":self.latitude, "lng":self.longitude}, "icon":self.getMarkerCode()}
        
    def getMarkerCode(self):
        s = '''(new google.maps.MarkerImage('http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|' + {0},
              new google.maps.Size(21, 34),
              new google.maps.Point(0, 0),
              new google.maps.Point(10, 34)))'''.format(self.color)
        return s

    def getLat(self):
        return self.latitude

    def getLong(self):
        return self.longitude

    def __str__(self):
        return "Address="+self.address+", Lat="+str(self.latitude)+", long="+str(self.longitude)