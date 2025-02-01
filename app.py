import streamlit as st
from datetime import datetime, timedelta
from lunarcalendar import Converter, Solar, Lunar
import pandas as pd

utc_now = datetime.utcnow()
time_offset = timedelta(hours=7)
thai_time = utc_now + time_offset

st.title('BaZi Teller')
st.header('BAZI Birth Chart')

inf1, inf2, inf3 = st.columns(3, vertical_alignment="center")

inf1.write('Your Birthday:')
with inf2:
  bd_val = st.date_input("", value=thai_time.date())
with inf3:
  bt_val = st.time_input("", value=thai_time.time())

if st.button("Calculate"):
    st.write(thai_time.date(), thai_time.time())
    st.write(thai_time)
