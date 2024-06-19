from django.urls import path

from myapp import views

urlpatterns=[
    path("tasks/add/",views.TaskCreateView.as_view(),name="task-add"),
    path("tasks/all/",views.TaskListView.as_view(),name="task-list"),
    path("tasks/<int:pk>/change/",views.TaskUpdateView.as_view(),name="task-edit"),
    path("tasks/<int:pk>/remove/",views.TaskDeleteView.as_view(),name="task-delete"),
    path("tasks/<int:pk>/",views.TaskDetailView.as_view(),name="task-detail"),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("signin/",views.SigninView.as_view(),name="signin"),
    path("signout/",views.SignOutView.as_view(),name="signout"),


]
