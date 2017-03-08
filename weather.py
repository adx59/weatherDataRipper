#!/usr/bin/env python

"""Simple weather API that rips weather info from wunderground.com
    setLoc() function is required for getting weather info
    DICT KEYS:
    temp, humidity, apressure, rainfall, windspeed, winddir, 
    sunrise, sunset, ccondition
    """

from urllib.request import urlopen

city = 0
state = 0
country = 0


class Weather:
    def __init__(self, temp, hmd, prs, precip, winddir, windspeed, sunrise, sunset, cc):
        """weather(temp, hmd, prs, precip, cc) -> None
            creates a class storing the elements of
            weather"""
        self.t = float(temp)
        self.h = hmd
        self.p = prs
        self.pcp = float(precip)
        self.ws = float(windspeed)
        self.wd = winddir
        self.sr = sunrise
        self.ss = sunset
        self.C = cc

    def __str__(self):
        """w.__str__() -> str
            returns weather info in
            a string, for display"""
        return 'Temperature: ' + str(self.t) + '\nHumidity: ' + str(self.h) + '\nAir Pressure: ' + str(self.p)\
        + "\nRainfall: " + str(self.pcp) + "\nWind Speed: " + str(self.ws) + "\nWind Direction: " + \
        str(self.wd) + "\nSunrise: " + self.sr + "\nSunset: " + self.ss +"\nCurrent Weather Condition: " + str(self.C)

    def __dict__(self):
        """w.__dict__() -> dict
            returns weather info as
            as dictionary"""
        return {'temp':self.t,
                'humidity':self.h,
                'apressure':self.p,
                'rainfall':self.pcp,
                'windspeed':self.ws,
                'winddir':self.wd,
                'sunrise':self.sr,
                'sunset':self.ss,
                'ccondition':self.C
                }

    def getFactor(self, factor):
        """w.getFactor(factor) -> float or str
            returns factor of weather, factor parameter
            should be the same as the dict keys"""
        d = self.__dict__()
        return d[factor]
    


def setLoc(c, s, ct):
    """setLoc(city, state) -> None
        sets location for weather detection
        required to run getWeather()"""
    global city, state, country
    if len(s) > 2 or len(ct) > 2:
        raise RuntimeError('only two-letter state/country codes are accepted')
    city = c.replace(' ', '_')
    state = s
    country = ct


def getWeather():
    """getWeather() -> weather
        returns current weather conditions at the
        specified location in the setLoc() function
        rips from wunderground.com"""
    tempStr = ''
    hmdStr = ''
    prsStr = ''
    prpStr = ''
    wspdStr = ''
    wdirStr = ''
    cStr = ''
    srStr = ''
    ssStr = ''

    try:
        global city, state, country
        len(city)
        len(state)
        len(country)
    except:
        raise RuntimeError('No city and/or state specified')

    # <factor>Data LiNe found <- abbreviation for variables
    tempDLNf = False
    hmdDLNf = False
    prsDLNf = False
    prpDNLf = False
    wDLNf = False
    wdDLNf = False
    startReading = False

    w = urlopen('http://wunderground.com/' + country + '/' + state + '/' + city)
    wh = w.readlines()

    # search html file
    for ln in wh:
        l = str(ln)
        if tempDLNf:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    tempStr += char
            tempDLNf = False
        elif hmdDLNf:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    hmdStr += char
            hmdDLNf = False
        elif prsDLNf:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    prsStr += char
            prsDLNf = False
        elif prpDNLf:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    prpStr += char
            prpDNLf = False
        elif wDLNf:
            if "wx-value" in l:
                for char in l:
                    if char == '>':
                        startReading = True
                    elif char == '<':
                        startReading = False
                    elif startReading:
                        wspdStr += char
                wDLNf = False
        elif wdDLNf:
            if 'span class="wx-value"' in l:
                for char in l:
                    if char == '>':
                        startReading = True
                    elif char == '<':
                        startReading = False
                    elif startReading:
                        wdirStr += char
                wdDLNf = False
        elif 'id="cc-sun-rise"' in l:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    srStr += char
        elif 'id="cc-sun-set"' in l:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    ssStr += char
        elif 'data-variable="temperature"' in l:
            tempDLNf = True
        elif 'data-variable="humidity"' in l:
            hmdDLNf = True
        elif 'data-variable="pressure"' in l:
            prsDLNf = True
        elif 'data-variable="precip_today"' in l:
            prpDNLf = True
        elif 'data-variable="wind_speed"' in l:
            wDLNf = True
        elif 'data-variable="wind_dir"' in l:
            wdDLNf = True
        elif 'data-variable="condition"' in l:
            for char in l:
                if char == '>':
                    startReading = True
                elif char == '<':
                    startReading = False
                elif startReading:
                    cStr += char

    # process input from html file
    tempStr = tempStr[:len(tempStr) - 3]
    tempStr = ''.join(filter(lambda x: x.isdigit() or x == '.', tempStr))
    hmdStr = hmdStr[:len(hmdStr)//2]
    hmdStr = ''.join(filter(lambda x: x.isdigit() or x in ['.', '%'], hmdStr))
    prsStr = prsStr[len(prsStr)//2:]
    prsStr = ''.join(filter(lambda x: x.isdigit() or x == '.', prsStr))
    prpStr = prpStr[len(prpStr)//2:]
    prpStr = ''.join(filter(lambda x: x.isdigit() or x == '.', prpStr))
    wspdStr = ''.join(filter(lambda x: x.isdigit() or x == '.', wspdStr))
    wdirStr = wdirStr.replace('Wind from ', '')
    wdirStr = ''.join(filter(lambda f: f in ['N', 'S', 'W', 'E'], wdirStr))
    wdirStr2 = ''
    for chrc in wdirStr:
        if chrc == 'N':
            wdirStr2 += 'S'
        elif chrc == 'S':
            wdirStr2 += 'N'
        elif chrc == 'E':
            wdirStr2 += 'W'
        elif chrc == 'W':
            wdirStr2 += 'E'
    srStr = srStr[:len(srStr)//2]
    srStr = ''.join(filter(lambda x: x.isdigit() or x in ['A', 'M', ' '] or x == ':', srStr))
    ssStr = ssStr[:len(ssStr)//2]
    ssStr = ''.join(filter(lambda x: x.isdigit() or x in ['P', 'M', ' '] or x == ':', ssStr))
    cStr = cStr[:len(cStr)-3]

    return Weather(tempStr, hmdStr, prsStr, prpStr, wdirStr2, wspdStr, srStr, ssStr, cStr)
