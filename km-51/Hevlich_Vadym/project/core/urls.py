from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', login_required(views.MainView.as_view()), name='main'),
    path('signin/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    path('repo/<int:pk>/', login_required(views.RepoView.as_view()), name='repo'),
    path('categories/', login_required(views.CategoriesView.as_view()), name='categories'),
    path('category/<int:pk>', login_required(views.CategoryView.as_view()), name='category'),
]
