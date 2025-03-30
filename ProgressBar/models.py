import uuid
import random
import string
import secrets
from django.db import models

def generate_unique_id(length=9):
    """Generuje unikalny ciąg znaków dla public_id i admin_id."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_string(length=9):
    """Funkcja generująca losowy ciąg znaków o zadanej długości."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class Progress(models.Model):
    name = models.CharField(max_length=255, default='Lorem psum')
    percentage = models.FloatField(default=5)
    public_id = models.CharField(max_length=9, unique=True, default=generate_unique_id, editable=False)
    admin_id = models.CharField(max_length=9, default=generate_random_string, unique=True)  # Losowy ciąg znaków
    view_count = models.IntegerField(default=0)  # Liczba wejść na publiczny link

    def increment_view_count(self):
        self.view_count += 1
        self.save()

class Update(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, related_name="updates")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ProgressHistory(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, related_name="history")
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)