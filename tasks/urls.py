from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, TaskReportView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]