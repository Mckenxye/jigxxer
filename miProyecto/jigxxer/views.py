from django.shortcuts import render, redirect
from .models import Venta,Negocio
from .forms import VentaForm,CustomUserCreationForm,NegocioForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test


#verificadores de grupo
def es_cliente(user):
    return user.groups.filter(name='Cliente').exists()
def es_admin(user):
    return user.groups.filter(name='Administrador').exists()


#paginas disponibles para cada grupo
class ClienteView(LoginRequiredMixin, TemplateView):
    vista = 'vista.html' 
    nosotros = 'nosotrosC.html' 
    bienvenido = 'bienvenido.html'

class AdminView(LoginRequiredMixin, TemplateView):
    inico = 'inicio.html'
    nosotros = 'nostros.html'
    producto = 'index.html'
    crear = 'crear.html'
    form = 'form.html'
    editar = 'editar.html'
    negocio = 'negocioindex.html'

#login

@login_required
def mi_vista_de_redireccion(request):
    # Obtén el primer grupo del usuario
    group = request.user.groups.first()

    # Redirige basándose en el grupo del usuario
    if group.name == 'Administrador':
        return redirect('inicio')
    elif group.name == 'Cliente':
        return redirect('bienvenido')
    else:
        # Redirige a una URL por defecto si el usuario no tiene grupo
        return redirect('login')

def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('')

#funcion para registrarse como cliente o Administrador 

def registro(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save(commit=False)
            user_type = formulario.cleaned_data.get('user_type')
            if user_type is None:
                messages.error(request, 'El tipo de usuario no puede estar vacío.')
                return render(request, 'registration/registro.html', {'form': formulario})
            user.save()
            # Asignar el grupo correspondiente
            try:
                group_name = user_type.capitalize()
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                user.save()  # Guardar nuevamente el usuario para confirmar la asignación del grupo
                # Autenticar y logear al usuario
                username = formulario.cleaned_data.get('username')
                raw_password = formulario.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Registro correcto.')
                    # Redirigir al usuario según su grupo
                    if group_name == 'Administrador':
                        return redirect('formularioNegocio')
                    elif group_name == 'Cliente':
                        return redirect('bienvenido')
                    else:
                        messages.error(request, 'No se encontró un grupo válido para el usuario.')
                        return redirect('login')
                else:
                    messages.error(request, 'No se pudo autenticar al usuario.')
            except Group.DoesNotExist:
                messages.error(request, f'El grupo {group_name} no existe.')
        else:
            messages.error(request, formulario.errors)
    else:
        formulario = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': formulario})

#funcion para el formulario de negocio 
def crear_negocio(request):
    if request.method == 'POST':
        form = NegocioForm(request.POST, user=request.user)
        if form.is_valid():
            negocio = form.save(commit=False)
            negocio.save()
            return redirect('inicio')  # Redirige a donde desees después de crear el negocio
    else:
        form = NegocioForm(user=request.user)
    return render(request, 'registration/negociof.html', {'form': form})

# vistas de adminstrador
@login_required
@user_passes_test(es_admin)
def inicio(request):
    return render(request, "paginas/inicio.html")


# en esta funcion nos devuelve la pagina que habla sobre nosotros 
@login_required
@user_passes_test(es_admin)
def nosotros(request):
    return render(request, "paginas/nosotros.html")

#mostrar productos 
@login_required
@user_passes_test(es_admin)
def producto(request):
    # Filtra los negocios asociados con el usuario actual
    negocios_usuario = Negocio.objects.filter(usuario_administrador=request.user)
    # Obtiene todos los productos asociados con los negocios del usuario actual
    productos_usuario = Venta.objects.filter(Id_negocio__in=negocios_usuario)
    return render(request, "local/index.html", {'ventas': productos_usuario})

@login_required
@user_passes_test(es_admin)
def negocio(request):
    negocio = Negocio.objects.all() 
    return render(request, "local/negocioindex.html",{'negocios': negocio})

#funcion para crear productos 
@login_required
@user_passes_test(es_admin)
def crear(request):
    if request.method == 'POST':
        formulario = VentaForm(request.user, request.POST or None, request.FILES or None)
        if formulario.is_valid():
            venta = formulario.save(commit=False)
            venta.id_negocio = request.user.negocios.first()  # Asigna el negocio del usuario actual
            venta.save()
            return redirect('productos')
    else:
        formulario = VentaForm(user=request.user)
    return render(request, 'local/crear.html', {'formulario': formulario})


#funcion para editar informacion de los productos
@login_required 
@user_passes_test(es_admin)
def editar(request, Id_venta):
    venta = Venta.objects.get(Id_venta=Id_venta)
    formulario = VentaForm(user=request.user, instance=venta)  # Pasar el objeto user correctamente
    if request.method == 'POST':
        formulario = VentaForm(request.user, request.POST or None, request.FILES or None, instance=venta)
        if formulario.is_valid():
            formulario.save()
            return redirect('productos')
    return render(request, 'local/editar.html', {'formulario': formulario})

#funcion para eliminar productos
@login_required
@user_passes_test(es_admin)
def eliminar(request, Id_venta):
    # Busca la venta por su Id y asegúrate de que pertenezca a un negocio del usuario actual
    venta = get_object_or_404(Venta, Id_venta=Id_venta, Id_negocio__usuario_administrador=request.user)
    # Borra la venta
    venta.delete()
    return redirect('productos')

#funcion para el buscador de productos 
@login_required
@user_passes_test(es_admin)
def buscar_producto(request):
    q = request.GET.get('q', '')
    # Filtra los negocios asociados con el usuario actual
    negocios_usuario = Negocio.objects.filter(usuario_administrador=request.user)
    if q.strip():  # Verifica si se proporciona algún parámetro de búsqueda
        # Realiza la búsqueda si hay una consulta de búsqueda
        resultados = Venta.objects.filter(Id_negocio__in=negocios_usuario, producto__icontains=q)
    else:
        # Si no se proporciona ningún parámetro de búsqueda, muestra todos los productos asociados con los negocios del usuario actual
        resultados = Venta.objects.filter(Id_negocio__in=negocios_usuario)
    return render(request, 'local/index.html', {'resultados': resultados})

#vistas del cliente
@login_required
@user_passes_test(es_cliente)
def cliente(request):
    Ventas = Venta.objects.all() 
    return render(request, "local/clientes/vista.html", {'ventas':Ventas})

@login_required
@user_passes_test(es_cliente)
def bienvenido(request):
    return render(request, "local/clientes/bienvenido.html")

@login_required
@user_passes_test(es_cliente)
def sobre_nosotros(request):
    return render(request, "local/clientes/nosotrosC.html")
