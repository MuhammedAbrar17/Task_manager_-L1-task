from django.urls import path
from .web_views import login_view, register_view, user_task_list, logout_view

urlpatterns = [
    path('login/', login_view, name='web-login'),
    path('register/', register_view, name='web-register'),
    path('tasks/', user_task_list, name='web-user-tasks'),
    path('logout/', logout_view, name='logout'),
]