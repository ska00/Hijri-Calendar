from flask import Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz
import csv
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Global variables to store our data
moon_phase_data = defaultdict(list)
hijri_data = {}

# Constants
DATEFORMAT = "%Y-%m-%d %H:%M:%S"
HIRJI_START_YEAR = 622
MECCA_TIMEZONE = pytz.timezone('Asia/Riyadh')
SOLARYEAR_DAYS = 365.24219
MUHARRAM_YEARS = [3, 6, 8, 11, 14, 17, 19]

HIJRI_MONTHS = {
    1: "Safar I", 2: "Safar II", 3: "Rabi I", 4: "Rabi II", 
    5: "Jumada I", 6: "Jumada II", 7: "Rajab", 8: "Sha'ban", 
    9: "Ramadan", 10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hij.",
    13: "Muharram", 0: "Muharram"
}

HIJRI_MONTHS_DAYCOUNT = {i: 30 if i % 2 == 1 else 29 for i in range(1, 13)}
HIJRI_MONTHS_DAYCOUNT[13] = 30
HIJRI_MONTHS_DAYCOUNT[0] = 30

KABS_MONTH = 12
KABS_MONTHS = [8, 12]

def load_csv_data(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
            moon_phase_data[date.date()].append({
                'phase': row['phase'],
                'eclipse': row['eclipse'] if row['eclipse'] else None
            })

# Load the CSV data when the app starts
load_csv_data('Moon phases CSV files/moon-phases-601-to-2100-UT.csv.csv')

def calculate_hijri_dates():
    entries = sorted(moon_phase_data.items())
    hijri_year = 1
    lunar_days = 0
    month_count = 0
    is_muharram = False

    for i in range(len(entries) - 1):
        gregorian_start_month, phases = entries[i]
        gregorian_end_month, _ = entries[i + 1]

        if gregorian_start_month.year < HIRJI_START_YEAR:
            continue

        month_count += 1
        start_month = gregorian_start_month + timedelta(days=1)
        end_month = start_month + timedelta(days=HIJRI_MONTHS_DAYCOUNT[month_count])

        days_off = (gregorian_end_month - end_month).days

        if days_off >= 1 and not is_muharram and month_count == KABS_MONTH:
            end_month += timedelta(days=1)
            HIJRI_MONTHS_DAYCOUNT[month_count] = 30
        elif month_count in KABS_MONTHS:
            HIJRI_MONTHS_DAYCOUNT[month_count] = 29

        lunar_days += HIJRI_MONTHS_DAYCOUNT[month_count]

        for day in range(HIJRI_MONTHS_DAYCOUNT[month_count]):
            date = start_month + timedelta(days=day)
            hijri_data[date] = {
                'year': hijri_year,
                'month': month_count,
                'day': day + 1
            }

        if (month_count == 12 and not is_muharram) or month_count == 13:
            hijri_year += 1
            lunar_days = 0
            month_count = 0
            is_muharram = hijri_year % 19 in MUHARRAM_YEARS

calculate_hijri_dates()

def get_hijri_date(gregorian_date):
    return hijri_data.get(gregorian_date.date(), None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/today')
def get_today():
    today = datetime.now(MECCA_TIMEZONE).date()
    hijri_date = get_hijri_date(today)
    phases = moon_phase_data.get(today, [])
    return jsonify({
        "gregorian": today.strftime("%Y-%m-%d"),
        "hijri": hijri_date,
        "moon_phases": phases
    })

@app.route('/api/month/<int:year>/<int:month>')
def get_month(year, month):
    start_date = datetime(year, month, 1, tzinfo=MECCA_TIMEZONE).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1, tzinfo=MECCA_TIMEZONE).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1, tzinfo=MECCA_TIMEZONE).date() - timedelta(days=1)
    
    month_data = []
    current_date = start_date
    while current_date <= end_date:
        hijri_date = get_hijri_date(current_date)
        phases = moon_phase_data.get(current_date, [])
        month_data.append({
            "gregorian": current_date.strftime("%Y-%m-%d"),
            "hijri": hijri_date,
            "moon_phases": phases
        })
        current_date += timedelta(days=1)
    return jsonify(month_data)

if __name__ == '__main__':
    app.run(debug=True)