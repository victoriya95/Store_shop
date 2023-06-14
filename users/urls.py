from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import login, UserRegistrationView, UserProfileView, logout
from django.contrib.auth.views import LogoutView
from django.urls import path


app_name = 'users'



urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),


]
