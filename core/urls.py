from django.contrib import admin
from django.urls import path,include

from core.views.pod import PodView
from core.views.replicaset import ReplicaSetsView
from core.views.deployments import DeploymentView

urlpatterns = [
    path('pods/', PodView.as_view()),
    path('pods/<str:name_replicaset>', PodView.as_view()),
    path('replicasets/', ReplicaSetsView.as_view()),
    path('deployments/', DeploymentView.as_view()),
]