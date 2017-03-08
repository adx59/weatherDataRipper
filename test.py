import weather as wthr

wthr.setLoc('saratoga', 'ca', 'us')
weather = wthr.getWeather()

print(str(weather))
