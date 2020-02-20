from django.urls import path
from .views import UserListView, UserDetailView
from account.views import RegisterFormView, MyLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('register', RegisterFormView.as_view(), name='register'),
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]