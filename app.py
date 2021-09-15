import nfl_data_py as nfl
from pywebio.input import *
from pywebio import *
from pywebio.output import *
import pywebio
import pandas as pd
def app():
    session.set_env(title="Gaskins vs Zeke")
    put_markdown("<h2>Welcome, Please enjoy the beautiful data visualization below</h2>")
    put_column([
        print(zeke_headshot),
        print(gaskins_headshot),
    ])

if __name__ == '__main__':
    start_server(app, port=8081, debug=True)



