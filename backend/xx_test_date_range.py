from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
import datetime

def test_date(year, month, day):
    try:
        date = Datetime(f"{year:04d}/{month:02d}/{day:02d}", "12:00", "+00:00")
        pos = GeoPos(0, 0)  # Ekvator üzerinde Greenwich meridyeni
        Chart(date, pos)
        return True
    except Exception:
        return False

def find_date_range():
    print("Desteklenen tarih aralığını kontrol ediyorum...")
    
    # En eski tarihi bul
    start_year = 1
    while not test_date(start_year, 1, 1):
        start_year += 100
    while not test_date(start_year, 1, 1):
        start_year += 1
    
    # En yeni tarihi bul
    end_year = datetime.datetime.now().year
    while test_date(end_year, 12, 31):
        end_year += 100
    while test_date(end_year, 12, 31):
        end_year -= 1
    
    print(f"Desteklenen en eski tarih: {start_year}-01-01")
    print(f"Desteklenen en yeni tarih: {end_year}-12-31")

if __name__ == "__main__":
    find_date_range()

