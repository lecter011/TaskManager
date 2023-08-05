from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        # Create a new user from the submitted form
        # and save it to the database
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Create a new user from the submitted form
                # and save it to the database
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()

                # Save the session data
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm(),
                        "error": "That username has already been taken. Please choose a new username.",
                    },
                )
        else:
            # Tell the user the passwords didn't match
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm(), "error": "Passwords did not match."},
            )

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks})

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by("-datecompleted")
    print(tasks)
    return render(request, "tasks.html", {"tasks": tasks})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": CreateTaskForm()})
    else:
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": CreateTaskForm, "error": "Invalid values. Try again."},
            )

@login_required
def detail_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = CreateTaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            CreateTaskForm(request.POST, instance=task).save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": CreateTaskForm(), "error": "Invalid values."},
            )

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
    task.save()
    return redirect("tasks")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect("tasks")

@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username and password is not correct.",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")
    else:
        return render(request, "signin.html", {"form": AuthenticationForm()})
