import json

import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

st.title("Euros 2024 Shot Map")
st.subheader("Filter to any tema/player to see any of their shots taken!")

df = pd.read_csv('euros_2024_shot_map.csv')

df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)

#for selecting players that are only available to a specific team
player = st.selectbox('select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None)

def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    
    return df
filtered_df = filter_data(df,team, player)


pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10,10))
def plot_shots(df, ax, picth):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'], 
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x ['type'] == 'goal' else .5,
            zorder=2 if x['type'] == 'goal' else 1
                      
        )
plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
