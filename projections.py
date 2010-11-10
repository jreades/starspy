import math

def d2dd(d):
    deg,m=d
    if deg < 0:
        return deg-m/60.
    else:
        return deg+m/60.


def d2rad(dd):
    return dd*math.pi/180.

def gcd(p1,p2):
    lat1=d2rad(d2dd(p1[0]))
    lon1=d2rad(d2dd(p1[1]))
    lat2=d2rad(d2dd(p2[0]))
    lon2=d2rad(d2dd(p2[1]))
    s1=math.sin(lat1)
    s2=math.sin(lat2)
    c1=math.cos(lat1)
    c2=math.cos(lat2)
    cd=math.cos(lon1-lon2)
    return 3963. * math.acos(s1*s2+c1*c2*cd)


def plate(lat,lon):
    x=lon*math.pi/180.
    y=lat*math.pi/180.
    return (x,y)

def dist_plate(p1,p2):
    lat1,lon1=p1
    lat2,lon2=p2
    y1,x1=plate(d2dd(lat1),d2dd(lon1))
    y2,x2=plate(d2dd(lat2),d2dd(lon2))
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    d*=24901.55/(2*math.pi)
    return (d,(x1,y1),(x2,y2))


def mercator(lon,lat,R=6738137,s=1.):
    lon=d2rad(lon)
    lat=d2rad(lat)
    Rs=R*s
    x=Rs*lon
    y=Rs*math.log(math.tan(math.pi/4. + lat/2.))
    return (x,y)

def unproj(lon,lat,R=6738137,s=1.):
    xmax=math.pi*R
    x=lon/180. * xmax
    y=lat/180. * xmax
    return(x,y)

def mercatordd(lon,lat,R=6738137,s=1.):
    lon=d2rad(d2dd(lon))
    lat=d2rad(d2dd(lat))
    Rs=R*s
    x=Rs*lon
    y=Rs*math.log(math.tan(math.pi/4. + lat/2.))
if __name__ == '__main__':

    lax=((33,56),(-118,14))
    jfk=((40,29),(-73,47))

    print gcd(lax,jfk)

    la=((35,.54*60),(-118,.64*60))
    london=((51,.53*60),(0,0))
    print gcd(la,london)



    # mercator
    y_lax=d2rad(d2rad(d2dd(lax[0])))
    x_lax=d2rad(d2rad(d2dd(lax[1])))
    y_jfk=d2rad(d2rad(d2dd(jfk[0])))
    x_jfk=d2rad(d2rad(d2dd(jfk[1])))


    # plate
    laxdd=[d2dd(x) for x in lax]
    jfkdd=[d2dd(x) for x in jfk]
    laxr=[d2rad(x) for x in laxdd]
    jfkr=[d2rad(x) for x in jfkdd]


    """
    steps for projections

    1. select longitude value for central meridian. If 0 is chosen the
    central meridian is taken as the prime meridian.
    
    2. Select R, the radius of the refernece globe.

    3. Convert all latitude and longitude degree values to radians. 90 degrees
    in radians is 90 pi/180. 180 degrees is pi radians. All x values represent
    lontiude degree values and x values range from -pi to pi. Latitude values
    on the Earth range from -90 to 90 and all y values range from -pi/2 to
    pi/2.

    4. Compute x and y values by substituting radian values in projection
    equation.
    """


