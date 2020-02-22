from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages

from .models import User
from .forms import RegisterForm, LoginForm, ProfileForm, MyPasswordChangeForm, MySetPasswordForm

from utils.identicon import Identicon
from utils import auth_view
from submission.models import STATUS_STR


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
        addtional_ctx = {
            'courses': ctx['object'].course_participants.all().order_by('-create_time')[:5],
            'submissions': ctx['object'].user_submission.all().order_by('-submit_time')[:5],
            'STATUS_STR': STATUS_STR,
            'submission_cnt': ctx['object'].user_submission.all().count(),
        }
        return dict(ctx, **addtional_ctx)

class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "account/login.jinja2"
    redirect_field_name = 'home'
    redirect_authenticated_user = True


class RegisterFormView(FormView):
	template_name = 'account/register.jinja2'
	form_class = RegisterForm

	def form_valid(self, form):
		user = form.create()
		user.avatar.save('generated.png', Identicon(str(user.phone)).get_bytes())
		login(self.request, user)
		return redirect('/')


@method_decorator(login_required, 'dispatch')
class UpdateProfileView(UpdateView):
    template_name = 'account/profile.jinja2'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, '修改成功')
        return self.request.path


def my_password_change(request):
    return auth_view.password_change(
        request, 
        template_name = 'account/security.jinja2',
        post_change_redirect = reverse('profile_settings'),
        password_change_form = MyPasswordChangeForm,
        message = "密码修改成功",
    )

def my_password_reset(request):
    return auth_view.password_reset(
        request,
        post_reset_redirect='password_reset_done',
        template_name='account/password_reset.jinja2',
        email_template_name='account/password_reset_email.jinja2',
        subject_template_name='account/password_reset_subject.jinja2',
    )

def my_password_reset_done(request):
    return auth_view.password_reset_done(
        request,
        template_name='account/password_reset_done.jinja2',
    )

def my_password_reset_confirm(request, **kwargs):
    return auth_view.password_reset_confirm(
        request,
        template_name = 'account/password_reset_confirm.jinja2',
        post_reset_redirect = reverse('login'),
        set_password_form = MySetPasswordForm,
        **kwargs,
    )