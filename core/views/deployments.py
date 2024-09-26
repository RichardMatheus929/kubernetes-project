from rest_framework.views import APIView
from rest_framework.response import Response

from kubernetes.client.rest import ApiException

from core.kubernetes.deployment import list_deployments, create_deployment, delete_deployment

class DeploymentView(APIView):
    
    def get(self, request):

        all_deployments = list_deployments()

        return Response({"deployments": all_deployments}, status=200)
    
    def post(self, request):
        name = request.data.get('name')
        replicas = request.data.get('replicas')

        if create_deployment(replicas=replicas, name=name) == 'create':
            return Response({"reponse":f'{request.data['replicas']} replicas para o {name} criados'},status=200)
        else: 
            return Response({"reponse":f'{request.data['replicas']} replicas atualizadas para o deployment {name}'},status=201)
        
    def delete(self, request):
        name_object = request.data['name_object']

        try:
            delete_deployment(name_object)
        except ApiException:
            return Response({"reponse":f'Erro ao deletar o deployment {name_object}, verifique se ele existe'},status=400)

        return Response({"reponse":f'deployment: "{name_object}" deletado'},status=200)
