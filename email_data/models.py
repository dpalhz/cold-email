import uuid
from django.db import models

class EmailData(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Devisi HR'),
        ('RnD', 'Devisi RnD'),
        ('Media', 'Devisi Media Informasi'),
        ('Engineering', 'Devisi Engineering'),
        ('Customers', 'Customers'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.nama
