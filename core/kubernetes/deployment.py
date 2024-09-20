from kubernetes import client, config


def list_deployments() -> list[dict]:
    all_deployments = []

    config.load_kube_config()

    v1 = client.AppsV1Api()
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
    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
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
        api_instance.create_namespaced_deployment(
            namespace=namespace, body=manifest)
        return 'create'
    except Exception:  # Caso exista
        api_instance.patch_namespaced_deployment(
            name=name, namespace=namespace, body=manifest)
        return 'update'
    
def delete_deployment(name_object: str, namespace: str = "default"):

    # Carregar a configuração do Kubernetes
    config.load_kube_config()

    # Criar uma instância da API para ReplicaSets
    api_instance = client.AppsV1Api()

    api_instance.delete_namespaced_deployment(
        name=name_object, namespace=namespace)
