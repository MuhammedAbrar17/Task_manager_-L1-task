from django import forms
from .models import Task
from users.models import CustomUser

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'completion_report': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.is_user():
            self.fields['assigned_to'].disabled = True
            self.fields['title'].disabled = True
            self.fields['description'].disabled = True
            self.fields['due_date'].disabled = True
            
            if self.instance.status != 'COMPLETED':
                self.fields['completion_report'].disabled = True
                self.fields['worked_hours'].disabled = True
        
        if self.user and self.user.is_admin():
            # Limit assigned_to to users managed by this admin
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(admin=self.user)