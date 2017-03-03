# Weather Data Ripper
Rips weather data from the website wunderground.com by looking through the website's HTML files. A city, state(leave as '' if not in US), and country is required to find current weather conditions. Only two letter state/country codes are accepted (http://www.nationsonline.org/oneworld/country_code_list.htm is where to find the codes if you don't know them). Makes use of the urllib.request library in Python3. 

#Units
Temperature -> Degrees Fahrenheit

Humidity -> Percentage

Air Pressure -> Inches of Mercury(inHG)

Wind Speed -> Miles Per Hour

Wind Direction -> Any combination of N, W, E, S. 

Preciptiation -> Inches

#Functions
setLoc() -> None
sets the location for where to find the weather.
getWeather() -> weather

returns a weather object with the weather data.

WEATHER OBJECT:
str(w) -> str
Returns a string of weather data, which is easily human-readable
dict(w) -> dict
Returns a dictionary of weather data
w.get( insert weather data here )() -> str or float:\n
Returns the weather data requested, based on the function name

