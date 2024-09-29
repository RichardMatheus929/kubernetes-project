import requests
from time import sleep

# Função para obter métricas do Prometheus
def get_prometheus_metrics(query):
    """
    Consulta o Prometheus com a query PromQL fornecida.
    """
    prometheus_url = "http://localhost:9090/api/v1/query"
    params = {'query': query}
    response = requests.get(prometheus_url, params=params)

    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            return result['data']['result']
        else:
            raise Exception(f"Erro na consulta: {result['error']}")
    else:
        raise Exception(f"Erro HTTP {response.status_code}: {response.text}")

# Função para decidir com base em métricas
def check_memory_usage(memory_metrics, threshold):
    """
    Verifica o uso de memória dos nodes e toma decisões com base em um limite.
    """
    decisions = {}
    
    for metric in memory_metrics:
        node = metric['metric'].get('instance', 'desconhecido')
        memory_usage = float(metric['value'][1])  # Convertendo para float
        
        if memory_usage > threshold:
            decision = f"ALERTA: Memória alta no node {node}. Uso: {memory_usage:.2f}%"
        else:
            decision = f"Uso de memória normal no node {node}. Uso: {memory_usage:.2f}%"
        
        decisions[node] = decision
    
    return decisions

# Função para tomar decisões sobre uso de CPU
def check_cpu_usage(cpu_metrics, threshold):
    """
    Verifica o uso de CPU dos nodes e toma decisões com base em um limite.
    """
    decisions = {}
    
    for metric in cpu_metrics:
        node = metric['metric'].get('instance', 'desconhecido')
        cpu_usage = float(metric['value'][1])  # Convertendo para float
        
        if cpu_usage > threshold:
            decision = f"ALERTA: CPU alta no node {node}. Uso: {cpu_usage:.2f}%"
        else:
            decision = f"Uso de CPU normal no node {node}. Uso: {cpu_usage:.2f}%"
        
        decisions[node] = decision
    
    return decisions

# Função principal para execução e tomada de decisões
def execute_decision_logic():
    """
    Executa a lógica de decisões baseada nas métricas de CPU e Memória.
    """
    try:
        # Consulta para obter o uso de memória
        memory_query = '100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)'
        memory_metrics = get_prometheus_metrics(memory_query)
        
        # Definir o limite de memória em porcentagem
        memory_threshold = 80.0
        
        # Tomar decisões baseadas no uso de memória
        memory_decisions = check_memory_usage(memory_metrics, memory_threshold)
        print("Decisões sobre o uso de memória:")
        for node, decision in memory_decisions.items():
            print(decision)

        # Consulta para obter o uso de CPU
        cpu_query = 'sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)'
        cpu_metrics = get_prometheus_metrics(cpu_query)
        
        # Definir o limite de CPU (taxa de uso de CPU)
        cpu_threshold = 75.0  # Arbitrário, ajustar conforme necessidade
        
        # Tomar decisões baseadas no uso de CPU
        cpu_decisions = check_cpu_usage(cpu_metrics, cpu_threshold)
        print("\nDecisões sobre o uso de CPU:")
        for node, decision in cpu_decisions.items():
            print(decision)

        print('\n---\n')
    
    except Exception as e:
        print(f"Erro ao tomar decisões: {str(e)}")

while True:
    execute_decision_logic()
    sleep(5)
