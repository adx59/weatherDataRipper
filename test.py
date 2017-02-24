import weather as wthr

wthr.setLoc('chicago', 'il', 'us')
weather = wthr.getWeather()

print(str(weather))