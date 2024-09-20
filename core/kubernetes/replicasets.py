from kubernetes import config, client

import yaml
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


def create_replicaset(replicas: int = 1, name: str = 'my-replicaset') -> str:
    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    manifest = {
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
                            "image": "richardmatheus929/todolist:latest",
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
        api_instance.create_namespaced_replica_set(
            namespace=namespace, body=manifest)
        return 'create'
    except Exception:  # Caso exista
        api_instance.patch_namespaced_replica_set(
            name=name, namespace=namespace, body=manifest)
        return 'update'


def delete_replicaset(name_object: str, namespace: str = "default"):

    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    api_instance.delete_namespaced_replica_set(
        name=name_object, namespace=namespace)
