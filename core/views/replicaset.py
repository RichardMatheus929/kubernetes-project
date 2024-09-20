from kubernetes.client.rest import ApiException

from rest_framework.views import APIView
from rest_framework.response import Response

from core.kubernetes_driver import create_replicaset, delete_replicaset, list_replicasets

class ReplicaSetsView(APIView):

    def get(self,request):
        all_replicasets = list_replicasets()
        return Response({"replicasets":all_replicasets},status=200)
        
    def post(self,request):

        replicas = request.data['replicas']
        name = request.data.get('name','my-replicaset')

        if create_replicaset(replicas=replicas, name=name) == 'create':
            return Response({"reponse":f'{request.data['replicas']} replicas para o {name} criados'},status=200)
        else: 
            return Response({"reponse":f'{request.data['replicas']} replicas atualizadas para o replicaset {name}'},status=400)
    
    def delete(self,request):
        object = request.data['object']
        name_object = request.data['name_object']

        try:
            delete_replicaset(object,name_object)
        except ApiException:
            return Response({"reponse":f'Erro ao deletar o replicaset {name_object}, verifique se ele existe'},status=400)

        return Response({"reponse":f'Replicaset: {name_object} deletado'},status=200)