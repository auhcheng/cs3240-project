from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.Dashboard, name="dashboard"),
    url(r'^profile/$', views.update_profile, name="profile"),
    url(r'^account/logout/$', views.Logout, name="logout"),
    path('task/<todo_id>/complete', views.complete_todo, name="complete"),
    path('delcomp', views.delete_complete, name="delcomp"),
    path('delall', views.delete_all, name="delall"),
    path('del/<todo_id>', views.delete, name="del"),
    path('task/<todo_id>', views.TaskPage, name="taskpage")
]