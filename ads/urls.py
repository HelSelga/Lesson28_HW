from django.urls import path

from ads import views

urlpatterns = [
    path('add/ad/', views.AddToAd.as_view()),
    path('add/cat/', views.AddToCat.as_view()),
    path('cat/', views.CategoryView.as_view()),
    path('cat/create/', views.CategoryCreateView.as_view()),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),
    path('cat/<int:pk>/upd/', views.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/del/', views.CategoryDeleteView.as_view()),
    path('ads/', views.AdView.as_view()),
    path('ads/create/', views.AdCreateView.as_view()),
    path('ads/<int:pk>/', views.AdDetailView.as_view()),
    path('ads/<int:pk>/upload_image/', views.AdImageView.as_view()),
    path('ads/<int:pk>/upd/', views.AdUpdateView.as_view()),
    path('ads/<int:pk>/del/', views.AdDeleteView.as_view()),
]
