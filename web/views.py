from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ClienteForm, ProfesorForm
from .models import CustomUser, Cliente, Profesor
from .decoradores import role_required
from .decoradores import solo_profesores



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('home_superusuario')
            elif user.rol == 'profesor':
                return redirect('home_profesor')
            else:
                return redirect('home_cliente')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')

@login_required
def home_redirect(request):
    if request.user.is_superuser:
        return redirect('home_superusuario')
    elif request.user.rol == 'profesor':
        return redirect('home_profesor')
    else:
        return redirect('home_cliente')

@login_required
def panel_superusuario(request):
    return render(request, 'home_superuser.html')


@login_required
@solo_profesores
def panel_profesor(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(dni__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()

    return render(request, 'home_profesor.html', {'clientes': clientes})

@login_required
def panel_cliente(request):
    return render(request, 'home_cliente.html')

@login_required
@role_required('profesor')
def profesores(request):
    return render(request, 'home_profesor.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def registrar_cliente(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        if user_form.is_valid() and cliente_form.is_valid():
            user = user_form.save(commit=False)
            user.rol = 'cliente'
            user.save()
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        cliente_form = ClienteForm()
    return render(request, 'registro_cliente.html', {
        'user_form': user_form,
        'cliente_form': cliente_form
    })

@login_required
def editar_perfil_cliente(request):
    cliente = Cliente.objects.get(user=request.user)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('home_cliente')  # redirige al panel del cliente
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'editar_perfil_cliente.html', {'form': form})

def registrar_profesor(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profesor_form = ProfesorForm(request.POST)
        if user_form.is_valid() and profesor_form.is_valid():
            user = user_form.save(commit=False)
            user.rol = 'profesor'  # Asignar el rol directamente
            user.save()

            profesor = profesor_form.save(commit=False)
            profesor.user = user
            profesor.save()

            return redirect('login')  # Redirigir al login después del registro
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

@login_required
def home_redirect(request):
    # Dependiendo del tipo de usuario, redirige a un panel específico
    if request.user.is_superuser:
        return redirect('home_superusuario')
    elif hasattr(request.user, 'profesor'):
        return redirect('home_profesor')
    else:
        return redirect('home_cliente')


def eliminar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            # Usa CustomUser en lugar de User
            usuario = CustomUser.objects.get(username=username)
            usuario.delete()
            messages.success(request, f"El usuario {username} ha sido eliminado correctamente.")
        except CustomUser.DoesNotExist:
            messages.error(request, f"El usuario con el nombre de usuario '{username}' no existe.")
        
        return redirect('home_superusuario')  # Redirige al panel de administración
    return render(request, 'ruta/a/tu/template.html')  # Aquí, asegúrate de que esto sea correcto.