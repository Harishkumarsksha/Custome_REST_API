from django.urls import path
from API_App import views

urlpatterns = [
    path('', views.GetallRecords, name='getallrecords'),
    path('get/<str:id>/', views.get, name='get'),
    path('post/', views.post, name='post'),
    path('put/<str:id>/', views.put, name='put'),
    path('delete/<str:id>/', views.delete, name='delete'),
]
