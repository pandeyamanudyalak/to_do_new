

from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render
from .models import SharedTasks, User, UserManager,Tasks
from .utils import send_otp_via_email
from django.shortcuts import redirect
from .forms import ShareTasksForm,TasksForm

# Create your views here.



def register(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_user(email=email,password=password)
        send_otp_via_email(email)
        return render(request,"todoapp/otp_verification.html")
        
    return render(request,"todoapp/registration.html")


def user_registratiob_otp_verification(request):
    
    if request.method=='POST':
        otp = request.POST.get('otp')
        user =  User.objects.filter(otp=otp)
        if user:
            user.update(is_email_verified=True)
            
            return render(request,'todoapp/user_login.html')
        return HttpResponse("not user")
    return HttpResponse("Not is post request")
    

def user_login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        if user:
            login(request,user)
            return redirect("/home")
        return render(request,'todoapp/user_login.html')
    return render(request,'todoapp/user_login.html')

def home(request):
    print(request.user)
    return render(request,'todoapp/home.html')

def add_task(request):
    if request.method=="POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_id = request.user
        print(user_id)
        task = Tasks.objects.create(task_user=user_id,title=title,description=description)
        task.save()
        return render(request,'todoapp/home.html')

    return render(request,'todoapp/home.html')


def task_list(request):
    print(request.user)
    tasks = Tasks.objects.filter(task_user=request.user.id)
    print(tasks)
    return render(request,'todoapp/tasks.html',{"tasks":tasks})


def task_update(request,tid):
    task = Tasks.objects.filter(id=tid)
    print(task)
    return render(request,'todoapp/update_task.html',{"task":task})



def task_delete(request,tid):
    task = Tasks.objects.get(id=tid)
    task.delete()
    return HttpResponse("your task deleted successfilly")
    



def update(request):
    if request.method=="POST":
        tid = request.POST.get('tid')
        print(tid)
        title = request.POST.get("title")
        print(title)
        description = request.POST.get("description")
        print(description)
        completed = request.POST.get('completed')
        print(completed)
        Tasks.objects.filter(id=tid).update(title=title,description=description,is_completd=completed)
        

        return HttpResponse("your task updated successfully")
    return HttpResponse("Gte request")
    



def ShareTask(request,tid):
    user_form = TasksForm()
    share_task_form = ShareTasksForm()
    return render(request,'todoapp/share_task.html',{'task':tid,"form":user_form,"st_form":share_task_form})


def Share(request):
    if request.method=='POST':
        tid = request.POST.get('task_id')
        tk = Tasks.objects.get(id=tid)
        print(tk)
        user_id = request.POST.get("task_user")
        user = User.objects.get(id=user_id)
        print(user)
        read_only = request.POST.get('read_only')
       

        update = request.POST.get('update')
        print(update)
        task = SharedTasks.objects.create(to_user=user,tasks=tk)
        task.save()

        return HttpResponse("ffhjkddjkf")

def ReceivedTasks(request):
    user_id = request.user.id
    task = SharedTasks.objects.filter(to_user=user_id)
    return render(request,'todoapp/received_tasks.html',{"task":task})
