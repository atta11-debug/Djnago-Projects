from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def signup(request):
    if request.method == "POST":
        username = request.POST.get("fnm")
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Useername already taken")
            return redirect("signup")

        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        messages.success(request, "Account Created Successfully!")
        return redirect("loginn")

    return render(request, "signup.html")


def loginn(request):
    if request.method == "POST":
        username = request.POST.get("fnm")
        password = request.POST.get("pwd")
        userr = authenticate(request, username=username, password=password)

        if userr is not None:
            login(request, userr)
            messages.success(request, "Login Successfully!")
            return redirect("/todopage")
        else:
            messages.error(request, "Not valid login credentials!")
            return redirect("loginn")

    return render(request, "loginn.html")


@login_required(login_url="loginn")
def todopage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        obj = models.todo(title=title, user=request.user)
        obj.save()

        user = request.user
        tasks = models.todo.objects.filter(user=request.user).order_by("-date")
        return redirect("todopage")
    tasks = models.todo.objects.filter(user=request.user).order_by("-date")
    return render(request, "todo.html", {"tasks": tasks})


@login_required(login_url="loginn")
def edit_todo(request, srno):
    obj = get_object_or_404(models.todo, srno=srno, user=request.user)
    if request.method == "POST":
        obj.title = request.POST.get("title")
        obj.save()
        return redirect("todopage")
    return render(request, "edit_todo.html", {"obj": obj})


@login_required(login_url="loginn") 
def delete_task(request, srno):
    obj = get_object_or_404(models.todo, srno=srno, user=request.user)
    obj.delete()
    return redirect("todopage")


def signout(request):
    logout(request)
    return redirect("loginn")
