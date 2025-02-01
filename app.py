import streamlit as st
from datetime import datetime, timedelta
# from lunarcalendar import Converter, Solar, Lunar
import pandas as pd

utc_now = datetime.utcnow()
thai_time = utc_now + timedelta(hours=7)
min_date = utc_now - timedelta(days=3650)

# Elements and Animals for Heavenly Stems and Earthly Branches
heavenly_stems_elements = ["Yang-Wood", "Yin-Wood", "Yang-Fire", "Yin-Fire", "Yang-Earth", "Yin-Earth", "Yang-Metal", "Yin-Metal", "Yang-Water", "Yin-Water"]
earthly_branches_animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

# Function to calculate the Heavenly Stem and Earthly Branch for a given year
def calculate_year_pillar(year):
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return heavenly_stems_elements[stem_index], earthly_branches_animals[branch_index]

# Function to calculate the Heavenly Stem and Earthly Branch for a given month
def calculate_month_pillar(year, month):
    # Simplified approach (may not be accurate for all cases)
    stem_index = (year * 12 + month + 2) % 10
    branch_index = (month) % 12
    return heavenly_stems_elements[stem_index], earthly_branches_animals[branch_index]

# Function to calculate the Heavenly Stem and Earthly Branch for a given day
def calculate_day_pillar(year, month, day):
    # Convert Gregorian date to Julian Day Number (JDN)
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + y * 365 + y // 4 - y // 100 + y // 400 - 32045

    # Calculate the stem and branch for the day
    stem_index = (jdn + 9) % 10
    branch_index = (jdn + 1) % 12
    return heavenly_stems_elements[stem_index], earthly_branches_animals[branch_index]

# Function to calculate the Heavenly Stem and Earthly Branch for a given hour
def calculate_hour_pillar(day_stem, hour):
    # Each day is divided into 12 two-hour periods, each associated with an Earthly Branch
    branch_index = (hour + 1) // 2 % 12
    # The stem of the hour pillar depends on the stem of the day pillar
    stem_index = (day_stem * 2 + branch_index) % 10
    return heavenly_stems_elements[stem_index], earthly_branches_animals[branch_index]

# Main function to calculate Bazi
def calculate_bazi(year, month, day, hour):
    # Calculate the pillars
    year_stem, year_branch = calculate_year_pillar(year)
    month_stem, month_branch = calculate_month_pillar(year, month)
    day_stem, day_branch = calculate_day_pillar(year, month, day)
    hour_stem, hour_branch = calculate_hour_pillar(heavenly_stems_elements.index(day_stem), hour)
    # hour_stem, hour_branch = calculate_hour_pillar(heavenly_stems.index(day_stem), hour)

    # Return the Bazi as a dictionary
    bazi_element_animal = {
        "Hour": [hour_stem, hour_branch],
        "Day": [day_stem, day_branch],
        "Month": [month_stem, month_branch],
        "Year": [year_stem, year_branch],
    }

    return bazi_element_animal

st.title('BaZi Teller')
st.header('BAZI Birth Chart')

inf1, inf2, inf3, inf4 = st.columns(4, vertical_alignment="center")

with inf1:
  by_val = st.number_input("Pls tell Your Birthyear", 
                           value=thai_time.year, 
                           min_value=thai_time.year-100, 
                           max_value=thai_time.year)
with inf2:
  bm_val = st.number_input("Pls tell Your Birthmonth", 
                           value=thai_time.month, 
                           min_value=1, 
                           max_value=12)
with inf3:
  bd_val = st.number_input("Pls tell Your Birthday", 
                           value=thai_time.day, 
                           min_value=1, 
                           max_value=31)
with inf4:
  bt_val = st.time_input("Pls tell Your Birthtime:", value=thai_time.time())

if st.button("Calculate"):
    bazi_dict = calculate_bazi(by_val, bm_val, bd_val, bt_val.hour)
    bazi_tabel = pd.DataFrame(bazi_dict, index=['element', 'animal'])
    st.write('Your Birthdatetime: ',datetime(by_val, bm_val, bd_val).strftime("%d %B %Y"),bt_val.strftime("%H:%M"))
    st.write(bazi_tabel)