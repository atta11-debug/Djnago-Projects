from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.signup, name="signup"),
    path("loginn/",views.loginn, name="loginn"),
    path("todopage/",views.todopage, name="todopage"),
    path("edit_todo/<int:srno>/",views.edit_todo, name="edit_todo"),
    path("delete_task/<int:srno>/",views.delete_task, name="delete_task"),
    path("signout/",views.signout, name="signout"),
]
