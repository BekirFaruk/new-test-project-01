from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
import traceback
import math

# Custom utility functions
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

# Patch flatlib.utils
import flatlib.utils
flatlib.utils.isAboveHorizon = custom_isAboveHorizon

def test_location(lat, lon, location_name):
    try:
        date = Datetime('2023/05/15', '12:00', '+00:00')
        pos = GeoPos(lat, lon)
        chart = Chart(date, pos)
        
        # Test a few calculations
        sun = chart.get('Sun')
        moon = chart.get('Moon')
        asc = chart.get('Asc')
        
        print(f"Test başarılı: {location_name} (Enlem: {lat}, Boylam: {lon})")
        print(f"  Güneş: {sun.sign} {sun.signlon:.2f}°")
        print(f"  Ay: {moon.sign} {moon.signlon:.2f}°")
        print(f"  Yükselen: {asc.sign} {asc.signlon:.2f}°")
        print()
        return True
    except Exception as e:
        print(f"Hata: {location_name} (Enlem: {lat}, Boylam: {lon})")
        print(f"  Hata mesajı: {str(e)}")
        print(traceback.format_exc())
        print()
        return False

# Test edilecek lokasyonlar
locations = [
    (0, 0, "Ekvator ve Greenwich Meridyeni"),
    (90, 0, "Kuzey Kutbu"),
    (-90, 0, "Güney Kutbu"),
    (80, 0, "Kuzey Kutbuna Yakın"),
    (-80, 0, "Güney Kutbuna Yakın"),
    (41.0082, 28.9784, "İstanbul"),
    (39.9334, 32.8597, "Ankara"),
    (38.4237, 27.1428, "İzmir"),
    (40.7128, -74.0060, "New York"),
    (-33.8688, 151.2093, "Sydney"),
]

successful_tests = 0
failed_tests = 0

for lat, lon, name in locations:
    if test_location(lat, lon, name):
        successful_tests += 1
    else:
        failed_tests += 1

print(f"Toplam test sayısı: {len(locations)}")
print(f"Başarılı testler: {successful_tests}")
print(f"Başarısız testler: {failed_tests}")

