from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Konfigurasi untuk aplikasi 'tasks'.
    Kelas ini mengatur pengaturan dan perilaku aplikasi di Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Menentukan tipe default untuk kolom auto-increment.
    name = 'tasks'  # Nama aplikasi yang dikenali oleh Django.
