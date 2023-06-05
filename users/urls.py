from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import login, registration, profile, logout
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = 'users'



urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    # path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),

]
