# TP3 - Victor Henrique Silva Ribeiro

Este trabalho consiste na implementação e implantação de uma função serverless para analisar o uso de recursos da máquina virtual do curso. Além disso, foi implementado um painel para exibir continuamente o uso de recursos.

## Tarefa 1

Na primeira tarefa, é criada uma função serverless para processar as métricas de uso de recursos monitoradas na VM. Os resultados desta função serverless são armazenados no Redis.

O arquivo `func.py` contém a implementação desta função. A função recebe um dicionário como entrada, que contém as métricas de uso de recursos. A função processa essas métricas e retorna um dicionário com os resultados.

## Tarefa 2

Na segunda tarefa, é implementado um painel de monitoramento para exibir as informações monitoradas calculadas na Tarefa 1.

O arquivo `dashboard.py` contém a implementação deste painel. O painel é implementado usando a biblioteca Dash e é atualizado a cada segundo para exibir as informações mais recentes.