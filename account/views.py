from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .models import User
from .forms import RegisterForm, LoginForm

from utils.identicon import Identicon
from utils import auth_view


class UserListView(ListView):
    model = User
    template_name = 'account/list.jinja2'
    # paginate_by = 100
    context_object_name = 'users'

    def get_queryset(self):
        return self.model.objects.order_by('-create_time')


class UserDetailView(DetailView):
    model = User
    template_name = 'account/detail.jinja2'

    def get_queryset(self):
        return self.model.objects

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['joined_courses'] = ctx['object'].course_participants.all()
        return ctx

class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "account/login.jinja2"
    redirect_field_name = 'home'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # load CACHE fro form.get_user()
        #
        #
        # ##############################
        return super().form_valid(form)  # auth_login


class RegisterFormView(FormView):
	template_name = 'account/register.jinja2'
	form_class = RegisterForm

	def form_valid(self, form):
		user = form.create()
		user.avatar.save('generated.png', Identicon(str(user.phone)).get_bytes())
		login(self.request, user)
		return redirect('/')
