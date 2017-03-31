#!/usr/bin/python3
# Created By: Nathan Smith
# Weather API provided by OpenWeatherMap
import urllib.request
import json
import re

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?units=imperial&q=" # API URL (with conversion to imperial)
APP_ID = "abff696c529ee149e0d307f8136c1740"     # key used to access API


# currentWeather
# USES PARAMETERS: url
# url - string supplied that is a valid OpenWeatherMap URL
# uses URLLib.request library to request data from OpenWeatherMap
# Data comes in JSON format, then is decoded into UTF-8 format for json library to use
# Throws an exception if URL is unreachable.
# A URL may be unreachable for the following reasons:
#   - Improper API use
#   - Incorrect APP ID (a key used to access the API)
#   - No connection to internet
def currentWeather(url):
    try:
        with urllib.request.urlopen(url) as response:
            response_string = response.read().decode('UTF-8')
            return json.loads(response_string)
    except urllib.error.URLError:
        print("Connection failed. Check your internet settings and ensure the correct ID is used.")
        return {}


# getCityInfo:
# Uses no parameters.
# This is a function designed to gather input from the user. The user can input various types of input:
#   - City with country: more reliable as there is more information for the API to use.
#       THIS FORMAT ABOVE IS THE RECOMMENDED FORMAT. OTHER FORMATS MAY MISS INFORMATION OR NOT BE AVAILABLE TO THE USER.
#   - Just a city name: unreliable since there are many conflicting city names. The API chooses the result for the user.
#   - Coordinates: the user may not know coordinates, and the format can be confusing
#   - City Code: there are also assigned city codes in the API that a user can enter if the name is too complicated to
#       type.
#   - Country: the API returns the weather for the capital city of the country.
# ---------------------------------------------------------------------------------------------------------------------
# POTENTIAL PROBLEMS:
# - City name isn't found or isn't correct
#       -> API chooses a city close to the name or at random.
# - Gibberish is entered
#       -> API chooses a city at random or tells the user no data is found.
# - Numbers are entered
#       -> API chooses the format closest to it: city code or (if applicable) zip code, however the zip code may
#           conflict with a city code, making this format unreliable to use.
# - Nothing is entered
#       -> Program asks user for input again or a random city is chosen.
def getCityInfo():
    location = input("enter quit or location\n" +
                     "format: city, country\n" +
                     "eg: London, UK\n" +
                     "> ")

    # check for quit - return invalid location
    location = re.sub(r"^\s+", "", location)
    if location == "quit":
        return location

    # extract location data
    location = re.sub(r", ", ",", location)
    location = re.sub(r" ", "+", location)
    location = location.split(',')
    return location


# reportWeather:
# As of (3/12/2016): A known bug in the weather API currently provides the incorrect temperature: off by a few degrees.
# --------------------------------------------------------------------------------------------------------------------
#
# Uses a parameter, location, which is a list containing the names of the city and country.
# This is where the program organizes the weather data, using currentWeather to request the data from the API.
# In the event of an incorrect request or a request in which data is not found, the function displays an error message
# relevant to which error has occurred.
def reportWeather(location):
    city = location[0]
    try:
        country = location[1]
    except IndexError:
        country = ""
    weather_dict = currentWeather("%s%s,%s&appid=%s" % (BASE_URL, city, country, APP_ID))
    try:
        # location
        print("Weather for %s, %s" % (weather_dict['name'], weather_dict['sys']['country']))

        # current temp
        temp_current = weather_dict['main']['temp_max']
        print("Temp: %iºF" % temp_current)

        # high/low
        temp_high = weather_dict['main']['temp_max']
        temp_low =  weather_dict['main']['temp_min']
        print("HIGH: %iºF\tLOW: %iºF" % (temp_high, temp_low))

        # sky conditions
        sky_condition = dict(weather_dict['weather'][0])['description']
        print(sky_condition.capitalize())

        # wind
        wind_speed = int(weather_dict['wind']['speed'])
        print("Wind: %i MPH\n" % wind_speed)
    except KeyError:
        print("Weather data not found for location.")


# main loop of program, this loop ends when the user enters (case insensitive): quit
location = ""
while location != "quit":
    location = getCityInfo()
    if location == "quit" or location[0].lower() == "quit":
        break
    try:
        reportWeather(location)
    except ValueError:
        print("Invalid URL. Be sure a valid website URL is used.")