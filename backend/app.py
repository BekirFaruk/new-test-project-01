from flask import Flask, request, jsonify
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import math
import traceback
import logging
from flask_cors import CORS

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# CORS'u etkinleştir
CORS(app, resources={r"/calculate_birth_chart": {"origins": "http://localhost:3000"}})  # Frontend uygulamanızın adresi

# Custom utility functions
def safe_asin(x):
    if isinstance(x, str):
        try:
            x = float(x)
        except ValueError:
            logging.error(f"Invalid input to safe_asin: {x}")
            return 0
    if x > 1:
        return math.pi / 2
    elif x < -1:
        return -math.pi / 2
    else:
        return math.asin(x)

def custom_ascdiff(decl, lat):
    try:
        delta = math.radians(float(decl))
        phi = math.radians(float(lat))
        ad = safe_asin(math.tan(delta) * math.tan(phi))
        return math.degrees(ad)
    except Exception as e:
        logging.error(f"Error in custom_ascdiff: {e}")
        return 0

def custom_dnarcs(decl, lat):
    dArc = 180 + 2 * custom_ascdiff(decl, lat)
    nArc = 360 - dArc
    return dArc, nArc

def custom_isAboveHorizon(ra, decl, mcRA, lat):
    dArc, _ = custom_dnarcs(decl, lat)
    return abs((float(ra) - float(mcRA)) % 360) <= dArc / 2

# Patch flatlib.utils
import flatlib.utils
flatlib.utils.isAboveHorizon = custom_isAboveHorizon

def get_coordinates_and_timezone(location):
    geolocator = Nominatim(user_agent="astrological_chart_app")
    location_data = geolocator.geocode(location)
    if location_data:
        lat, lon = location_data.latitude, location_data.longitude
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        return lat, lon, timezone_str
    else:
        raise ValueError(f"Invalid location: {location}")

HOUSE_SYSTEMS = {
    'Placidus': 'Placidus',
    'Koch': 'Koch',
    'Porphyrius': 'Porphyrius',
    'Regiomontanus': 'Regiomontanus',
    'Campanus': 'Campanus',
    'Equal': 'Equal',
    'Whole Sign': 'Whole Sign'
}

def get_house_system_code(house_system):
    logging.debug(f"Getting house system code for: {house_system}")
    if house_system in HOUSE_SYSTEMS:
        result = HOUSE_SYSTEMS[house_system]
        logging.debug(f"Returned house system: {result}")
        return result
    logging.warning(f"Unknown house system: {house_system}. Defaulting to Placidus.")
    return 'Placidus'  # Default to Placidus if not found

def calculate_birth_chart(birth_date, birth_time, birth_location, house_system='Placidus'):
    logging.debug(f"Received house_system: {house_system}")
    try:
        lat, lon, timezone_str = get_coordinates_and_timezone(birth_location)
        logging.debug(f"Coordinates: lat={lat}, lon={lon}, timezone={timezone_str}")
        
        local_tz = pytz.timezone(timezone_str)
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        local_dt = local_tz.localize(dt)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        logging.debug(f"Local datetime: {local_dt}")
        logging.debug(f"UTC datetime: {utc_dt}")
        
        date = Datetime(f"{utc_dt.year:04d}/{utc_dt.month:02d}/{utc_dt.day:02d}", 
                        f"{utc_dt.hour:02d}:{utc_dt.minute:02d}", '+00:00')
        logging.debug(f"Flatlib Datetime: {date}")
        
        pos = GeoPos(lat, lon)
        logging.debug(f"GeoPos: {pos}")
        
        # Set house system
        house_system_code = get_house_system_code(house_system)
        logging.debug(f"Using house system code: {house_system_code}")
        try:
            chart = Chart(date, pos, hsys=house_system_code)
            logging.debug(f"Chart created successfully with house system: {house_system}")
        except Exception as e:
            logging.error(f"Error creating chart: {str(e)}")
            raise ValueError(f"Error creating chart with house system {house_system}: {str(e)}")

        sun_sign = chart.get(const.SUN).sign
        moon_sign = chart.get(const.MOON).sign
        ascendant_sign = chart.get(const.ASC).sign

        planetary_positions = {}
        for planet in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            obj = chart.get(planet)
            planetary_positions[planet] = f"{obj.lon:.1f}° {obj.sign}"

        houses = {}
        for house in range(1, 13):
            house_obj = chart.get(f"House{house}")
            if house_obj:
                houses[f"house_{house}"] = f"{house_obj.lon:.1f}° {house_obj.sign}"
            else:
                houses[f"house_{house}"] = "Unknown"

        return {
            "sun_sign": sun_sign,
            "moon_sign": moon_sign,
            "ascendant_sign": ascendant_sign,
            "planetary_positions": planetary_positions,
            "birth_chart": {
                "houses": houses
            },
            "local_time": local_dt.strftime("%Y-%m-%d %H:%M %Z"),
            "utc_time": utc_dt.strftime("%Y-%m-%d %H:%M %Z"),
            "house_system": house_system
        }
    except Exception as e:
        logging.error(f"Error in calculate_birth_chart: {str(e)}")
        logging.error(traceback.format_exc())
        raise

@app.route('/calculate_birth_chart', methods=['POST'])
def api_calculate_birth_chart():
    data = request.json
    logging.debug(f"Received data: {data}")
    
    birth_date = data.get('birth_date')
    birth_time = data.get('birth_time')
    birth_location = data.get('birth_location')
    house_system = data.get('house_system', 'Placidus')

    logging.debug(f"Extracted parameters: date={birth_date}, time={birth_time}, location={birth_location}, house_system={house_system}")

    if not all([birth_date, birth_time, birth_location]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        result = calculate_birth_chart(birth_date, birth_time, birth_location, house_system)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in api_calculate_birth_chart: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

