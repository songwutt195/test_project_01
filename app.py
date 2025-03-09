import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

utc_now = datetime.utcnow()
this_time = utc_now + timedelta(hours=7)

if 'calendar' not in st.session_state:
    st.session_state.calendar = pd.read_csv('calendar.csv').set_index(['day','month','year'])
    
df_calendar = st.session_state.calendar

if 'relationships' not in st.session_state:
    df_10_gods = pd.read_csv('10g.csv').set_index('elements')
    relationships = {}
    for col in df_10_gods.columns:
        for ind in df_10_gods.index:
            relationships[(col, ind)] = df_10_gods.loc[ind, col]
    st.session_state.relationships = relationships

relationships = st.session_state.relationships

date_dict = {'甲': 'Yang-Wood',
 '乙': 'Yin-Wood',
 '丙': 'Yang-Fire',
 '丁': 'Yin-Fire',
 '戊': 'Yang-Earth',
 '己': 'Yin-Earth',
 '庚': 'Yang-Metal',
 '辛': 'Yin-Metal',
 '壬': 'Yang-Water',
 '癸': 'Yin-Water'}

zodiac_dict = {'子': 'Rat Yang-Water',
 '丑': 'Ox Yin-Earth',
 '寅': 'Tiger Yang-Wood',
 '卯': 'Rabbit Yin-Wood',
 '辰': 'Dragon Yang-Earth',
 '巳': 'Snake Yin-Fire',
 '午': 'Horse Yang-Fire',
 '未': 'Goat Yin-Earth',
 '申': 'Monkey Yang-Metal',
 '酉': 'Rooster Yin-Metal',
 '戌': 'Dog Yang-Earth',
 '亥': 'Pig Yin-Water'}

def find_bazi(by_val, bm_val, bd_val):
    return df_calendar.loc[(bd_val,bm_val,by_val)]

def transfrom_bazi(bazi_series):
    result_key = {'Day':'zd_d', 'Month':'zd_m', 'Year':'zd_y'}
    result_dic = {}
    for key in result_key:
        teamp_result = bazi_series[result_key[key]]
        result_dic[key] = [date_dict[teamp_result[0]]]+zodiac_dict[teamp_result[1]].split()
    return pd.DataFrame(result_dic, index=['Stems Elements', 'Zodiac', 'Branches Elements'])

def analyze_profiles(bazi_table):
    elements_dict = {'Wood':0, 'Fire':0, 'Earth':0, 'Metal':0, 'Water':0}
    
    for col in ['Day', 'Month', 'Year']:
        for ind in ['Stems Elements', 'Branches Elements']:
            elements_dict[(bazi_table.loc[ind, col].split('-')[-1])] += 1

    main_elements = bazi_table.loc['Stems Elements', 'Day'].split('-')[-1]

    return main_elements, elements_dict
    
def analyze_balance(main, dict):
    control_dict = {'Wood':'Metal', 'Fire':'Water', 'Earth':'Wood', 'Metal':'Fire', 'Water':'Earth'}
    encourage_dict = {'Wood':'Water', 'Fire':'Wood', 'Earth':'Fire', 'Metal':'Earth', 'Water':'Metal'}
    color_dict = {'Wood':'Green & Brown', 'Fire':'Red & Purple', 'Earth':'Yellow & Orange', 'Metal':'Silver & Gold', 'Water':'Blue & Black'}

    if dict[control_dict[main]]>0 and dict[encourage_dict[main]]>0:
        balance_result = 'Balance'
        balance_color = 'White'
    elif dict[control_dict[main]]>0:
        balance_result = 'Lack of Encourage'
        balance_color = color_dict[encourage_dict[main]]
    elif dict[encourage_dict[main]]>0:
        balance_result = 'Lack of Control'
        balance_color = color_dict[control_dict[main]]
    else:
        balance_result = 'Imbalance'
        balance_color = color_dict[encourage_dict[main]] + ' & ' + color_dict[control_dict[main]]
    
    return balance_result, balance_color

def analyze_structure(main, dict):
    elements_list = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
    shift = elements_list.index(main)

    structure_list = ['Companion', 'Output', 'Wealth', 'Influence', 'Resource']
    point_list = []
    for i in range(5):
        point_list.append(dict[elements_list[(i+shift)%5]])
    return pd.DataFrame({'structure':structure_list, 'point':point_list})

st.title('BaZi Teller')
st.header('BaZi Birth Chart')

inf1, inf2, inf3 = st.columns(3, vertical_alignment="center")

with inf1:
  by_val = st.number_input("Pls tell Your Birthyear", 
                           value=this_time.year+543, 
                           min_value=this_time.year+443, 
                           max_value=this_time.year+593)
with inf2:
  bm_val = st.number_input("Pls tell Your Birthmonth", 
                           value=this_time.month, 
                           min_value=1, 
                           max_value=12)
with inf3:
  bd_val = st.number_input("Pls tell Your Birthday", 
                           value=this_time.day, 
                           min_value=1, 
                           max_value=31)

if st.button("Calculate"):
    try:
        bazi_result = find_bazi(by_val, bm_val, bd_val)
        bazi_tabel = transfrom_bazi(bazi_result)

        st.divider()
        st.write('Your Birthdatetime: ',datetime(by_val, bm_val, bd_val).strftime("%d %B %Y"))
        st.write(bazi_tabel)

        main_elements, elements_dict = analyze_profiles(bazi_tabel)

        st.divider()
        status, color = analyze_balance(main_elements, elements_dict)
        st.write(f'Your Status: {status}')
        st.write(f'Recommended Colors: {color}')

        st.divider()
        st.write('Your Structure:')
        structure_tabel = analyze_structure(main_elements, elements_dict)
        st.bar_chart(structure_tabel, x="structure", y="point", horizontal=True,
                     x_label='', y_label='')
        st.write(structure_tabel)
        
    except:
        st.write("Please Check Birthdate again!")