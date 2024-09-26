from kubernetes import client, config

import yaml

# Carregar a configuração do Kubernetes
config.load_kube_config()

# Obter a configuração e desabilitar a verificação SSL
configuration = client.Configuration.get_default_copy()
configuration.verify_ssl = False  # Desabilitar a verificação SSL

# Criar um cliente com a nova configuração
api_client = client.ApiClient(configuration)
v1 = client.AppsV1Api(api_client)

api_instance = client.AppsV1Api()

def list_deployments() -> list[dict]:
    all_deployments = []

    deployments = v1.list_deployment_for_all_namespaces(watch=False).items

    for deployment in deployments:
        all_deployments.append({
            'name': deployment.metadata.name,
            'namespace': deployment.metadata.namespace,
            'created_at': deployment.metadata.creation_timestamp,
            'pods_run': deployment.status.available_replicas,
        })

    return all_deployments


def create_deployment(name:str = 'my-replicaset', replicas:int = 1) -> str:
    
    # Criar uma instância da API para ReplicaSets
    with open("core/manifest/deployment.yaml", 'r') as file:
        manifest = yaml.safe_load(file)

    manifest['metadata']['name'] = name
    manifest['spec']['replicas'] = int(replicas)

    # Criar o ReplicaSet no namespace default
    namespace = "default"
    try:
        api_instance.create_namespaced_deployment(
            namespace=namespace, body=manifest)
        return 'create'
    except Exception:  # Caso exista
        api_instance.patch_namespaced_deployment(
            name=name, namespace=namespace, body=manifest)
        return 'update'
    
def delete_deployment(name_object: str, namespace: str = "default"):

    api_instance.delete_namespaced_deployment(
        name=name_object, namespace=namespace)
