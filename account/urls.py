from django.urls import path
from django.conf.urls import url
from .views import UserListView, UserDetailView
from account.views import RegisterFormView, MyLoginView, UpdateProfileView, my_password_change, my_password_reset, my_password_reset_done, my_password_reset_confirm
from django.contrib.auth.views import LogoutView
from submission.views import MySubmissionListView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/profile/', UpdateProfileView.as_view(), name='profile_settings'),
    path('settings/security/', my_password_change, name='profile_security'),
    path('my_submissions/', MySubmissionListView.as_view(), name='my_submissions'),
    path('password_reset/', my_password_reset, name='password_reset'),
    path('password_reset_done/', my_password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', my_password_reset_confirm, name='password_reset_confirm'),
]