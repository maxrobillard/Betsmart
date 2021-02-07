import pandas as pd
import plotly_express as px

import os.path

from urllib.request import urlopen

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dashboard import app

if __name__ == '__main__':
    app.run_server(debug=True)
