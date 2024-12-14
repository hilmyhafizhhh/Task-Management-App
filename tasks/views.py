from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Log, Comment
from .forms import TaskForm, CommentForm, EditProfileForm


# View untuk halaman landing
class LandingPageView(TemplateView):
    template_name = 'tasks/landing_page.html'


# View untuk registrasi pengguna
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.save()
        return redirect('login')
    return render(request, 'tasks/register.html')


# View untuk login pengguna
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')
    
    return render(request, 'tasks/login.html')


# View untuk logout pengguna
def logout_view(request):
    logout(request)
    return redirect('landing')


# View untuk halaman utama (daftar tugas)
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', 'all')

        tasks = Task.objects.all()

        if status_filter == 'completed':
            tasks = tasks.filter(completed=True)
        elif status_filter == 'pending':
            tasks = tasks.filter(completed=False)

        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        paginator = Paginator(tasks, 5)
        page_number = self.request.GET.get('page')
        tasks_page = paginator.get_page(page_number)

        context['tasks'] = tasks_page
        context['search_query'] = search_query
        context['status_filter'] = status_filter

        return context


# View untuk membuat tugas baru
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        response = super().form_valid(form)
        Log.objects.create(
            user=self.request.user,
            action=f"Membuat tugas: {form.instance.title}",
            timestamp=now()
        )
        return response


# View untuk memperbarui tugas
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit_task.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        response = super().form_valid(form)
        Log.objects.create(
            user=self.request.user,
            action=f"Memperbarui tugas: {form.instance.title}",
            timestamp=now()
        )
        return response


# View untuk menghapus tugas
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    Log.objects.create(
        user=request.user,
        action=f"Menghapus tugas: {task.title}",
        timestamp=now()
    )
    task.delete()
    return redirect('home')


# View untuk halaman tentang
class AboutView(TemplateView):
    template_name = 'tasks/about.html'


# View untuk detail tugas
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


# View untuk halaman profil pengguna
@login_required
def profile(request):
    return render(request, 'tasks/profile.html')


# View untuk mengedit profil pengguna
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'tasks/edit_profile.html', context)


# View untuk menambahkan komentar pada tugas
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

            Log.objects.create(
                user=request.user,
                action=f"Menambahkan komentar pada tugas: {task.title}",
                timestamp=now()
            )

            return redirect('task_detail', pk=task.id)
    else:
        form = CommentForm()

    return render(request, 'tasks/task_detail.html', {'task': task, 'form': form})


# View untuk melihat log aktivitas
class ActivityLogView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'tasks/activity_log.html'
    context_object_name = 'logs'
    ordering = ['-timestamp']
