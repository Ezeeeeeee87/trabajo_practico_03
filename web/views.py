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

def home(request):
    return render(request, 'base.html')

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
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('superuser_dashboard')
        elif user.rol == 'profesor':
            return redirect('profesor_dashboard')
        elif user.rol == 'cliente':
            return redirect('cliente_dashboard')
    return redirect('login')

@login_required
def panel_superusuario(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        resultados = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    
    context = {
        'resultados': resultados,
        'query': query,  
    }

    return render(request, 'home_superuser.html', context)


@login_required
@solo_profesores
def panel_profesor(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        resultados = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    
    context = {
        'resultados': resultados,
        'query': query,  
    }

    return render(request, 'home_profesor.html', context)

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
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.rol = 'cliente'
            user.save()

            # Crear instancia Cliente asociada al usuario
            Cliente.objects.create(
                user=user,
                direccion=user.direccion,
                genero=user.genero,
                dni=user.dni
            )

            messages.success(request, 'Cliente creado con éxito.')
            return redirect('home_superusuario')
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'registro_cliente.html', {'user_form': user_form})

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
            
            messages.success(request, 'Profesor creado con éxito.')
            return redirect('home_superusuario')  # Redirigir después del registro
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
        confirm = request.POST.get('confirm')

        if not username:
            messages.error(request, "No se especificó ningún usuario.")
            return redirect('home_superusuario')

        if confirm == '1':
            usuario = CustomUser.objects.filter(username=username).first()  # Confirmación final → eliminar
            if usuario:
                usuario.delete()
                messages.success(request, f"El usuario '{username}' ha sido eliminado.")
            else:
                messages.error(request, f"El usuario '{username}' no existe.")
            return redirect('home_superusuario')

        return redirect(f'/eliminar_usuario/?username={username}') # Primera vez: redirigir a confirmación

    username = request.GET.get('username') # GET → mostrar confirmación
    if not username:
        messages.error(request, "No se especificó ningún usuario para eliminar.")
        return redirect('home_superusuario')

    usuario = CustomUser.objects.filter(username=username).first()
    if not usuario:
        messages.error(request, f"El usuario '{username}' no existe.")
        return redirect('home_superusuario')

    return render(request, 'eliminar_usuario.html', {'usuario': usuario})


# def eliminar_usuario(request,username):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         try:
#             usuario = CustomUser.objects.get(username=username)
#             usuario.delete()
#             messages.success(request, f"El usuario {username} ha sido eliminado correctamente.")
#         except CustomUser.DoesNotExist:
#             messages.error(request, f"El usuario con el nombre de usuario '{username}' no existe.")
        
#         return redirect('home_superusuario')  # Redirige al panel de administración
#     return render(request, 'base.html')  # Aquí, asegúrate de que esto sea correcto.