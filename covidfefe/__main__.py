import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .data import confirmed
from . import data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='COVIDfefe'),
    dcc.Graph(id='cases-graph'),
    html.Label('Country/Region'),
    html.Div([
        dcc.Dropdown(
            id='select-country',
            options=[{'label': label, 'value': label}
                     for label in confirmed.countries],
            value='US'
        ),
        dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        )
    ])
])

@app.callback(
    Output(component_id='cases-graph', component_property='figure'),
    [Input(component_id='select-country', component_property='value'),
     Input('yaxis-type', 'value')]
)
def update_graph(country, yaxis_type):
    return {
        'data': data.dash_data_by_country(country),
        'layout': dict(
            title='Cases by country ({})'.format(country),
            yaxis=dict(
                title='Number of cases',
                type='linear' if yaxis_type == 'Linear' else 'log'
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
