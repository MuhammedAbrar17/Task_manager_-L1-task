from rest_framework import serializers
from .models import Task
from users.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'assigned_to_username', 
                 'due_date', 'status', 'completion_report', 'worked_hours', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'assigned_to_username']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'completion_report', 'worked_hours', 'due_date']
        
    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not (data.get('completion_report') and data.get('worked_hours')):
                raise serializers.ValidationError(
                    "Completion report and worked hours are required when marking task as completed"
                )
        return data