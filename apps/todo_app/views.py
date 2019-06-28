from django.shortcuts import render, HttpResponse, redirect
from .models import User, Group, ToDo, SubTask
from django.contrib import messages
import bcrypt
import datetime
import re

# ----------------------------------------------------------------------------
# Routes to render templates
# ----------------------------------------------------------------------------


def index(request):
    # fdsafdsafdsafdsafdsa
    return render(request, 'todo_app/index.html')


def group(request):
    return render(request, 'todo_app/group.html')


def home(request, groupid):
    context = {
        'Todos': ToDo.objects.all(),
    }
    return render(request, 'todo_app/home.html', context)

# ----------------------------------------------------------------------------
# Route to validate, register group and redirect to home page
# ----------------------------------------------------------------------------


def addGroup(request):
    errors = Group.objects.group_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/groups')
    else:
        group_name = request.POST["group_name"]
        pw_to_hash = request.POST["password"]

        password = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        password = password.decode()

        new_group = Group.objects.create(
            group_name=group_name, password=password)
        request.session['groupid'] = new_group.id
        request.session['group_name'] = new_group.group_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/home/" + str(request.session['groupid']))

# ----------------------------------------------------------------------------
# Route to validate, register group and redirect to home page
# ----------------------------------------------------------------------------


def loginGroup(request):
    errors = Group.objects.group_login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/groups')

    else:
        current_group = Group.objects.get(
            group_name=request.POST['groupLogin'])
        request.session['groupid'] = current_group.id
        request.session['isloggedin'] = True
        request.session['group_name'] = current_group.group_name
        return redirect("/home/" + str(request.session['groupid']))


# ----------------------------------------------------------------------------
# Route to validate, register user and redirect to group page
# ----------------------------------------------------------------------------

def addUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect('/')

    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        pw_to_hash = request.POST["password"]

        password = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        password = password.decode()

        new_user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, password=password)
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/groups")

# ----------------------------------------------------------------------------
# Route to login and route to home page
# ----------------------------------------------------------------------------


def loginUser(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect('/')
    else:
        current_user = User.objects.get(email=request.POST['emailLogin'])
        request.session['userid'] = current_user.id
        request.session['isloggedin'] = True
        request.session['first_name'] = current_user.first_name
        return redirect("/groups")

# ----------------------------------------------------------------------------
# Route to logout user
# ----------------------------------------------------------------------------


def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')

# ----------------------------------------------------------------------------
# Route to add task
# ----------------------------------------------------------------------------


def add_task(request):
    new_task = SubTask.objects.create(
        task=request.POST['task'], task_for=request.session['todo.id'])

    return redirect("/view")

# ----------------------------------------------------------------------------
# Route to view task
# ----------------------------------------------------------------------------


def view(request):
    return render(request, 'todo_app/view_todo.html')

# ----------------------------------------------------------------------------
# Route to new todo
# ----------------------------------------------------------------------------


def new_todo(request):
    return render(request, 'todo_app/new_todo.html')
# ----------------------------------------------------------------------------
# Route to add a todo
# ----------------------------------------------------------------------------


def add_todo(request):
    # errors = ToDo.objects.todo_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, extra_tags=key)
    #     return redirect('/')
    # else:
    # sent_by = User.objects.get(id=request.session['userid'])
    todo = request.POST['todo']
    desc = request.POST['todo_desc']
    start = request.POST['start']
    end = request.POST['end']
    name = request.POST['name']

    ToDo.objects.create(
        todo=todo, desc=desc, start=start, end=end, name=name)
    return redirect("/home/" + str(request.session['groupid']))


def remove_todo(request, todoid):
    current_todo = ToDo.objects.get(id=todoid)
    current_todo.delete()
    return redirect("/home/" + str(request.session['groupid']))


