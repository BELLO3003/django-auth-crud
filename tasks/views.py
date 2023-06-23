from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm #Plantilla de Formulario de Crear Cuenta
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1']) #Crea el Usuario con los datos proporcionados
                user.save() #Guarda el usuario en la BdD
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error":'ADVERTENCIA: Username already exist'
        })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error":'ADVERTENCIA: Las PS no coinciden'
        })    


def home(request):
    return render(request, 'home.html')

def tasks(request):
    return render(request, 'tasks.html')

from .forms import TaskForm
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form=TaskForm(request.POST) #Creamos otro formulario para almacenar los datos que el usuario introduce
            new_task=form.save(commit=False)#Ver los datos pero sin guardarlos
            new_task.user=request.user #Obtenemos el ID del usuario de la sesión existente y lo ponemos como FK
            new_task.save() #Guardar los datos en la BdD
            return redirect('tasks')
        except ValueError: 
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': "Proporciona datos validos"
        })

from django.contrib.auth.decorators import login_required
@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def task_detail(request,task_id): #Método para mostrar los detalles de las tareas y editarlos
        if request.method == 'GET':
            task=get_object_or_404(Task,pk=task_id,user=request.user) #Mostrará solo las tareas pertenecientes al usuario
            form = TaskForm(instance=task)
            return render(request, 'task_detail.html', {'task':task, 'form': form})
        else:
            try:
                task=get_object_or_404(Task,pk=task_id,user=request.user)
                form=TaskForm(request.POST, instance=task)#Toma los datos introducidos y genera un nuevo formulario
                form.save()#Guarda el formulario (actualiza los datos)
                return redirect('tasks')
            except ValueError: 
                return render(request,'task_detail.html', {
                'task':task, 'form': form,
                'error': "Proporciona datos validos"
        })

from django.utils import timezone
@login_required
def complete_task(request,task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now() #Se marca como completada una tarea al asignarle la fecha actual
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Usuario o contraseña incorrecta"
            })
        else:             
            login(request, user)
            return redirect('tasks') #Si los datos son correctos se nos direcciona a la página de Tasks