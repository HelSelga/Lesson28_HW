from django.urls import path

from users import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('<int:pk>/upd/', views.UserUpdateView.as_view()),
    path('<int:pk>/del/', views.UserDeleteView.as_view()),
    path('add/user/', views.AddToUser.as_view()),
    path('add/loc/', views.AddToLocation.as_view()),
]
