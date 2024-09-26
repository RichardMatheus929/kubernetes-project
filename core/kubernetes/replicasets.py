from kubernetes import config, client

import yaml
from collections import Counter

config.load_kube_config()
v1 = client.AppsV1Api()

# Criar uma instância da API para ReplicaSets
api_instance = client.AppsV1Api()

def list_replicasets():

    all_replicasets = []

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

    with open("core/manifest/replicaset.yaml", 'r') as file:
        manifest = yaml.safe_load(file)

    manifest['metadata']['name'] = name
    manifest['spec']['replicas'] = int(replicas)

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

    api_instance.delete_namespaced_replica_set(
        name=name_object, namespace=namespace)
