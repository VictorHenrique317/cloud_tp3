import random
import redis
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Função para gerar dados aleatórios para testes
def getMockData():
    random_percentage = lambda: random.randint(0, 100) / 100

    data_dict = {
        'percent-network-egress': 0.8 * random_percentage(),
        'percent-memory-cache': 0.6 * random_percentage(),
        'moving-avg-cpu1': 0.5 * random_percentage(),
        'moving-avg-cpu2': 0.6 * random_percentage(),
        'moving-avg-cpu3': 0.4 * random_percentage(),
        'moving-avg-cpu4': 0.2 * random_percentage(),
        'moving-avg-cpu5': 0.3 * random_percentage(),
        'moving-avg-cpu6': 0.1 * random_percentage(),
        'moving-avg-cpu7': 0.9 * random_percentage(),
        'moving-avg-cpu8': 0.4 * random_percentage(),
        'moving-avg-cpu9': 0.5 * random_percentage(),
        'moving-avg-cpu10': 0.4 * random_percentage(),
        'moving-avg-cpu11': 0.7 * random_percentage(),
        'moving-avg-cpu12': 0.3 * random_percentage(),
        'moving-avg-cpu13': 0.6 * random_percentage(),
        'moving-avg-cpu14': 0.5 * random_percentage(),
        'moving-avg-cpu15': 0.8 * random_percentage(),
        'moving-avg-cpu16': 0.5 * random_percentage(),
    }

    return data_dict

def getDataFromRedis():
    # r = redis.Redis(host='localhost', port=6379, db=0)
    r = redis.Redis(host='67.159.94.11', port=6379, db=0)

    my_id = "victorribeiro"
    key = f"{my_id}-proj3-output"
    data = r.get(key)

    data = data.decode('utf-8')

    data_dict = json.loads(data)
    return data_dict

def getDataDict():
    data_dict = getDataFromRedis()
    return data_dict

# Retira os dados do Redis e os armazena em variáveis
data_dict = getDataDict()
network_egress = data_dict['percent-network-egress']
memory_cache = data_dict['percent-memory-cache']
moving_cpu_avgs = []
for i in range(16):
    moving_cpu_avgs.append(data_dict[f'moving-avg-cpu{i}'])

# Cria a aplicação Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard de monitoramento de recursos'),

    html.H3(children='''
        Métricas:
    '''),

    html.Div(id='network-output', children=f'Porcentagem de saída de rede: {network_egress: .2f}%'),
    html.Div(id= 'memory-cache', children=f'Cache de memória: {memory_cache: .2f}%'),

    dcc.Interval(
        id='interval-component-metrics',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),

    dcc.Graph(
        id='main-graph',
        figure={
            'data': [
                {'x': list(range(16)), 'y': moving_cpu_avgs, 'type': 'bar', 'name': 'CPU'},
            ],
            'layout': {
                'title': '<b> Média móvel da porcentagem de utilização das CPU\'s: </b>',
                'xaxis': {
                    'tickmode': 'array',
                    'tickvals': list(range(16))
                },
                'yaxis': {
                    'range': [0, 1]
                }
            }
        }
    ),

    dcc.Interval(
        id='interval-component-graph',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )

], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'})


# Define um callback para atualizar os valores das métricas a cada segundo
@app.callback(
    Output('network-output', 'children'),
    Output('memory-cache', 'children'),
    Input('interval-component-metrics', 'n_intervals')
)
def update_values(n):
    data_dict = getDataDict() 
    network_egress = data_dict['percent-network-egress']
    memory_cache = data_dict['percent-memory-cache']

    return f'Porcentagem de saída de rede: {network_egress: .2f}%', f'Cache de memória: {memory_cache: .2f}%'

# Define um callback para atualizar o gráfico a cada segundo
@app.callback(
    Output('main-graph', 'figure'),
    Input('interval-component-graph', 'n_intervals')
)
def update_graph_live(n):
    data_dict = getDataDict()
    moving_cpu_avgs = [data_dict[f'moving-avg-cpu{i}'] for i in range(16)]

    figure={
        'data': [
            {'x': list(range(16)), 'y': moving_cpu_avgs, 'type': 'bar', 'name': 'CPU'},
        ],
        'layout': {
            'title': '<b> Média móvel da porcentagem de utilização das CPU\'s: </b>',
            'xaxis': {
                'tickmode': 'array',
                'tickvals': list(range(16))
            },
            'yaxis': {
                'range': [0, 1]
            }
        }
    }

    return figure

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)

