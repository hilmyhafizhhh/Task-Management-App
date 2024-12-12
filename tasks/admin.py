from django.contrib import admin
from .models import Task, Category, Comment, Log

# Tugas
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'completed')  # Sesuaikan dengan atribut model Task
    list_filter = ('completed', 'created_at')  # Pastikan atribut ada di models.py
    search_fields = ('title', 'description')


# Kategori
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# Komentar
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('content',)


# Log Aktivitas
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('action',)
