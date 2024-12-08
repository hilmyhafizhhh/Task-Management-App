from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),  # Landing page
    path('register/', views.register, name='register'),
    
    # Gunakan auth_views untuk login dan logout
    path('login/', auth_views.LoginView.as_view(
        template_name='tasks/login.html',
        redirect_authenticated_user=True), name='login'),
        
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),

    # View setelah login
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('add/', views.TaskCreateView.as_view(), name='add_task'),
    path('edit/<int:pk>/', views.TaskUpdateView.as_view(), name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
]
