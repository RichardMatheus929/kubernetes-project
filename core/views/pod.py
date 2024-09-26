from rest_framework.views import APIView
from rest_framework.response import Response

from kubernetes.client.rest import ApiException

from core.kubernetes.pods import  list_pods, list_pods_replicaset

# Create your views here.
class PodView(APIView):
    
    def get(self,request, name_replicaset : str = ""):

        if name_replicaset:
            try:
                all_pods, count_status = list_pods_replicaset(name_replicaset)
            except ApiException:
                return Response({"response":f"Replicaset {name_replicaset} não encontrado"},status=400)
            return Response({ "status":count_status,"pods":all_pods,},status=200)
           
        all_pods, count_status = list_pods()
        return Response({ "status":count_status,"pods":all_pods,},status=200)