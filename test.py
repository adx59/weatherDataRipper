import weather as wthr

wthr.setLoc('beijing', '', 'cn')
weather = wthr.getWeather()

print(str(weather))