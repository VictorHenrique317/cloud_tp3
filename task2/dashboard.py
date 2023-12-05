import redis
import json
import dash
import dash_core_components as dcc
import dash_html_components as html

r = redis.Redis(host='localhost', port=6379, db=0)

my_id = 0
key = f"{my_id}-proj3-output"
data = r.get(key)

data = data.decode('utf-8')

data_dict = json.loads(data)

network_egress = data_dict['percent-network-egress']
memory_cache = data_dict['percent-memory-cache']
moving_cpu_avgs = []

for i in range(17):
    moving_cpu_avgs.append(data_dict[f'moving-avg-cpu{i+1}'])


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard de monitoramento de recursos'),

    html.Div(children='''
        Métricas retiradas do Redis.
    '''),

    dcc.Graph(
        id='main-graph',
        figure={
            'data': [
                {'x': list(range(1, 18)), 'y': moving_cpu_avgs, 'type': 'bar', 'name': 'CPU'},
            ],
            'layout': {
                'title': 'Moving Average da utilização de CPU'
            }
        }
    ),

    html.Div(children=f'Network Egress: {network_egress}'),
    html.Div(children=f'Memory Cache: {memory_cache}'),
])

#  The dashboard will be served at localhost:8050 by default.

if __name__ == '__main__':
    app.run_server(debug=True)
