from numpy.lib.function_base import median
import nfl_data_py as nfl
from pywebio.input import select
from pywebio.session import set_env
from pywebio.output import put_markdown, put_html, put_column, put_row, popup
from pywebio.platform.tornado_http import start_server
import base64
import pandas as pd
import plotly.express as px
import numpy as np
from bs4 import BeautifulSoup
import argparse

def app():
    set_env(title="Gaskin vs Zeke")
    put_markdown("<h2>NFL Data Comparison of M.Gaskin and E.Elliott</h2>")

    # Retrieve Year Data
    df_2021 = nfl.import_weekly_data([2021], downcast=True)
    #print(df_2021)

    #Fetch Gaskins and Zeke Data
    gaskin = getPlayerData('M.Gaskin',df_2021)
    #print(gaskin)
    zeke = getPlayerData('E.Elliott', df_2021)
    #print(zeke)
    total_stats =  pd.concat([gaskin, zeke], axis=0)

    #Full Season Bar Graph (Totals)
    full_season_bar = printBarChart(total_stats).to_html(include_plotlyjs="require", full_html=False)

    #Full Season Line Graph (Weekly)
    full_season_line = printLineChart(total_stats).to_html(include_plotlyjs="require", full_html=False)

    put_html(full_season_bar)
    put_html(full_season_line)

    put_markdown("<h3>Current Leader<h3>")
    put_html(getCurrentLeader(total_stats))

    available_weeks = total_stats['week'].value_counts(normalize=True)
    #print(available_weeks)


    selected_week = select("Select Week for week specific data", options=available_weeks)
    if(selected_week is not None):
        selected_week_stats = total_stats.loc[total_stats['week'] == selected_week]
        #Week Bar Graph (Totals)
        title = "Week " + str(selected_week) + " Rushing Totals"
        week_bar = printBarChart(selected_week_stats,title).to_html(include_plotlyjs="require", full_html=False)
        popup(title,[
            put_html(week_bar),
            put_markdown("Week Leader"),
            put_html(getCurrentLeader(selected_week_stats))
        ], size='large')
        


def getCurrentLeader(data):
    gaskin_yds = data['rushing_yards'].loc[data['player_name'] == 'M.Gaskin'].values[0]
    #print(gaskin_yds)
    zeke_yds = data['rushing_yards'].loc[data['player_name'] == 'E.Elliott'].values[0]
    #print(zeke_yds)
    if gaskin_yds > zeke_yds:
        data_uri = base64.b64encode(open('imgs/gaskin.png', 'rb').read()).decode('utf-8')
    else:
        data_uri = base64.b64encode(open('imgs/zeke.png', 'rb').read()).decode('utf-8')

    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    return img_tag

def getPlayerData(name, year_data):
    return year_data.loc[year_data['player_name'] == name]

def printBarChart(data, title="Total Rushing Yards 2021"):
    fig = px.bar(data, x='player_name', y='rushing_yards', color='player_name', title = title)
    return fig

def printLineChart(data):
    fig = px.line(data, x='week', y='rushing_yards', color ='player_name', markers=True, title = 'Weekly Rushing Yards 2021')
    return fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(app, port=args.port)



