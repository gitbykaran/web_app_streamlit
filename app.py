import streamlit as st
import pandas as pd
import base64
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="NBA Dashboard",
    page_icon="🏀",
    layout="centered",)


st.title('NBA Player Stats Dashboard')
st.image('shaquille_o_neal_nba_wallpaper_by_skythlee_d9rtlbk-pre.jpg')

st.markdown(
    '''This dashboard is designed to help you visualize the NBA player stats ! 
* **Python libraries** : streamlit, pandas, base64
* **Data Source** : [Basketball Reference](https://www.basketball-reference.com)'''
)

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('year', list(reversed(range(1950, 2020))))


@st.cache_resource
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(
        year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(
        df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


playerstats = load_data(selected_year)

unique_team = playerstats['Tm'].unique()
team_selected = st.sidebar.multiselect('Teams', unique_team, unique_team)

unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
sel_pos = st.sidebar.multiselect('Positions', unique_pos, unique_pos)

df_selected_team = playerstats[(playerstats.Tm.isin(team_selected))
                               & (playerstats.Pos.isin(sel_pos))]

st.header('Player Stats of Selected Team(s)')
st.write('Data Dimensions : ' + str(df_selected_team.shape[0]) + ' rows and ' +
         str(df_selected_team.shape[1]) + ' columns')


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.table(df_selected_team.head(10))

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
