import googlemaps

class GMaps:

    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def address_to_longlat(self, address):
        loc = self.client.geocode(address)[0]['geometry']['location']
        return (loc['lat'], loc['lng'])

    def longlat_to_addres(self, coords):
        address = self.client.reverse_geocode(coords)[0]["address_components"]
        add_str = ""
        for component in address:
            add_str = " ".join([add_str, component["long_name"]])
        return add_str
        
