from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # home page
    path('imoo/login/', views.login_view, name='login'),
    path('imoo/signup/', views.signup, name='signup'),
    path('chat/<str:username>/', views.private_chat, name='private_chat'),
    path('global/', views.global_chat, name='global_chat'),
    path("ai/doubt/", views.ai_doubt_solver, name="ai_doubt"),
]
