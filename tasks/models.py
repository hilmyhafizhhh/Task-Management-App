from django.db import models
from django.contrib.auth.models import User  # Mengimpor User model dari django

# Model Task
class Task(models.Model):
    title = models.CharField(max_length=200)  # Memperbarui max_length menjadi 200
    description = models.TextField(blank=True, null=True)  # Membuat description opsional
    completed = models.BooleanField(default=False)  # Ganti nama dari `done` ke `completed`
    created_at = models.DateTimeField(auto_now_add=True)  # Menyimpan waktu pembuatan

    def __str__(self):
        return self.title  # Menampilkan judul task ketika dipanggil

# Model Category
class Category(models.Model):
    name = models.CharField(max_length=100)  # Nama kategori
    description = models.TextField(blank=True, null=True)  # Deskripsi kategori (opsional)
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan kategori

    def __str__(self):
        return self.name  # Menampilkan nama kategori ketika dipanggil

# Model Comment
class Comment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='comments')  # Menghubungkan komentar dengan task
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Menghubungkan komentar dengan user
    content = models.TextField()  # Konten komentar
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan komentar

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'  # Menampilkan info komentar

# Model Log
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Menghubungkan log dengan user
    action = models.CharField(max_length=255)  # Tindakan yang dilakukan oleh user
    timestamp = models.DateTimeField(auto_now_add=True)  # Waktu tindakan dilakukan

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"  # Menampilkan log dengan format yang jelas
