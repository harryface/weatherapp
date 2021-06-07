import requests, json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


def get_weather_info(latitude, longitude):
    dict = {}
    try:
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;"}
        url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}"
        data_request = requests.get(url, headers=header).text
        data = json.loads(data_request)
        dict['time'] = data['properties']['timeseries'][0]['time']
        dict['pres'] = data['properties']['timeseries'][0]['data']['instant']['details']['air_pressure_at_sea_level']
        dict['temp'] = data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
        dict['cloud'] = data['properties']['timeseries'][0]['data']['instant']['details']['cloud_area_fraction']
        dict['hum'] = data['properties']['timeseries'][0]['data']['instant']['details']['relative_humidity']
        dict['wind_d'] = data['properties']['timeseries'][0]['data']['instant']['details']['wind_from_direction']
        dict['wind_sp'] = data['properties']['timeseries'][0]['data']['instant']['details']['wind_speed']
        dict['next_1'] = data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']
        dict['next_6'] = data['properties']['timeseries'][0]['data']['next_6_hours']['summary']['symbol_code']
        dict['next_12'] = data['properties']['timeseries'][0]['data']['next_12_hours']['summary']['symbol_code']
        return dict
    except Exception as e:
        return None
    

class GetWeatherInfoView(View):
    # Since there is no access to the database, its best to use Get instead of Post
    def get(self, request):
        template = "weather.html"
        latitude = request.GET.get('latitude', None)
        longitude = request.GET.get('longitude', None)
        
        if latitude and longitude:
            context = get_weather_info(latitude, longitude)
        else:
            messages.add_message(self.request, messages.ERROR,
                    'Please input your latitude and longitude'
        )
            return redirect('home')
        return render(request, template, context)
