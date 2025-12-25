from django.shortcuts import render
import requests
import datetime

# ================= API KEYS =================
OPENWEATHER_API_KEY = "c4fb1bfda677f15f8b621f85666dd7e8"
UNSPLASH_ACCESS_KEY = "rR5jSUp3S9fOe9vIM8Zg8SGnrKc6GJSzJ5b1nX35Wc4"
# ============================================


def home(request):
    # Default city (first load)
    city = request.POST.get('city', 'Mumbai')

    # ---------- DEFAULT BACKGROUND ----------
    image_url = "/static/default.jpg"

    # ---------- WEATHER API ----------
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    # ---------- UNSPLASH IMAGE API ----------
    unsplash_url = "https://api.unsplash.com/search/photos"
    unsplash_params = {
        'query': f"{city} city landscape",
        'client_id': UNSPLASH_ACCESS_KEY,
        'per_page': 1,
        'orientation': 'landscape'
    }

    try:
        # 🌦️ Weather request
        weather_response = requests.get(
            weather_url, params=weather_params, timeout=5
        )
        weather_data = weather_response.json()

        if weather_data.get('cod') != 200:
            raise ValueError("Invalid city")

        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']

        # 🖼️ Unsplash image request
        image_response = requests.get(
            unsplash_url, params=unsplash_params, timeout=5
        )
        image_data = image_response.json()

        if image_data.get('results'):
            image_url = image_data['results'][0]['urls']['regular']

    except Exception:
        # Fallback values if API fails
        temp = "N/A"
        description = "City not found or API error"
        icon = ""
        image_url = "/static/default.jpg"

    context = {
        'city': city,
        'temp': temp,
        'description': description,
        'icon': icon,
        'day': datetime.date.today(),
        'image_url': image_url
    }

    return render(request, 'home.html', context)
