from django.urls import path
from .views import RegisterView, LoginView  # API views
from .web_views import login_view, register_view, user_task_list  # Web views

urlpatterns = [
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    
    # Web views
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('tasks/', user_task_list, name='user-task-list'),
]