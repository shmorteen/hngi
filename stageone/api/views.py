import requests
from django.http import JsonResponse
from django.views import View

from django.http import JsonResponse
from django.views import View
import requests

class HelloAPI(View):
    def get(self, request):
        print("Received request")
        
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            client_ip = client_ip.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        
        print(f"Visitor name: {visitor_name}")
        print(f"Client IP: {client_ip}")

        location = "Unknown location"
        temperature = "Unknown temperature"

        if client_ip != '127.0.0.1':
            try:
                geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    location = geo_data.get('city', 'Unknown location')

                    weather_api_key = '793705cbf8447a6e14b21a81b2cde988'
                    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric')
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        temperature = weather_data.get('main', {}).get('temp', 'Unknown temperature')
            except Exception as e:
                print(f"Error fetching data: {e}")

        greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}."
        response_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting
        }
        print(f"Response data: {response_data}")
        return JsonResponse(response_data)
