from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

# urlpatterns = [
#     url(r'^$', views.Dashboard, name="dashboard"),
#     url(r'^todos', views.TodoTab, name='todo'),
#     url(r'^notes', views.NotesTab, name='note'),
#     url(r'^profile/$', views.update_profile, name="profile"),
#     url(r'^account/logout/$', views.Logout, name="logout"),
#     path('task/<todo_id>/complete', views.complete_todo, name="complete"),
#     path('delcomp', views.delete_complete, name="delcomp"),
#     path('delall', views.delete_all, name="delall"),
#     path('del/<todo_id>', views.delete, name="del"),
#     path('task/<todo_id>', views.TaskPage, name="taskpage")
# ]

urlpatterns = [
    url(r'^$', views.Dashboard, name="dashboard"),
    url(r'^todos', views.TodosPage, name='todolist'),
    url(r'^notes', views.NotesPage, name='note'),
    url(r'^profile/$', views.update_profile, name="profile"),
    url(r'^account/logout/$', views.Logout, name="logout"),
    path('task/<todo_id>/complete', views.complete_todo, name="complete"),
    path('delcomp', views.delete_complete, name="delcomp"),
    path('delall', views.delete_all, name="delall"),
    path('del/<todo_id>', views.delete, name="del"),
    path('delnote/<note_id>', views.deleteNote, name='delnote'),
    url(r'^calendar/$', login_required(views.CalendarView.as_view()), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('task/<todo_id>', views.edit_todo, name="taskpage"),
]