from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, RegisterView, ProfileView, UserViews

urlpatterns = [
    # 🔽 Explicit views with names for {% url %}
    path('users/', UserViews.as_view(), name='user-list'),
    path('users/<int:pk>/', UserViews.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='user-login'),
    # 🔽 Explicit views with names for {% url %}
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
]
