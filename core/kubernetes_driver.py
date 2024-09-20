from kubernetes import client, config, watch

from collections import Counter

def list_replicasets():
    all_replicasets = []

    config.load_kube_config()

    v1 = client.AppsV1Api()
    replicasets = v1.list_replica_set_for_all_namespaces(watch=False).items

    for replicaset in replicasets:
        all_replicasets.append({    
            'name': replicaset.metadata.name,
            'namespace': replicaset.metadata.namespace,
            'created_at': replicaset.metadata.creation_timestamp,
            'replicas': replicaset.spec.replicas,
            'available_replicas': replicaset.status.available_replicas
        })

    return all_replicasets

def list_pods_replicaset(replicaset_name : str) -> list[dict]:

    config.load_kube_config()

    v1_apps = client.AppsV1Api()
    v1 = client.CoreV1Api()

    replicaset = v1_apps.read_namespaced_replica_set(name=replicaset_name, namespace='default')

    # Extrair o selector do ReplicaSet
    selector = replicaset.spec.selector.match_labels
    label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])

    # Listar os pods com base no selector
    pods = v1.list_namespaced_pod(namespace='default', label_selector=label_selector).items

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

def create_replicaset(replicas : int = 1, name : str ='my-replicaset') -> str:
    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    # Definir o manifesto do ReplicaSet
    replicaset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "ReplicaSet",
        "metadata": {
            "name": name
        },
        "spec": {
            "replicas": int(replicas),
            "selector": {
                "matchLabels": {
                    "app": "my-app-django"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "my-app-django"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "my-app-django",
                            "image": "richardmatheus929/learn-docker:latest",
                            "ports": [
                                {
                                    "containerPort": 8000
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Criar o ReplicaSet no namespace default
    namespace = "default"   
    try:
        api_instance.create_namespaced_replica_set(namespace=namespace, body=replicaset_manifest)
        return 'create'
    except Exception: #Caso exista
        api_instance.patch_namespaced_replica_set(name=name, namespace=namespace, body=replicaset_manifest)
        return 'update'

def delete_replicaset(object_to_delete : str, name_object : str, namespace : str = "default"):

    objects_can_deletes = ['ReplicaSet','Pod','Service','Deployment']

    if object_to_delete not in objects_can_deletes:
        raise ValueError(f"Verifique se o nome do objeto: {object_to_delete} é um objeto válido")

    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    if object_to_delete == 'ReplicaSet':
        api_instance.delete_namespaced_replica_set(name=name_object, namespace=namespace)
