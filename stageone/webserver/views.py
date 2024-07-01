import requests
from django.http import JsonResponse
from django.views import View

class HelloAPI(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))

        # Assuming location service is an external API
        location = "Unknown location"
        temperature = "Unknown temperature"

        if client_ip != '127.0.0.1':
            # Fetch location based on client_ip
            geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                location = geo_data.get('city', 'Unknown location')

                # Fetch weather based on location
                weather_api_key = '793705cbf8447a6e14b21a81b2cde988'
                weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric')
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    temperature = weather_data.get('main', {}).get('temp', 'Unknown temperature')

        greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}."
        response_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting
        }
        return JsonResponse(response_data)
