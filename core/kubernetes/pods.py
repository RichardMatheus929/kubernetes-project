from kubernetes import config, client

from collections import Counter


def list_pods() -> list[dict]:

    all_pods = []

    config.load_kube_config()

    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False).items
    for pod in pods:
        all_pods.append({
            'IP': pod.status.pod_ip,
            'namespace': pod.metadata.namespace,
            'name': pod.metadata.name,
            'status': pod.status.phase
        })

    statuses = [pod.status.phase for pod in pods]

    status_count = Counter(statuses)

    count_status = {
        'Running': status_count.get('Running', 0),
        'Pending': status_count.get('Pending', 0),
        'Succeeded': status_count.get('Succeeded', 0),
        'Failed': status_count.get('Failed', 0),
        'Unknown': status_count.get('Unknown', 0)
    }

    return all_pods, count_status


def list_pods_replicaset(replicaset_name: str) -> list[dict]:

    config.load_kube_config()

    v1_apps = client.AppsV1Api()
    v1 = client.CoreV1Api()

    
    replicaset = v1_apps.read_namespaced_replica_set(
        name=replicaset_name, namespace='default')
        

    # Extrair o selector do ReplicaSet
    selector = replicaset.spec.selector.match_labels
    label_selector = ",".join(
        [f"{key}={value}" for key, value in selector.items()])

    # Listar os pods com base no selector
    pods = v1.list_namespaced_pod(
        namespace='default', label_selector=label_selector).items

    # Lista de todos os pods
    all_pods = [
        {
            'IP': pod.status.pod_ip,
            'namespace': pod.metadata.namespace,
            'name': pod.metadata.name,
            'status': pod.status.phase
        }
        for pod in pods
    ]

    # Contagem dos status dos pods
    statuses = [pod.status.phase for pod in pods]
    status_count = Counter(statuses)

    count_status = {
        'Running': status_count.get('Running', 0),
        'Pending': status_count.get('Pending', 0),
        'Succeeded': status_count.get('Succeeded', 0),
        'Failed': status_count.get('Failed', 0),
        'Unknown': status_count.get('Unknown', 0)
    }

    return all_pods, count_status
