

from asyncio import Task
from re import L
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render
from .models import SharedTasks, User, UserManager,Tasks
from .utils import send_otp_via_email
from django.shortcuts import redirect
from .forms import ShareTasksForm,TasksForm,TaskForm2,ShareTasksUpdateForm

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
        user = User.objects.filter(email=email,is_email_verified=True)
        if user:
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                return redirect("/home")
            return render(request,'todoapp/user_login.html')
        send_otp_via_email(email)
        return render(request,"todoapp/otp_verification.html")
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
    t = SharedTasks.objects.all()
    l = []

    for t in t:
        l.append(t.id)
    print(l)
    task = SharedTasks.objects.get(id=tid)
   
    form = ShareTasksUpdateForm(instance=task)
    task_id = task.id 
    print(task_id)
    if request.method=="POST":
        update_form = ShareTasksUpdateForm(request.POST,instance=task)
        if update_form.is_valid():
            fm = update_form.save(commit=False)
            fm.user = request.user
            fm.notify = True
            fm.save()


            return HttpResponse("your task updated successfully")
        return HttpResponse("your form is not valid")
    return render(request,'todoapp/update_task.html',{"form":form,'tid':task_id})



def task_delete(request,tid):
    task = Tasks.objects.get(id=tid)
    task.delete()
    return HttpResponse("your task deleted successfilly")
    


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
        print('---------------resd inly',read_only)
        can_update = request.POST.get('can_update')
       

        update = request.POST.get('update')
        print(update)
        task = SharedTasks.objects.create(to_user=user,can_update=True if can_update == 'on' else False,read_only=True if read_only == 'on' else False,tasks=tk,title=tk.title,description=tk.description,assigned_by=request.user.id)
        task.save()

        return HttpResponse("Your Task Successfully shared")

def ReceivedTasks(request):
    user_id = request.user.id
    task = SharedTasks.objects.filter(to_user=user_id)
    return render(request,'todoapp/received_tasks.html',{"task":task})
    

def UpdateAssignedTask(request,tid):
    print('----------------tid',tid)
    task = SharedTasks.objects.get(id=tid)
    form =ShareTasksUpdateForm(instance=task)
    if request.method=='POST':
        task = SharedTasks.objects.filter(tasks_id=tid)
        print(task)
        
        return render(request,'todoapp/update_assigned_task.html',{"task":task})

    return render(request,'todoapp/update_assigned_task.html',{'form':form})


def NotificationForVerification(request):
    user_id =request.user.id
    print(user_id)
    data = SharedTasks.objects.filter(assigned_by=user_id,notify=True)
    return render(request,'todoapp/notification.html',{'data':data})

def VerifyTask(request,id):
   shared_task_data = SharedTasks.objects.get(id = id)
   data = Tasks.objects.get(id = shared_task_data.tasks_id)
   data.title = shared_task_data.title
   data.description = shared_task_data.description
   data.save()
   return HttpResponse("Your Task is verify and updated.")

def RejectTask(request,id):
    shared_task_data = SharedTasks.objects.get(id = id)
    data = Tasks.objects.get(id = shared_task_data.tasks_id)
    data.title = shared_task_data.title
    data.description = shared_task_data.description
    return HttpResponse("Your Task is Rejected.")

    