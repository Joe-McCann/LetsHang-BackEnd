import gmaps

class Point:
    def __init__(self, uid, address, color, googleMapsCall, lt=None, lg=None, url=None):
        self.id = uid
        self.address = address
        self.color = color

        if(lt == None and lg == None):
            lt, lg = googleMapsCall.address_to_longlat(address)

        self.latitude = lt
        self.longitude = lg
        self.url = url

    def getDict(self):
        ret = {"position": {"lat":self.latitude, "lng":self.longitude}, "color": self.color, "id":self.id}
        if self.url:
            ret["url"] = self.url
        return ret
        
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