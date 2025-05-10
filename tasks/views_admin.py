from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from users.models import CustomUser

from django.http import HttpResponseForbidden

@login_required
def admin_task_list(request):
    tasks = Task.objects.all()
    if not request.user.is_superadmin:
        tasks = tasks.filter(assigned_to__assigned_admin=request.user)
    return render(request, 'tasks/admin/task_list.html', {'tasks': tasks})

@login_required
def admin_task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not (request.user.is_superadmin or request.user == task.assigned_to.assigned_admin or request.user == task.assigned_to):
        return HttpResponseForbidden()
    return render(request, 'tasks/admin/task_detail.html', {'task': task})

@login_required
def admin_user_list(request):
    if not request.user.is_superadmin:
        return HttpResponseForbidden()
    users = CustomUser.objects.filter(role='USER')
    print(users)
    return render(request, 'tasks/admin/user_list.html', {'users': users})

@login_required
def admin_user_detail(request, pk):
    if not request.user.is_superadmin:
        return HttpResponseForbidden()
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'tasks/admin/user_detail.html', {'user': user})

@login_required
def admin_admin_list(request):
    if not request.user.is_superadmin:
        return HttpResponseForbidden()
    admins = CustomUser.objects.filter(role='ADMIN')
    return render(request, 'tasks/admin/user_list.html', {'users': admins})

@login_required
def admin_dashboard(request):
    if not (request.user.is_admin or request.user.is_superadmin):
        return HttpResponseForbidden()
    
    context = {
        'user': request.user,  # Pass the user object explicitly
        'is_superadmin': request.user.is_superadmin  # Explicit superadmin flag
    }
    return render(request, 'tasks/admin/dashboard.html', context)

@login_required
def create_task(request):
    # Simple permission check - only allow admins
    if not request.user.is_admin and not request.user.is_superadmin:
        return redirect('admin-task-list')
    
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            assigned_to_id=request.POST['assigned_to'],
            due_date=request.POST['due_date'],
            status='PENDING'
        )
        return redirect('admin-task-list')
    
    # Get only regular users to assign tasks to
    users = CustomUser.objects.filter(role='USER')
    return render(request, 'tasks/admin/task_form.html', {'users': users})