from django.urls import path
from .views_admin import admin_task_list, admin_task_detail, admin_user_list, admin_user_detail, admin_admin_list,admin_dashboard,create_task

urlpatterns = [
    path('tasks/', admin_task_list, name='admin-task-list'),
    path('tasks/<int:pk>/', admin_task_detail, name='admin-task-detail'),
    path('users/', admin_user_list, name='admin-user-list'),
    path('users/<int:pk>/', admin_user_detail, name='admin-user-detail'),
    path('admins/', admin_admin_list, name='admin-admin-list'),
    path('', admin_dashboard, name='admin-dashboard'),  # Add this line
    path('tasks/create/', create_task, name='admin-task-create'),
]