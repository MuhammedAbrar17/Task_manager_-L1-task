from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SuperAdmin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    assigned_admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_users')
    
    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}, Role: {self.role}, Assigned Admin: {self.assigned_admin.username if self.assigned_admin else 'None'}"
    
    def is_superadmin(self):
        return self.role == 'SUPERADMIN'
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_user(self):
        return self.role == 'USER'