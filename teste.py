from prometheus_api_client import PrometheusConnect
import pandas as pd

from time import sleep

# Conectar ao Prometheus (substitua pela URL correta se necessário)
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

# Consulta PromQL para obter o uso de CPU de cada pod no namespace "default" em milicores
cpu_usage_query = 'sum(rate(container_cpu_usage_seconds_total{namespace="default"}[5m])) by (pod) * 1000'


while True:
    # Executar a consulta
    cpu_usage = prom.custom_query(cpu_usage_query)

    # Listas para armazenar os dados
    pod_names = []
    cpu_values = []
    cpu_percentages = []

    # Processar os resultados
    for item in cpu_usage:
        pod_name = item['metric']['pod']
        cpu_value_milicores = float(item['value'][1])  # O valor em milicores
        cpu_percentage = (cpu_value_milicores / 1000) * 100  # Calcular a porcentagem
        
        # Adicionar os dados às listas
        pod_names.append(pod_name)
        cpu_values.append(cpu_value_milicores)
        cpu_percentages.append(cpu_percentage)

    # Criar um DataFrame do pandas
    df = pd.DataFrame({
        'Pod Name': pod_names,
        'CPU Usage (milicores)': cpu_values,
        'CPU Usage (%)': cpu_percentages
    })

    # Exibir os dados em formato tabular
    print("\nUso de CPU de cada pod:")
    print(df)

    # Aguardar 5 segundos antes de executar a próxima iteração
    sleep(3)