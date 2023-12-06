import redis
import json
import dash
import dash_core_components as dcc
import dash_html_components as html

def getMockData():
    data_dict = {
        'percent-network-egress': 0.8,
        'percent-memory-cache': 0.6,
        'moving-avg-cpu1': 0.5,
        'moving-avg-cpu2': 0.6,
        'moving-avg-cpu3': 0.4,
        'moving-avg-cpu4': 0.2,
        'moving-avg-cpu5': 0.3,
        'moving-avg-cpu6': 0.1,
        'moving-avg-cpu7': 0.9,
        'moving-avg-cpu8': 0.4,
        'moving-avg-cpu9': 0.5,
        'moving-avg-cpu10': 0.4,
        'moving-avg-cpu11': 0.7,
        'moving-avg-cpu12': 0.3,
        'moving-avg-cpu13': 0.6,
        'moving-avg-cpu14': 0.5,
        'moving-avg-cpu15': 0.8,
        'moving-avg-cpu16': 0.5,
    }

    return data_dict

def getDataFromRedis():
    r = redis.Redis(host='localhost', port=6379, db=0)

    my_id = 0
    key = f"{my_id}-proj3-output"
    data = r.get(key)

    data = data.decode('utf-8')

    data_dict = json.loads(data)
    return data_dict

data_dict = getMockData()
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
