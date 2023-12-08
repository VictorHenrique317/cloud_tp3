import numpy as np

def handler(input: dict, context: object) -> dict:
    # Extrai as medições de uso de recursos
    nb_cpus = 16
    cpu_percentages = []
    for i in range(1, nb_cpus + 1):
        cpu_percentages.append(input.get(f'cpu_percent-{i}'))

    virtual_memory_total = input.get('virtual_memory-total')
    virtual_memory_buffers = input.get('virtual_memory-buffers')
    virtual_memory_cached = input.get('virtual_memory-cached')

    # Dados de tráfego de rede
    bytes_sent = input.get('net_io_counters_eth0-packets_sent')
    bytes_recv = input.get('net_io_counters_eth0-packets_recv')

    # Calcula a porcentagem de bytes de tráfego de saída
    total_bytes = bytes_sent + bytes_recv
    percent_network_egress = (bytes_sent / total_bytes) * 100 if total_bytes > 0 else 0

    # Calcula a porcentagem de conteúdo em cache de memória
    percent_memory_cache = ((virtual_memory_buffers + virtual_memory_cached) / virtual_memory_total) * 100

    # Calcula uma média móvel de utilização de cada CPU no ultimo minuto
    simple_moving_avgs = []
    for i, cpu_percent_X in enumerate(cpu_percentages):
        X_utilizations = context['env'].get(f'cpu{i+1}_utilizations', [])
        X_utilizations.append(cpu_percent_X)
        
        if len(X_utilizations) > 60:
            X_utilizations.pop(0)
        
        context['env'][f'cpu{i+1}_utilizations'] = X_utilizations
        X_simple_moving_avg = np.mean(X_utilizations)
        simple_moving_avgs.append(X_simple_moving_avg)
        
    # Retorna a resposta
    response  = dict()
    response['percent-network-egress'] = percent_network_egress
    response['percent-memory-cache'] = percent_memory_cache

    for i, simple_moving_avg in enumerate(simple_moving_avgs):
        response[f'moving-avg-cpu{i+1}'] = simple_moving_avg

    return response
