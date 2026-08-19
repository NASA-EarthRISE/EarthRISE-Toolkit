from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_tool, name='add_tool'),
    path('tool/<int:pk>/', views.tool_detail, name='tool_detail'),
    path('quick-create/<str:model_type>/', views.quick_create, name='quick_create'),
    
    path('hds-preview/', views.hds_preview, name='hds_preview'),

]
