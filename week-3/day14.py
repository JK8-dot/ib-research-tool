import requests
import datetime

API_KEY = "e124755c11742f5004a1654228426741"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    return response.json()

city = input("Enter a city name: ")
data = get_weather(city)

temp = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
description = data["weather"][0]["description"]
city_name = data["name"]
country = data["sys"]["country"]
sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")

print(f"\n{city_name}, {country}")
print(f"Temperature: {temp}°F")
print(f"Feels like: {feels_like}°F")
print(f"Humidity: {humidity}%")
print(f"Wind speed: {wind_speed} mph")
print(f"Conditions: {description.title()}")
print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")

print("\n--- Commodity Weather Analysis ---")
commodity = input("Pick a commodity (oil / gold / wheat): ").lower()

if commodity == "oil":
    region = "New Orleans"
elif commodity == "wheat":
    region = "Wichita"
elif commodity == "gold":
    region = "Johannesburg"
else:
    print("Invalid commodity")
    region = None

if region:
    c_data = get_weather(region)
    c_temp = c_data["main"]["temp"]
    c_desc = c_data["weather"][0]["description"]
    c_wind = c_data["wind"]["speed"]

    print(f"\nWeather in {region}: {c_temp}°F, {c_desc}, wind {c_wind} mph")

    if commodity == "oil" and c_wind > 20:
        print("⚠️ High winds in Gulf Coast — potential disruption to oil production")
    elif commodity == "oil":
        print("✅ Normal conditions in Gulf Coast — no supply disruption expected")
    elif commodity == "wheat" and c_temp > 95:
        print("⚠️ Extreme heat in Kansas — potential stress on wheat crops")
    elif commodity == "wheat":
        print("✅ Normal conditions in Kansas — wheat crop unaffected")
    elif commodity == "gold":
        print("ℹ️ Gold prices driven more by markets than weather — monitor USD and inflation")