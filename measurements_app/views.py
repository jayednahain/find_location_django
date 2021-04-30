from django.shortcuts import render,get_object_or_404
from .forms import MeasuremntForms
from geopy.geocoders import Nominatim

#calculating the distance
from geopy.distance import geodesic

#load map
import folium

from .location import get_geo_location,get_center_cordinate,get_zoom


from .models import Measurement

def distanceCalculationView(request):

   #inital set none for using in the model
   distance= None
   destination=None



   #data_object = get_object_or_404(Measurement,id=2)
   #object_test = Measurement.objects.all()

   form = MeasuremntForms(request.POST or None)
   geolocator = Nominatim(user_agent='address_maping')

   current_location = 'daffodil international university '
   current_destination = geolocator.geocode(current_location)
   current_lat = current_destination.latitude
   current_log = current_destination.longitude

   #ip = '72.14.207.99'
   #ip = '103.49.169.33'
   #country , city ,lat,log = get_geo_location(ip)
   #print('location country: ', country)
   #print('city: ', city)
   #print('cordinates: ', lat , log)

   citry_location = geolocator.geocode(current_location)
   #print("##city :", citry_location)


   #location cordinates
   #current_lat = lat
   #current_log =log
   pointA =(current_lat,current_log)



   #map
   m = folium.Map(width=800,height=500,location=get_center_cordinate(current_lat,current_log),zoom_start=50)

   #marking location on map
   folium.Marker(
      [current_lat,current_log],
      tooltip="click here for more",
      popup=current_location,
      icon=folium.Icon(color='purple')
   ).add_to(m)


   if form.is_valid():
      instance = form.save(commit=False)
      get_destination = form.cleaned_data.get('destination')

      destination = geolocator.geocode(get_destination)
      #instance.location= 'San Francisco'

      #distance cordinates
      destination_let = destination.latitude
      destination_log=destination.longitude
      pointB=(destination_let,destination_log)


      #calculation between two points
      distance = round(geodesic(pointA, pointB).km,2)

      # map
      m = folium.Map(width=800, height=500, location=get_center_cordinate(current_lat,current_log,destination_let,destination_log),zoom_start=get_zoom(distance))

      # marking location on map
      folium.Marker(
         [current_lat, current_log],
         tooltip="click here for more",
         popup=current_location,
         icon=folium.Icon(color='purple')
      ).add_to(m)

      folium.Marker(
         [destination_let, destination_log],
         tooltip="click here for more",
         popup=destination,
         icon=folium.Icon(color='purple',icon='cloud')
      ).add_to(m)

      #draw line between two points
      line = folium.PolyLine(locations=[pointA,pointB],weight=2,color='blue')
      m.add_child(line)


      #save to data base
      instance.location = citry_location
      instance.distance = distance
      instance.save()




   #over write the map
   m = m._repr_html_()
   #distance=None
   context = {
      'distance':distance,
      'form':form,
      'map':m,
      'destination':destination
   }

   return render(request,'measurement/measurement.html',context)