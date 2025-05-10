from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, ClienteForm, ProfesorForm
from .models import CustomUser

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Redirigir según el tipo de usuario
            if user.is_superuser:
                return redirect('home_superusuario')  # Redirigir a home de superusuario
            elif user.groups.filter(name='Profesores').exists():
                return redirect('home_profesor')  # Redirigir a home de profesor
            else:
                return redirect('home_cliente')  # Redirigir a home de cliente

        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html')
    



@login_required
def home_redirect(request):
    if request.user.is_superuser:
        return redirect('home_superusuario')  # Redirigir al home de superusuario
    elif request.user.groups.filter(name='profesores').exists():
        return redirect('home_profesor')  # Redirigir al home de profesor
    else:
        return redirect('home_cliente')  # Redirigir al home de cliente

@login_required
def panel_superusuario(request):
    return render(request, 'home_superusuario.html')  # Cambiar al home de superusuario

@login_required
def panel_profesor(request):
    return render(request, 'home_profesor.html')  # Cambiar al home de profesor

@login_required
def panel_cliente(request):
    return render(request, 'home_cliente.html')  # Cambiar al home de cliente

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')  # Redirige a la plantilla logout.html



def es_profesor(user):
    return user.groups.filter(name='profesores').exists()

@login_required
@user_passes_test(es_profesor)
def profesores(request):
    return render(request, 'profesores.html')



def registrar_cliente(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        if user_form.is_valid() and cliente_form.is_valid():
            user = user_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()
            return redirect('login')  # Redirigir a la página de login después del registro
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
            return redirect('login')  # Redirigir a la página de login después del registro
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
def panel_superusuario(request):
    form_profesor = ProfesorForm()
    form_cliente = CustomUserCreationForm()

    if request.method == 'POST':
        if 'puesto' in request.POST:
            # Crear profesor
            form_profesor = ProfesorForm(request.POST)
            form_usuario = CustomUserCreationForm(request.POST)
            if form_profesor.is_valid() and form_usuario.is_valid():
                user = form_usuario.save()
                grupo, _ = Group.objects.get_or_create(name='profesores')
                user.groups.add(grupo)
                profesor = form_profesor.save(commit=False)
                profesor.usuario = user
                profesor.save()
                return redirect('panel_superusuario')  # Redirigir al panel de superusuario

        else:
            # Crear cliente
            form_usuario = CustomUserCreationForm(request.POST)
            if form_usuario.is_valid():
                user = form_usuario.save()
                return redirect('panel_superusuario')  # Redirigir al panel de superusuario

    context = {
        'form_profesor': form_profesor,
        'form_cliente': form_cliente,
    }
    return render(request, 'superusuario.html', context)