from django.urls import path
from . import views

urlpatterns = [
    # List view for tasks
    path('', views.TaskListView.as_view(), name='task_list'),

    # Task creation view
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),

    # Task update view
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),

    # Task detail view (optional)
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
]
