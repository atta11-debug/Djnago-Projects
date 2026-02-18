from django.shortcuts import render
import requests
import datetime
from django.contrib import messages

WEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"


def home(request):
    city = request.POST.get("city", "Jhang")

    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}

    # Default values
    description = icon = temp = "N/A"
    image_url = None
    exception_occurred = False

    try:
        # 🌤 Weather API
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            description = weather_data["weather"][0]["description"]
            icon = weather_data["weather"][0]["icon"]
            temp = weather_data["main"]["temp"]
        else:
            exception_occurred = True
            messages.error(request, "City not found.")

        # 🖼 Google Image API
        query = city + " 1920x1080"
        image_url_api = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=xlarge"

        image_response = requests.get(image_url_api)
        image_data = image_response.json()

        items = image_data.get("items")
        if items:
            image_url = items[0]["link"]

    except Exception:
        exception_occurred = True
        messages.error(request, "Something went wrong.")

    day = datetime.date.today()

    return render(
        request,
        "index.html",
        {
            "description": description,
            "icon": icon,
            "temp": temp,
            "day": day,
            "city": city,
            "exception_occurred": exception_occurred,
            "image_url": image_url,
        },
    )
