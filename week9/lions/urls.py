from django.urls import path
from . import views

urlpatterns = [
    # Lion CRUD
    path('', views.lion_list, name='lion_list'),
    path('new/', views.lion_create, name='lion_create'),
    path('<int:pk>/', views.lion_detail, name='lion_detail'),
    path('<int:pk>/edit/', views.lion_edit, name='lion_edit'),
    path('<int:pk>/delete/', views.lion_delete, name='lion_delete'),

    # Task
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),

    # LionProfile
    path('<int:pk>/profile/', views.profile_edit, name='profile_edit'),

    # Tag
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/new/', views.tag_create, name='tag_create'),
    path('<int:lion_pk>/tags/<int:tag_pk>/toggle/', views.tag_toggle, name='tag_toggle'),
]
