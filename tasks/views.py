from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from users.models import CustomUser

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin() or user.is_admin():
            if user.is_superadmin():
                return Task.objects.all()
            return Task.objects.filter(assigned_to__assigned_admin=user)
        return Task.objects.filter(assigned_to=user)
    
    def perform_create(self, serializer):
        if self.request.user.is_admin() or self.request.user.is_superadmin():
            serializer.save()
        else:
            return Response({"error": "Only admins can create tasks"}, status=status.HTTP_403_FORBIDDEN)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskUpdateSerializer
        return TaskSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # Check if user is allowed to update this task
        if not (user.is_superadmin() or user.is_admin() or instance.assigned_to == user):
            return Response({"error": "You don't have permission to update this task"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # If marking as completed, require report and hours
        if request.data.get('status') == 'COMPLETED':
            if not (request.data.get('completion_report') and request.data.get('worked_hours')):
                return Response(
                    {"error": "Completion report and worked hours are required when marking task as completed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)

class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # Only allow access for completed tasks
        if instance.status != 'COMPLETED':
            return Response({"error": "Task is not completed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check permissions
        if not (user.is_superadmin() or user.is_admin() or instance.assigned_to == user):
            return Response({"error": "You don't have permission to view this report"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)