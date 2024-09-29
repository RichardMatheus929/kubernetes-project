from pprint import pprint
import requests

# Chamando o endpoitn de metricas do prometheus para pesquisa a partir de uma query
url = "http://localhost:9090/api/v1/query"
prometheus_query = '100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)'
# prometheus_query = 'sum by (namespace) (kube_pod_info)'
params = {"query":prometheus_query}

response = requests.get(url, params=params)
all_metrics = response.json()['data']['result']

# print('Métricas totais')
# pprint(all_metrics)

for metric in all_metrics:
    # print(f"Node: {metric['metric']['instance']} RAM-USAGE {float(metric['value'][1]):.2f}%")
    pprint(metric)

# import pdb; pdb.set_trace()

