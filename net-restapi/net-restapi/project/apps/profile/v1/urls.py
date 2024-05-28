from django.urls import path

from project.apps.profile.v1 import views

urlpatterns = [
    path("create_personnel/", views.CreateUserViews.as_view(), name='create-personnel'),
    path('get_personnel/<int:pk>/', views.GetUserView.as_view(), name='get-personnel'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('token_refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


]
