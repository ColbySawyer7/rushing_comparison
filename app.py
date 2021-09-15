import nfl_data_py as nfl
from pywebio.input import *
from pywebio.session import set_env
from pywebio.output import put_markdown, put_html
from pywebio.platform.tornado_http import start_server
import base64
import pandas as pd
import plotly.express as px
import numpy as np
from bs4 import BeautifulSoup
import argparse

def app():
    set_env(title="Gaskins vs Zeke")
    put_markdown("<h2>Welcome, please enjoy the beautiful data visualization below</h2>")

    # Retrieve Year Data
    df_2021 = nfl.import_weekly_data([2021], downcast=True)
    #print(df_2021)

    #Fetch Gaskins and Zeke Data
    gaskin = getPlayerData('M.Gaskin',df_2021)
    #print(gaskin)
    zeke = getPlayerData('E.Elliott', df_2021)
    #print(zeke)
    total_stats =  pd.concat([gaskin, zeke], axis=0)

    html = printBarChart(total_stats).to_html(include_plotlyjs="require", full_html=False)
    put_html(html)

    put_markdown("Current Leader")
    put_html(getCurrentLeader(total_stats))

def getCurrentLeader(data):
    gaskin_yds = data['rushing_yards'].loc[data['player_name'] == 'M.Gaskin'].values[0]
    #print(gaskin_yds)
    zeke_yds = data['rushing_yards'].loc[data['player_name'] == 'E.Elliott'].values[0]
    #print(zeke_yds)
    if gaskin_yds > zeke_yds:
        data_uri = base64.b64encode(open('gaskin.png', 'rb').read()).decode('utf-8')
    else:
        data_uri = base64.b64encode(open('zeke.png', 'rb').read()).decode('utf-8')

    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    return img_tag

def getPlayerData(name, year_data):
    return year_data.loc[year_data['player_name'] == name]

def printBarChart(data):
    fig = px.bar(data, x='player_name', y='rushing_yards', color='player_name', title = "Total Rushing Yards 2021")
    return fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(app, port=args.port)



