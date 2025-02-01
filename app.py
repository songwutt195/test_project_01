import streamlit as st
import pandas as pd

st.title('BaZi Teller')
st.header('BAZI Birth Chart')

inf1, inf2, inf3 = st.columns(3)

inf1.write('Your Birthday:')
with inf2:
  bd_val = st.date_input("", value=None)
with in32:
  bt_val = st.time_input("", value=None)

if st.button("Calculate"):
    st.write(type(bd_val), type(bt_val))
