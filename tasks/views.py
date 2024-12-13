from django.shortcuts import render
from .models import Task
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LandingPageView(TemplateView):
    template_name = 'tasks/landing_page.html'  # Menentukan template untuk halaman ini

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        # Buat user baru
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

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


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

from django.shortcuts import render, redirect
from django.contrib.auth import logout

# View untuk logout
def logout_view(request):
    logout(request)  # Logout pengguna
    return redirect('landing')  # Arahkan pengguna ke halaman landing atau halaman lain


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Task
from django.core.paginator import Paginator


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/home.html'
    login_url = 'login'  # Pengguna yang belum login akan diarahkan ke halaman login

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', 'all')

        # Ambil query tugas
        tasks = Task.objects.all()

        # Filter berdasarkan status
        if status_filter == 'completed':
            tasks = tasks.filter(completed=True)
        elif status_filter == 'pending':
            tasks = tasks.filter(completed=False)

        # Filter berdasarkan pencarian
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        # Paginasi
        paginator = Paginator(tasks, 5)  # Menampilkan 5 tugas per halaman
        page_number = self.request.GET.get('page')
        tasks_page = paginator.get_page(page_number)

        # Tambahkan data ke dalam context
        context['tasks'] = tasks_page
        context['search_query'] = search_query
        context['status_filter'] = status_filter

        return context


from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm

# Ganti fungsi add_task dengan CBV menggunakan CreateView
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

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit_task.html'
    context_object_name = 'task'
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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    Log.objects.create(
        user=request.user,
        action=f"Menghapus tugas: {task.title}",
        timestamp=now()
    )
    task.delete()
    return redirect('home')
 

from django.views.generic import TemplateView

# View untuk halaman About
class AboutView(TemplateView):
    template_name = 'tasks/about.html'

# views.py

# views.py
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Task

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Halaman profil pengguna
@login_required
def profile(request):
    return render(request, 'tasks/profile.html')

from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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

    context = {
        'form': form,
    }
    return render(request, 'tasks/edit_profile.html', context)

from django.shortcuts import get_object_or_404, redirect
from .models import Task, Comment
from .forms import CommentForm

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



from .models import Log
from django.utils.timezone import now

from django.views.generic import ListView

class ActivityLogView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'tasks/activity_log.html'
    context_object_name = 'logs'
    ordering = ['-timestamp']
