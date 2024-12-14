from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import add_comment, ActivityLogView  # Mengimpor view yang dibutuhkan

urlpatterns = [
    # Halaman utama
    path('', views.LandingPageView.as_view(), name='landing_page'),  # Landing page

    # Halaman registrasi
    path('register/', views.register, name='register'),

    # Gunakan auth_views untuk login dan logout
    path('login/', auth_views.LoginView.as_view(
        template_name='tasks/login.html',
        redirect_authenticated_user=True), name='login'),
    
    # Logout dengan redirect ke landing page
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),

    # View setelah login
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),

    # Halaman untuk menambah, mengedit, dan menghapus task
    path('add/', views.TaskCreateView.as_view(), name='add_task'),  # Halaman tambah task
    path('edit/<int:pk>/', views.TaskUpdateView.as_view(), name='edit_task'),  # Halaman edit task
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),  # Halaman hapus task

    # Halaman detail task
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),

    # Halaman profil dan edit profil
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Menambahkan komentar pada task
    path('tasks/<int:task_id>/add_comment/', add_comment, name='add_comment'),

    # Halaman activity log
    path('activity_log/', ActivityLogView.as_view(), name='activity_log'),
]
