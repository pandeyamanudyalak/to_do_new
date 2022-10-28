
from django.urls import path
from . import views

urlpatterns = [
    path('',views.register),
    path('verify_email',views.user_registratiob_otp_verification),
    path('user_login',views.user_login,name="user-login"),
    path('home',views.home),
    path('add_task',views.add_task),
    path('all_task',views.task_list),
    path('task_update/<int:tid>',views.task_update,name='task-update'),
    #path('update',views.update),
    path('task_delete/<int:tid>',views.task_delete,name='task-delete'),
    #path('share_task',views.ShareTask)
    path('share_task/<int:tid>',views.ShareTask,name='share-task'),
    path('share',views.Share),
    path('received_tasks',views.ReceivedTasks,name='received-tasks'),
    path('update_assigned_task/<int:tid>',views.UpdateAssignedTask,name='update-assigned-task')

]