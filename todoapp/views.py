

from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render
from .models import SharedTasks, User, UserManager,Tasks
from .utils import send_otp_via_email
from django.shortcuts import redirect
from .forms import ShareTasksForm,TasksForm,TaskForm2

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
    t = Tasks.objects.all()
    l = []

    for t in t:
        l.append(t.id)
    print(l)
    task = Tasks.objects.get(id=tid)
   
    form = TaskForm2(instance=task)
    task_id = task.id 
    print(task_id)
    if request.method=="POST":
        update_form = TaskForm2(request.POST,instance=task)
        if update_form.is_valid():
            fm = update_form.save(commit=False)
            fm.user = request.user
            fm.save()


            return HttpResponse("your task updated successfully")
        return HttpResponse("your form is not valid")
    return render(request,'todoapp/update_task.html',{"form":form,'tid':task_id})



def task_delete(request,tid):
    task = Tasks.objects.get(id=tid)
    task.delete()
    return HttpResponse("your task deleted successfilly")
    



# def update(request):
#     if request.method=="POST":
      
#         tid = request.POST.get('update_task')
#         form = TaskForm2(instance=tid)
#         if form.is_valid():
#             form.save()

#             return HttpResponse("your task updated successfully")
#         return HttpResponse("your form is not valid")
#     return HttpResponse("Gte request")
    



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
        task = SharedTasks.objects.create(to_user=user,tasks=tk,assigned_by=request.user.id)
        task.save()

        return HttpResponse("Your Task Successfully shared")

def ReceivedTasks(request):
    user_id = request.user.id
    task = SharedTasks.objects.filter(to_user=user_id)
    return render(request,'todoapp/received_tasks.html',{"task":task})
