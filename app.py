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

players = [{
 'name': 'Myles Gaskin',
 'rushing_yds': 49,
 'rushing_att': 9
}, {
 'name': 'Ezekiel Elliot',
 'rushing_yds': 33,
 'rushing_att': 11
}]

def app():
    set_env(title="Gaskins vs Zeke")
    put_markdown("<h2>Welcome, please enjoy the beautiful data visualization below</h2>")

    html = printBarChart().to_html(include_plotlyjs="require", full_html=False)
    put_html(html)

    put_markdown("Current Leader")
    data_uri = base64.b64encode(open('gaskin.png', 'rb').read()).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    put_html(img_tag)

    df_2021 = nfl.import_weekly_data([2021], downcast=True)
    print(df_2021)


def printBarChart():
    data = pd.DataFrame(players)
    fig = px.bar(players, x='name', y='rushing_yds', color='name', title = "Total Rushing Yards 2021")
    return fig

def getRushingStats(name) -> dict:
    for player in players:
        name = player.get('name', None)
        rushing_yds = player.get('rushing_yds', None)
        rushing_att = player.get('rushing_att', None)
        if name and rushing_yds and rushing_att:
            print(name + ' had a yd per carry average of ' + str(rushing_yds/rushing_att))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(app, port=args.port)



