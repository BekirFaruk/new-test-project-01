import math

def safe_asin(x):
    if x > 1:
        return math.pi / 2
    elif x < -1:
        return -math.pi / 2
    else:
        return math.asin(x)

def custom_ascdiff(decl, lat):
    delta = math.radians(decl)
    phi = math.radians(lat)
    ad = safe_asin(math.tan(delta) * math.tan(phi))
    return math.degrees(ad)

def custom_dnarcs(decl, lat):
    dArc = 180 + 2 * custom_ascdiff(decl, lat)
    nArc = 360 - dArc
    return dArc, nArc

def custom_isAboveHorizon(ra, decl, mcRA, lat):
    dArc, _ = custom_dnarcs(decl, lat)
    return abs((ra - mcRA) % 360) <= dArc / 2

