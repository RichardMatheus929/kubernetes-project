from rest_framework.views import APIView
from rest_framework.response import Response

from core.kubernetes_driver import  list_pods, list_pods_replicaset

# Create your views here.
class PodView(APIView):
    
    def get(self,request, name_replicaset : str = None):

        if name_replicaset:
            all_pods, count_status = list_pods_replicaset(name_replicaset)
            return Response({ "status":count_status,"pods":all_pods,},status=200)
           
        all_pods, count_status = list_pods()
        return Response({ "status":count_status,"pods":all_pods,},status=200)