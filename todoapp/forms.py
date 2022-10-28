from django import forms
from .models import SharedTasks,User,Tasks



class ShareTasksForm(forms.ModelForm):
    class Meta:
        model = SharedTasks
        fields = ['read_only','can_update']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model =User
#         fields=['email']

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['task_user']


class DateInput(forms.DateInput):
    input_type = 'date'



class TaskForm2(forms.ModelForm):
   
    class Meta:
        model = Tasks
        fields = '__all__'



class ShareTasksUpdateForm(forms.ModelForm):
    class Meta:
        model = SharedTasks
        fields = ['title','description']