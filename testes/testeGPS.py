from gps import *
    
gpsd = gps(mode=WATCH_ENABLE)


print("lmao")
px = gpsd.next()
while True:
    px = gpsd.next()
    if px['class'] == 'TPV':
        latAtual = getattr(px, 'lat', "unknown")
        lonAtual = getattr(px, 'lon', "unknown")
        print("latitude: " + str(latAtual) + "longitude: " + str(lonAtual))
        print("foidaseeee")
