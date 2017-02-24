#!/usr/bin/env python

"""Simple weather API that rips weather info from wunderground.com
    setLoc() function is required for getting weather info
    """

from urllib.request import urlopen

city = 0
state = 0
country = 0

class weather:
    def __init__(self, temp, hmd, prs, precip, winddir, windspeed, cc):
        """weather(temp, hmd, prs, precip, cc) -> None
            creates a class storing the elements of
            weather"""
        self.t = float(temp)
        self.h = hmd
        self.p = prs
        self.pcp = float(precip)
        self.ws = float(windspeed)
        self.wd = winddir
        self.C = cc

    def __str__(self):
        return 'Temperature: ' + str(self.t) + '\nHumidity: ' + str(self.h) + '\nAir Pressure: ' + str(self.p)\
        + "\nRainfall: " + str(self.pcp) + "\nWind Speed: " + str(self.ws) + "\nWind Direction: " + \
        str(self.wd) + "\nCurrent Weather Condition: " + str(self.C)


    def getCondition(self):
        return self.C

    def getPrecip(self):
        return self.pcp

    def getPressure(self):
        return self.p

    def getTemp(self):
        return self.t

    def getWindSpd(self):
        return self.ws

    def getHumid(self):
        return self.h

    def getWindDir(self):
        return self.wd


def setLoc(c, s, ct):
    """setLoc(city, state) -> None
        sets location for weather detection
        required to run getWeather()"""
    global city, state, country
    if len(s) > 2 or len(ct) > 2:
        raise RuntimeError('only two-letter state/country codes are accepted')
    city = c.replace(' ', '_')
    state = s
    if ct == '':
        country = ''
    else:
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


    try:
        global city, state, country
        len(city)
        len(state)
        len(country)
    except:
        raise RuntimeError('No city and/or state specified')


    #<factor>Data LiNe found <- abbreviation for variables
    tempDLNf = False
    hmdDLNf = False
    prsDLNf = False
    prpDNLf = False
    wDLNf = False
    wdDLNf = False
    startReading = False

    w = urlopen('http://wunderground.com/' + country + '/'+ state + '/' + city)
    wh = w.readlines()

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

    #please ignore the following block of shameful code
    tempStr = tempStr[:len(tempStr) - 3]
    tempStr = ''.join(filter(lambda x: x.isdigit() or x == '.', tempStr))
    hmdStr = hmdStr[:len(hmdStr)//2]
    hmdStr = ''.join(filter(lambda x: x.isdigit() or x == '.', hmdStr))
    prsStr = prsStr[len(prsStr)//2:]
    prsStr = ''.join(filter(lambda x: x.isdigit() or x == '.', prsStr))
    prpStr = prpStr[len(prpStr)//2:]
    prpStr = ''.join(filter(lambda x: x.isdigit() or x == '.', prpStr))
    wspdStr = ''.join(filter(lambda x: x.isdigit() or x == '.', wspdStr))
    wdirStr = wdirStr.replace('Wind from ', '')
    wdirStr = ''.join(filter(lambda f: f in ['N', 'S', 'W', 'E'], wdirStr))
    wdirStr2 = ''
    for chr in wdirStr:
        if chr == 'N':
            wdirStr2 += 'S'
        elif chr == 'S':
            wdirStr2 += 'N'
        elif chr == 'E':
            wdirStr2 += 'W'
        elif chr == 'W':
            wdirStr2 += 'E'
    cStr = cStr[:len(cStr)-3]

    return weather(tempStr, hmdStr, prsStr, prpStr, wdirStr2, wspdStr, cStr)
