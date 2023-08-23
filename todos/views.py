from django.shortcuts import render,redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Task


# https://ccbv.co.uk/projects/Django/4.1/

class CustomeLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')

class CustomRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(CustomRegisterView,self).form_valid()
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(CustomRegisterView,self).get(self,*args,**kwargs)
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    paginate_by = 2  # if pagination is desired
    template_name = 'task_list.html'  # Replace with the actual template name
    context_object_name = 'todos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, complete=False)
        queryset = queryset.order_by('-created_at')  # Order by creation date in descending order
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        # context["todos"] = context["todos"].filter(user=self.request.user)
        #context["count"] = context["todos"].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_detail.html'  # Replace with the actual template name
    context_object_name = 'todo'



class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'task_form.html'  # Replace with the actual template name
    fields = ["title","description","complete"]
    # fields = '__all__'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task_form.html'  # Replace with the actual template name
    fields = ["title","description","complete"]
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate,self).form_valid(form)


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'  # Replace with the actual template name
    success_url = reverse_lazy('task-list')