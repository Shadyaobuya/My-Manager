from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView,UpdateView,DeleteView
from django.views.generic import View

from .models import Tasks

from django.contrib.auth.views import LoginView, redirect_to_login

from .forms import UserForm
from .forms import SignUpForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin


# from django.http import Http404

# Create your views here.



class UserLoginView(LoginView):
    template_name='tasks/login.html'
    redirect_authenticated_user=True
    success_url=reverse_lazy('index')

    def get_success_url(self):
        return reverse_lazy('index')

class SignUpView(FormView):
    form_class=UserForm
    template_name='tasks/signup.html'
    success_url=reverse_lazy('index')
    redirect_to_login=True

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(SignUpView,self).form_valid(form)


class HomePage(TemplateView):
    template_name='tasks/index.html'
    
class ViewAllTasks(LoginRequiredMixin, ListView):
    model=Tasks
    context_object_name="all_tasks"
    template_name='tasks/tasks.html'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['all_tasks']=context['all_tasks'].filter(user=self.request.user)
        context['count']=context['all_tasks'].filter(completed=False).count()

        search_task=self.request.GET.get('search_item')
        if search_task:
            context['all_tasks']=context['all_tasks'].filter(task_title__icontains=search_task)
        context['search_task']=search_task
        return context


class Viewtask(LoginRequiredMixin, DetailView):
    model=Tasks
    context_object_name='task'
    template_name='tasks/view_task.html'

class AddTask(LoginRequiredMixin, CreateView):
    model=Tasks
    fields=['task_title','description','completed']
    template_name='tasks/addtask.html'
    success_url=reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddTask,self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model=Tasks
    fields="__all__"
    template_name='tasks/addtask.html'
    success_url=reverse_lazy("index")

class DeleteTask(LoginRequiredMixin, DeleteView):
    model=Tasks
    context_object_name='task'
    template_name='tasks/delete_task.html'
    success_url=reverse_lazy("index")