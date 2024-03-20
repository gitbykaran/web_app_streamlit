import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Dashboard')

st.markdown(
    '''This dashboard is designed to help you visualize the NBA player stats ! 
* **Python libraries** : streamlit, pandas, base64
* **Data Source** : [Basketball Reference](https://www.basketball-reference.com)'''
)

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('year', list(reversed(range(1950, 2020))))


@st.cache_data
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


