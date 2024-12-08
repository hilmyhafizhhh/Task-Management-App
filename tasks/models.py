from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)  # Memperbarui max_length menjadi 200
    description = models.TextField(blank=True, null=True)  # Membuat description opsional
    completed = models.BooleanField(default=False)  # Ganti nama dari `done` ke `completed`
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
