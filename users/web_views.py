from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from tasks.models import Task
from django.contrib.auth import logout

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superadmin or user.is_admin:
                return redirect('admin-task-list')
            return redirect('user-task-list')
        else:
            error = "Invalid username or password"
    return render(request, 'users/auth/login.html', {'error': error})

def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            error = "Passwords don't match"
        else:
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='USER'
                )
                auth_login(request, user)
                return redirect('user-task-list')
            except Exception as e:
                error = str(e)
    
    return render(request, 'users/auth/register.html', {'error': error})

@login_required
def user_task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/user/task_list.html', {'tasks': tasks})

def logout_view(request):
    logout(request)
    return redirect('web-login')