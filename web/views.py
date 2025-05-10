# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ClienteForm, ProfesorForm
from .models import Cliente, Profesor
from django.db.models import Q
from .models import CustomUser

def registrar_cliente(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        if user_form.is_valid() and cliente_form.is_valid():
            user = user_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()
            return redirect('login')  # o donde quieras redirigir
    else:
        user_form = CustomUserCreationForm()
        cliente_form = ClienteForm()
    return render(request, 'registro_cliente.html', {
        'user_form': user_form,
        'cliente_form': cliente_form
    })

def registrar_profesor(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profesor_form = ProfesorForm(request.POST)
        if user_form.is_valid() and profesor_form.is_valid():
            user = user_form.save()
            profesor = profesor_form.save(commit=False)
            profesor.user = user
            profesor.save()
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        profesor_form = ProfesorForm()
    return render(request, 'registro_profesor.html', {
        'user_form': user_form,
        'profesor_form': profesor_form
    })



def buscar_usuarios(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        resultados = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'buscar_usuarios.html', {'resultados': resultados})

# Pagina de de inicio 
def home(request):
    return render(request, 'home.html')