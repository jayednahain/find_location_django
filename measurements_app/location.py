from django.contrib.gis.geoip2 import GeoIP2



def get_geo_location(ip):
   g = GeoIP2()
   country = g.country(ip)
   city = g.city(ip)
   lat,lon = g.lat_lon(ip)

   return country,city,lat,lon

def get_center_cordinate(latA,longA,latB=None,longB=None):
   cord = (latA,longA)
   if latB:
      cord = [(latA+latB)/2,(longA+longB)/2]

   return cord

def get_zoom(distance):
   if distance <25:
      return 13
   elif distance > 50:
      return 10
